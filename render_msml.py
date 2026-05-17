#!/usr/bin/env python3
"""MSML renderer — all 9 SysML diagram types. Modular, one class per diagram type."""

import json, math, sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("pip install Pillow")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DIAGRAM_ABBREV = {
    "bdd": "bdd", "ibd": "ibd", "activity": "act", "sequence": "sd",
    "state_machine": "stm", "use_case": "uc", "requirement": "req",
    "parametric": "par", "package": "pkg",
}

FONT_PATHS = [
    "/System/Library/Fonts/Helvetica.ttc",
    "/Library/Fonts/Arial.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "C:/Windows/Fonts/arial.ttf",
]

# Per-relationship-type line defaults: dashed, source head, target head, auto label
REL_DEFAULTS = {
    "composition":       dict(dashed=False, src="composition", tgt="none"),
    "aggregation":       dict(dashed=False, src="aggregation",  tgt="none"),
    "generalization":    dict(dashed=False, src="none",         tgt="triangle"),
    "realization":       dict(dashed=True,  src="none",         tgt="triangle"),
    "dependency":        dict(dashed=True,  src="none",         tgt="open"),
    "association":       dict(dashed=False, src="none",         tgt="none"),
    "include":           dict(dashed=True,  src="none",         tgt="open",  label="«include»"),
    "extend":            dict(dashed=True,  src="none",         tgt="open",  label="«extend»"),
    "transition":        dict(dashed=False, src="none",         tgt="open"),
    "control_flow":      dict(dashed=False, src="none",         tgt="filled"),
    "object_flow":       dict(dashed=True,  src="none",         tgt="open"),
    "connector":         dict(dashed=False, src="none",         tgt="none"),
    "binding_connector": dict(dashed=False, src="none",         tgt="none"),
    "derive":            dict(dashed=True,  src="none",         tgt="open",  label="«derive»"),
    "satisfy":           dict(dashed=True,  src="none",         tgt="open",  label="«satisfy»"),
    "verify":            dict(dashed=True,  src="none",         tgt="open",  label="«verify»"),
    "refine":            dict(dashed=True,  src="none",         tgt="open"),
    "containment":       dict(dashed=False, src="none",         tgt="filled"),
    "package_import":    dict(dashed=True,  src="none",         tgt="triangle"),
    "package_merge":     dict(dashed=True,  src="none",         tgt="triangle"),
}

# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def parse_color(hex_str: str) -> tuple:
    s = hex_str.lstrip("#")
    if len(s) == 6:
        return (int(s[0:2],16), int(s[2:4],16), int(s[4:6],16), 255)
    if len(s) == 8:
        return (int(s[0:2],16), int(s[2:4],16), int(s[4:6],16), int(s[6:8],16))
    raise ValueError(f"bad color {hex_str!r}")

def load_font(size: int) -> ImageFont.ImageFont:
    for p in FONT_PATHS:
        try:
            return ImageFont.truetype(p, max(8, size))
        except (IOError, OSError):
            continue
    return ImageFont.load_default()

def tbbox(draw, text, font):
    bb = draw.textbbox((0,0), text, font=font)
    return bb[2]-bb[0], bb[3]-bb[1]

def center_text(draw, x, y, w, h, text, font, color):
    tw, th = tbbox(draw, text, font)
    draw.text((x+(w-tw)/2, y+(h-th)/2), text, fill=color, font=font)

# ---------------------------------------------------------------------------
# Base Renderer
# ---------------------------------------------------------------------------

class MSMLRenderer:
    FRAME_BORDER = 2
    TAB_HEIGHT   = 30

    def __init__(self, data: dict):
        d = data["diagram"]
        self.d = d
        self.elements = {e["id"]: e for e in d.get("elements", [])}
        self.relationships = d.get("relationships", [])
        c = d["canvas"]
        self.cw, self.ch = c["width"], c["height"]
        self.ox = self.FRAME_BORDER
        self.oy = self.TAB_HEIGHT + self.FRAME_BORDER

    def cx(self, x): return self.ox + x
    def cy(self, y): return self.oy + y

    # ---------------------------------------------------------------- render

    def render(self, output_path: Path):
        iw = self.cw + 2*self.FRAME_BORDER
        ih = self.ch + self.TAB_HEIGHT + 2*self.FRAME_BORDER
        img = Image.new("RGBA", (iw, ih), (255,255,255,255))
        draw = ImageDraw.Draw(img)
        bg = parse_color(self.d["canvas"].get("background_color","#FFFFFF"))
        draw.rectangle([self.ox, self.oy, self.ox+self.cw-1, self.oy+self.ch-1], fill=bg)
        self._draw_frame(draw)
        for el in sorted(self.d.get("elements",[]),
                         key=lambda e: e.get("layout",{}).get("z_index",0)):
            self._draw_element(draw, el)
        for rel in self.relationships:
            self._draw_relationship(draw, rel)
        img.save(str(output_path), "PNG")
        print(f"  {output_path.name}")

    # ---------------------------------------------------------------- frame

    def _draw_frame(self, draw):
        frame = self.d.get("frame", {})
        if not frame.get("visible", True):
            return
        st = frame.get("style", {})
        bc = parse_color(st.get("border_color","#333333"))
        bw = max(1, int(st.get("border_width", 2)))
        iw = self.cw + 2*self.FRAME_BORDER
        ih = self.ch + self.TAB_HEIGHT + 2*self.FRAME_BORDER
        draw.rectangle([0, self.TAB_HEIGHT, iw-1, ih-1], outline=bc, width=bw)
        abbrev = DIAGRAM_ABBREV.get(self.d["type"], self.d["type"])
        ctx  = self.d.get("context","")
        name = self.d.get("name","")
        label = f"{abbrev} [{ctx}] {name}" if ctx else f"{abbrev} {name}"
        ts = st.get("tab", {})
        fc = ts.get("font", {})
        font = load_font(int(fc.get("size", 11)))
        px, py = ts.get("padding_x", 8), ts.get("padding_y", 4)
        tw, _ = tbbox(draw, label, font)
        chamfer = 10
        tab_w = tw + 2*px + chamfer
        tab_h = self.TAB_HEIGHT
        fill  = parse_color(ts.get("fill_color","#FFFFFF"))
        out   = parse_color(ts.get("border_color","#333333"))
        pts = [(0,0),(tab_w,0),(tab_w,tab_h-chamfer),(tab_w-chamfer,tab_h),(0,tab_h)]
        draw.polygon(pts, fill=fill)
        draw.line(pts+[pts[0]], fill=out, width=bw)
        draw.text((px, py), label, fill=parse_color(fc.get("color","#000000")), font=font)

    # ------------------------------------------------------------ elements

    def _draw_element(self, draw, el):
        handler = getattr(self, f"_draw_{el['type']}", None)
        if handler:
            handler(draw, el)

    # Shared element types used across multiple diagram types

    def _draw_initial_pseudostate(self, draw, el):
        self._draw_initial_node(draw, el)

    def _draw_initial_node(self, draw, el):
        lo, st = el["layout"], el.get("style",{})
        x, y, w, h = self.cx(lo["x"]), self.cy(lo["y"]), lo["width"], lo["height"]
        draw.ellipse([x,y,x+w,y+h], fill=parse_color(st.get("fill_color","#000000")))

    def _draw_final_state(self, draw, el):
        lo, st = el["layout"], el.get("style",{})
        x, y, w, h = self.cx(lo["x"]), self.cy(lo["y"]), lo["width"], lo["height"]
        border = parse_color(st.get("border_color","#000000"))
        draw.ellipse([x,y,x+w,y+h], fill=parse_color(st.get("fill_color","#FFFFFF")), outline=border, width=2)
        m = w*0.28
        draw.ellipse([x+m,y+m,x+w-m,y+h-m], fill=border)

    def _draw_activity_final_node(self, draw, el):
        self._draw_final_state(draw, el)

    def _draw_flow_final_node(self, draw, el):
        lo, st = el["layout"], el.get("style",{})
        x, y, w, h = self.cx(lo["x"]), self.cy(lo["y"]), lo["width"], lo["height"]
        border = parse_color(st.get("border_color","#000000"))
        draw.ellipse([x,y,x+w,y+h], fill=parse_color(st.get("fill_color","#FFFFFF")), outline=border, width=2)
        m = 4
        draw.line([(x+m,y+m),(x+w-m,y+h-m)], fill=border, width=2)
        draw.line([(x+w-m,y+m),(x+m,y+h-m)], fill=border, width=2)

    def _draw_comment(self, draw, el):
        lo, st = el["layout"], el.get("style",{})
        x, y, w, h = self.cx(lo["x"]), self.cy(lo["y"]), lo["width"], lo["height"]
        fold = 12
        fill   = parse_color(st.get("fill_color","#FFFDE7"))
        border = parse_color(st.get("border_color","#999900"))
        pts = [(x,y),(x+w-fold,y),(x+w,y+fold),(x+w,y+h),(x,y+h)]
        draw.polygon(pts, fill=fill)
        draw.line(pts+[pts[0]], fill=border, width=1)
        draw.line([(x+w-fold,y),(x+w-fold,y+fold),(x+w,y+fold)], fill=border, width=1)
        font = load_font(int(st.get("font",{}).get("size",10)))
        fc   = parse_color(st.get("font",{}).get("color","#000000"))
        text = el.get("text", el.get("name",""))
        draw.text((x+6, y+6), text, fill=fc, font=font)

    # --------------------------------------------------------- relationships

    def _draw_relationship(self, draw, rel):
        src_el = self.elements.get(rel.get("source",""))
        tgt_el = self.elements.get(rel.get("target",""))
        if not src_el or not tgt_el:
            return
        rtype  = rel.get("type","")
        style  = rel.get("style",{})
        defaults = REL_DEFAULTS.get(rtype, {})

        line_color = parse_color(style.get("line_color","#333333"))
        lw = max(1, int(style.get("line_width", 1.5)))
        dashed = style.get("line_style","solid") == "dashed" or defaults.get("dashed", False)
        if "line_style" in style:
            dashed = style["line_style"] == "dashed"
        corner_r = style.get("corner_radius", 10)

        wps = rel.get("waypoints",[])
        if wps:
            pts = [(self.cx(p["x"]), self.cy(p["y"])) for p in wps]
        else:
            sl, tl = src_el["layout"], tgt_el["layout"]
            pts = [
                (self.cx(sl["x"]+sl["width"]/2),  self.cy(sl["y"]+sl["height"]/2)),
                (self.cx(tl["x"]+tl["width"]/2),  self.cy(tl["y"]+tl["height"]/2)),
            ]

        smooth = self._smooth(pts, corner_r)
        if dashed:
            self._dashed_poly(draw, smooth, line_color, lw)
        else:
            for i in range(len(smooth)-1):
                draw.line([smooth[i], smooth[i+1]], fill=line_color, width=lw)

        tgt_head = style.get("target_arrowhead", defaults.get("tgt","none"))
        src_head = style.get("source_arrowhead", defaults.get("src","none"))
        self._draw_head(draw, smooth[-2], smooth[-1], line_color, lw, tgt_head)
        if src_head != "none":
            self._draw_head(draw, smooth[1],  smooth[0],  line_color, lw, src_head)

        lbl_font = load_font(10)
        fc = parse_color(style.get("font",{}).get("color","#222222") if isinstance(style.get("font"),dict) else "#222222")

        # multiplicity labels near source and target ends
        mult_src = rel.get("multiplicity_source","")
        mult_tgt = rel.get("multiplicity_target","")
        if mult_src and len(smooth) >= 2:
            ex, ey = smooth[0]
            nx, ny = smooth[1]
            dx, dy = nx-ex, ny-ey
            dist = math.hypot(dx, dy) or 1
            px, py = ex + dx/dist*20, ey + dy/dist*20   # 20px along line
            ux, uy = -dy/dist, dx/dist                   # perpendicular
            draw.text((int(px + ux*6), int(py + uy*6)), mult_src, fill=fc, font=lbl_font)
        if mult_tgt and len(smooth) >= 2:
            ex, ey = smooth[-1]
            nx, ny = smooth[-2]
            dx, dy = nx-ex, ny-ey
            dist = math.hypot(dx, dy) or 1
            px, py = ex + dx/dist*20, ey + dy/dist*20
            ux, uy = -dy/dist, dx/dist
            draw.text((int(px + ux*6), int(py + uy*6)), mult_tgt, fill=fc, font=lbl_font)

        # relationship label (trigger/guard/effect/name/auto_label)
        auto_label = defaults.get("label","")
        parts = []
        if auto_label:
            parts.append(auto_label)
        if rel.get("trigger"): parts.append(rel["trigger"])
        if rel.get("guard"):   parts.append(f"[{rel['guard']}]")
        if rel.get("effect"):  parts.append(f"/ {rel['effect']}")
        if rel.get("name") and not auto_label: parts.append(rel["name"])
        if parts:
            label = " ".join(parts)
            off = style.get("label_offset",{"x":0,"y":0})
            mid = len(pts)//2
            mx = (pts[mid-1][0]+pts[mid][0])/2 + off.get("x",0)
            my = (pts[mid-1][1]+pts[mid][1])/2 + off.get("y",0)
            draw.text((int(mx)+4, int(my)-14), label, fill=fc, font=lbl_font)

    # --------------------------------------------------------- arrowheads

    def _draw_head(self, draw, p1, p2, color, lw, kind):
        if kind == "none":
            return
        dx, dy = p2[0]-p1[0], p2[1]-p1[1]
        dist = math.hypot(dx, dy)
        if dist < 1: return
        ux, uy = dx/dist, dy/dist
        al, aw = 12, 5
        L = (p2[0]-ux*al-uy*aw, p2[1]-uy*al+ux*aw)
        R = (p2[0]-ux*al+uy*aw, p2[1]-uy*al-ux*aw)
        if kind == "open":
            draw.line([L, p2], fill=color, width=lw)
            draw.line([R, p2], fill=color, width=lw)
        elif kind == "filled":
            draw.polygon([p2, L, R], fill=color)
        elif kind == "triangle":
            draw.polygon([p2, L, R], fill=(255,255,255,255), outline=color)
        elif kind in ("composition","aggregation"):
            # diamond: base at p2, extends back along line
            dl = 18
            dw = 7
            tip  = (p2[0]-ux*dl*2, p2[1]-uy*dl*2)
            left = (p2[0]-ux*dl-uy*dw, p2[1]-uy*dl+ux*dw)
            right= (p2[0]-ux*dl+uy*dw, p2[1]-uy*dl-ux*dw)
            fill = color if kind=="composition" else (255,255,255,255)
            draw.polygon([p2, left, tip, right], fill=fill, outline=color)

    # -------------------------------------------------------- polyline utils

    def _smooth(self, pts, radius=10):
        if len(pts) <= 2: return list(pts)
        out = [pts[0]]
        for i in range(1, len(pts)-1):
            p0,p1,p2 = pts[i-1], pts[i], pts[i+1]
            d1 = math.hypot(p1[0]-p0[0], p1[1]-p0[1])
            d2 = math.hypot(p2[0]-p1[0], p2[1]-p1[1])
            r  = min(radius, d1/2, d2/2)
            if r < 1: out.append(p1); continue
            u1x,u1y = (p1[0]-p0[0])/d1, (p1[1]-p0[1])/d1
            u2x,u2y = (p2[0]-p1[0])/d2, (p2[1]-p1[1])/d2
            bef = (p1[0]-u1x*r, p1[1]-u1y*r)
            aft = (p1[0]+u2x*r, p1[1]+u2y*r)
            out.append(bef)
            steps = max(6, int(r*0.8))
            for s in range(1, steps+1):
                t = s/steps
                bx = (1-t)**2*bef[0]+2*(1-t)*t*p1[0]+t**2*aft[0]
                by = (1-t)**2*bef[1]+2*(1-t)*t*p1[1]+t**2*aft[1]
                out.append((bx,by))
        out.append(pts[-1])
        return out

    def _dashed_poly(self, draw, pts, color, lw, dash=8, gap=5):
        rem, on = 0.0, True
        for i in range(len(pts)-1):
            p1,p2 = pts[i], pts[i+1]
            dx,dy = p2[0]-p1[0], p2[1]-p1[1]
            slen = math.hypot(dx, dy)
            if slen < 0.5: continue
            ux,uy = dx/slen, dy/slen
            pos = 0.0
            while pos < slen:
                need = (dash if on else gap) - rem
                take = min(need, slen-pos)
                if on:
                    draw.line([(p1[0]+ux*pos, p1[1]+uy*pos),
                                (p1[0]+ux*(pos+take), p1[1]+uy*(pos+take))],
                               fill=color, width=lw)
                pos += take; rem += take
                if rem >= (dash if on else gap): rem=0.0; on=not on

    # ------------------------------------------------ shared box primitives

    def _box(self, draw, x, y, w, h, fill, border, bw=2, r=0):
        if r:
            draw.rounded_rectangle([x,y,x+w,y+h], radius=r, fill=fill, outline=border, width=bw)
        else:
            draw.rectangle([x,y,x+w,y+h], fill=fill, outline=border, width=bw)

    def _stereotype_block(self, draw, x, y, w, h, stereotype, name, compartments,
                           fill, border, bw=2, r=6, font_size=12):
        """Draw a SysML classifier box: stereotype, name, divider, compartment lines."""
        self._box(draw, x, y, w, h, fill, border, bw, r)
        font_bold  = load_font(font_size)
        font_small = load_font(max(9, font_size-2))
        font_stereo= load_font(max(9, font_size-2))
        fc = (30,30,30,255)
        row_h = font_size + 6

        # stereotype row + name row in header band
        header_h = row_h * (2 if stereotype else 1) + 4
        cy_s = y + 4
        if stereotype:
            center_text(draw, x, cy_s, w, row_h, f"«{stereotype}»", font_stereo, fc)
            cy_s += row_h
        center_text(draw, x, cy_s, w, row_h, name, font_bold, fc)
        div_y = y + header_h
        draw.line([(x+bw, div_y),(x+w-bw, div_y)], fill=border, width=1)

        ty = div_y + 5
        for section in compartments:
            for line in section:
                draw.text((x+8, ty), line, fill=fc, font=font_small)
                _, lh = tbbox(draw, line, font_small)
                ty += lh + 3
            # divider between sections
            if section and section != compartments[-1]:
                draw.line([(x+bw, ty+2),(x+w-bw, ty+2)], fill=border, width=1)
                ty += 6


# ---------------------------------------------------------------------------
# BDD Renderer
# ---------------------------------------------------------------------------

class BDDRenderer(MSMLRenderer):

    def _draw_block(self, draw, el):
        lo, st = el["layout"], el.get("style",{})
        x,y,w,h = self.cx(lo["x"]), self.cy(lo["y"]), lo["width"], lo["height"]
        fill   = parse_color(st.get("fill_color","#DDEEFF"))
        border = parse_color(st.get("border_color","#336699"))
        bw = int(st.get("border_width",2))
        props = [f"  {p['name']}: {p['type']}" for p in el.get("compartments",{}).get("properties",[])]
        ops   = [f"  {o['name']}()" for o in el.get("compartments",{}).get("operations",[])]
        comps = []
        if props: comps.append(props)
        if ops:   comps.append(ops)
        self._stereotype_block(draw, x,y,w,h,
                               el.get("stereotype","block"),
                               el.get("name",""), comps,
                               fill, border, bw, r=4,
                               font_size=int(st.get("font",{}).get("size",12)))

    def _draw_value_type(self, draw, el):
        lo, st = el["layout"], el.get("style",{})
        x,y,w,h = self.cx(lo["x"]), self.cy(lo["y"]), lo["width"], lo["height"]
        fill   = parse_color(st.get("fill_color","#FFF8DC"))
        border = parse_color(st.get("border_color","#8B6914"))
        self._stereotype_block(draw, x,y,w,h, "value type", el.get("name",""), [],
                               fill, border, r=4,
                               font_size=int(st.get("font",{}).get("size",12)))

    def _draw_interface_block(self, draw, el):
        lo, st = el["layout"], el.get("style",{})
        x,y,w,h = self.cx(lo["x"]), self.cy(lo["y"]), lo["width"], lo["height"]
        fill   = parse_color(st.get("fill_color","#E8F4FD"))
        border = parse_color(st.get("border_color","#2E86AB"))
        self._stereotype_block(draw, x,y,w,h, "interface block", el.get("name",""), [],
                               fill, border, r=4,
                               font_size=int(st.get("font",{}).get("size",12)))


# ---------------------------------------------------------------------------
# IBD Renderer
# ---------------------------------------------------------------------------

class IBDRenderer(MSMLRenderer):

    def _draw_part(self, draw, el):
        lo, st = el["layout"], el.get("style",{})
        x,y,w,h = self.cx(lo["x"]), self.cy(lo["y"]), lo["width"], lo["height"]
        fill   = parse_color(st.get("fill_color","#EEF5DD"))
        border = parse_color(st.get("border_color","#557744"))
        bw = int(st.get("border_width",2))
        r  = int(st.get("corner_radius",4))
        self._box(draw, x,y,w,h, fill, border, bw, r)
        font = load_font(int(st.get("font",{}).get("size",11)))
        fc   = parse_color(st.get("font",{}).get("color","#000000"))
        label = el.get("name","")
        if el.get("type_ref"):
            label = f"{label}:{el['type_ref']}"
        center_text(draw, x, y, w, 34, label, font, fc)
        draw.line([(x+bw, y+34),(x+w-bw, y+34)], fill=border, width=1)

    def _draw_port(self, draw, el):
        lo, st = el["layout"], el.get("style",{})
        x,y,w,h = self.cx(lo["x"]), self.cy(lo["y"]), lo["width"], lo["height"]
        fill   = parse_color(st.get("fill_color","#FFFFFF"))
        border = parse_color(st.get("border_color","#333333"))
        draw.rectangle([x,y,x+w,y+h], fill=fill, outline=border, width=1)
        if el.get("name"):
            font = load_font(max(9, int(st.get("font",{}).get("size",9))))
            draw.text((x+w+3, y-1), el["name"], fill=border, font=font)

    def _draw_reference(self, draw, el):
        lo, st = el["layout"], el.get("style",{})
        x,y,w,h = self.cx(lo["x"]), self.cy(lo["y"]), lo["width"], lo["height"]
        fill   = parse_color(st.get("fill_color","#F5F5F5"))
        border = parse_color(st.get("border_color","#888888"))
        # dashed border for reference
        self._dashed_poly(draw,
            [(x,y),(x+w,y),(x+w,y+h),(x,y+h),(x,y)], border, 1)
        font = load_font(11)
        center_text(draw, x, y, w, h, el.get("name",""), font, border)


# ---------------------------------------------------------------------------
# Activity Renderer
# ---------------------------------------------------------------------------

class ActivityRenderer(MSMLRenderer):

    def _draw_action(self, draw, el):
        lo, st = el["layout"], el.get("style",{})
        x,y,w,h = self.cx(lo["x"]), self.cy(lo["y"]), lo["width"], lo["height"]
        fill   = parse_color(st.get("fill_color","#FFF8DC"))
        border = parse_color(st.get("border_color","#8B6914"))
        bw = int(st.get("border_width",2))
        r  = int(st.get("corner_radius",10))
        self._box(draw, x,y,w,h, fill, border, bw, r)
        font = load_font(int(st.get("font",{}).get("size",11)))
        fc   = parse_color(st.get("font",{}).get("color","#000000"))
        center_text(draw, x, y, w, h, el.get("name",""), font, fc)

    def _draw_call_behavior_action(self, draw, el):
        self._draw_action(draw, el)

    def _draw_decision_node(self, draw, el):
        self._draw_diamond(draw, el)

    def _draw_merge_node(self, draw, el):
        self._draw_diamond(draw, el)

    def _draw_diamond(self, draw, el):
        lo, st = el["layout"], el.get("style",{})
        x,y,w,h = self.cx(lo["x"]), self.cy(lo["y"]), lo["width"], lo["height"]
        cx2, cy2 = x+w/2, y+h/2
        pts = [(cx2, y), (x+w, cy2), (cx2, y+h), (x, cy2)]
        fill   = parse_color(st.get("fill_color","#FFFFFF"))
        border = parse_color(st.get("border_color","#333333"))
        draw.polygon(pts, fill=fill, outline=border)
        if el.get("name"):
            font = load_font(9)
            tw, th = tbbox(draw, el["name"], font)
            draw.text((cx2-tw/2, cy2-th/2), el["name"],
                      fill=parse_color(st.get("font",{}).get("color","#000000")), font=font)

    def _draw_fork_node(self, draw, el):
        self._draw_bar(draw, el)

    def _draw_join_node(self, draw, el):
        self._draw_bar(draw, el)

    def _draw_bar(self, draw, el):
        lo, st = el["layout"], el.get("style",{})
        x,y,w,h = self.cx(lo["x"]), self.cy(lo["y"]), lo["width"], lo["height"]
        fill = parse_color(st.get("fill_color","#000000"))
        draw.rectangle([x,y,x+w,y+h], fill=fill)

    def _draw_partition(self, draw, el):
        lo, st = el["layout"], el.get("style",{})
        x,y,w,h = self.cx(lo["x"]), self.cy(lo["y"]), lo["width"], lo["height"]
        fill   = parse_color(st.get("fill_color","#F5F5F5"))
        border = parse_color(st.get("border_color","#999999"))
        draw.rectangle([x,y,x+w,y+h], fill=fill, outline=border, width=1)
        font = load_font(11)
        tw, _ = tbbox(draw, el.get("name",""), font)
        draw.text((x+6, y+4), el.get("name",""),
                  fill=parse_color(st.get("font",{}).get("color","#555555")), font=font)


# ---------------------------------------------------------------------------
# Sequence Renderer
# ---------------------------------------------------------------------------

class SequenceRenderer(MSMLRenderer):

    def render(self, output_path: Path):
        iw = self.cw + 2*self.FRAME_BORDER
        ih = self.ch + self.TAB_HEIGHT + 2*self.FRAME_BORDER
        img = Image.new("RGBA", (iw, ih), (255,255,255,255))
        draw = ImageDraw.Draw(img)
        bg = parse_color(self.d["canvas"].get("background_color","#FFFFFF"))
        draw.rectangle([self.ox, self.oy, self.ox+self.cw-1, self.oy+self.ch-1], fill=bg)
        self._draw_frame(draw)
        # Draw lifeline dashed lines first (behind everything)
        for el in self.d.get("elements",[]):
            if el["type"] == "lifeline":
                self._draw_lifeline_line(draw, el)
        # Draw all elements
        for el in sorted(self.d.get("elements",[]),
                         key=lambda e: e.get("layout",{}).get("z_index",0)):
            self._draw_element(draw, el)
        # Messages
        for rel in self.relationships:
            self._draw_relationship(draw, rel)
        img.save(str(output_path), "PNG")
        print(f"  {output_path.name}")

    def _draw_lifeline_line(self, draw, el):
        lo = el["layout"]
        head_h = lo.get("head_height", 40)
        cx2 = self.cx(lo["x"] + lo["width"]/2)
        top = self.cy(lo["y"] + head_h)
        bot = self.cy(lo["y"] + lo["height"])
        self._dashed_poly(draw, [(cx2,top),(cx2,bot)],
                          parse_color(el.get("style",{}).get("border_color","#555555")), 1)

    def _draw_lifeline(self, draw, el):
        lo, st = el["layout"], el.get("style",{})
        x,y,w = self.cx(lo["x"]), self.cy(lo["y"]), lo["width"]
        head_h = lo.get("head_height", 40)
        fill   = parse_color(st.get("fill_color","#FFFFFF"))
        border = parse_color(st.get("border_color","#333333"))
        draw.rectangle([x,y,x+w,y+head_h], fill=fill, outline=border, width=2)
        font = load_font(int(st.get("font",{}).get("size",11)))
        fc   = parse_color(st.get("font",{}).get("color","#000000"))
        center_text(draw, x, y, w, head_h, el.get("name",""), font, fc)

    def _draw_execution_occurrence(self, draw, el):
        lo, st = el["layout"], el.get("style",{})
        x,y,w,h = self.cx(lo["x"]), self.cy(lo["y"]), lo["width"], lo["height"]
        fill   = parse_color(st.get("fill_color","#CCCCFF"))
        border = parse_color(st.get("border_color","#333399"))
        draw.rectangle([x,y,x+w,y+h], fill=fill, outline=border, width=1)

    def _draw_relationship(self, draw, rel):
        if rel.get("type") != "message":
            super()._draw_relationship(draw, rel)
            return
        src = self.elements.get(rel["source_lifeline"])
        tgt = self.elements.get(rel["target_lifeline"])
        if not src or not tgt:
            return
        msg_y = self.cy(rel.get("layout",{}).get("y", 100))
        sx = self.cx(src["layout"]["x"] + src["layout"]["width"]/2)
        tx = self.cx(tgt["layout"]["x"] + tgt["layout"]["width"]/2)

        sort    = rel.get("message_sort","synch_call")
        style   = rel.get("style",{})
        color   = parse_color(style.get("line_color","#333333"))
        lw      = max(1, int(style.get("line_width",1.5)))
        dashed  = sort in ("reply","asynch_call","asynch_signal")

        if dashed:
            self._dashed_poly(draw, [(sx,msg_y),(tx,msg_y)], color, lw)
        else:
            draw.line([(sx,msg_y),(tx,msg_y)], fill=color, width=lw)

        # arrowhead at tx
        head = "open" if dashed else "filled"
        if tx > sx:
            self._draw_head(draw, (sx,msg_y), (tx,msg_y), color, lw, head)
        else:
            self._draw_head(draw, (sx,msg_y), (tx,msg_y), color, lw, head)

        # label above
        if rel.get("name"):
            font = load_font(10)
            mx = (sx+tx)/2
            draw.text((int(mx-40), int(msg_y-14)), rel["name"],
                      fill=color, font=font)


# ---------------------------------------------------------------------------
# State Machine Renderer
# ---------------------------------------------------------------------------

class StateMachineRenderer(MSMLRenderer):

    def _draw_state(self, draw, el):
        lo, st = el["layout"], el.get("style",{})
        x,y,w,h = self.cx(lo["x"]), self.cy(lo["y"]), lo["width"], lo["height"]
        fill   = parse_color(st.get("fill_color","#F0E6FF"))
        border = parse_color(st.get("border_color","#6633AA"))
        bw = max(1,int(st.get("border_width",2)))
        r  = int(st.get("corner_radius",8))
        draw.rounded_rectangle([x,y,x+w,y+h], radius=r, fill=fill, outline=border, width=bw)
        font_cfg  = st.get("font",{})
        name_font = load_font(int(font_cfg.get("size",12)))
        fc = parse_color(font_cfg.get("color","#000000"))
        name_h = 34
        nw,nh = tbbox(draw, el.get("name",""), name_font)
        draw.text((x+(w-nw)/2, y+(name_h-nh)/2), el.get("name",""), fill=fc, font=name_font)
        div_y = int(y+name_h)
        draw.line([(x+bw,div_y),(x+w-bw,div_y)], fill=border, width=1)
        items = []
        if el.get("entry"): items.append(f"entry / {el['entry']}")
        if el.get("do"):    items.append(f"do / {el['do']}")
        if el.get("exit"):  items.append(f"exit / {el['exit']}")
        if items:
            sf = load_font(max(9,int(font_cfg.get("size",12))-2))
            ty = div_y+6
            for item in items:
                draw.text((x+8,ty), item, fill=fc, font=sf)
                _,lh = tbbox(draw, item, sf)
                ty += lh+4


# ---------------------------------------------------------------------------
# Use Case Renderer
# ---------------------------------------------------------------------------

class UseCaseRenderer(MSMLRenderer):

    def _draw_actor(self, draw, el):
        lo, st = el["layout"], el.get("style",{})
        x,y,w,h = self.cx(lo["x"]), self.cy(lo["y"]), lo["width"], lo["height"]
        fc = parse_color(st.get("border_color","#333333"))
        cx2 = x+w/2
        head_r = 12
        # head
        draw.ellipse([cx2-head_r, y, cx2+head_r, y+2*head_r], outline=fc, width=2)
        body_top = y+2*head_r
        body_bot = body_top+22
        draw.line([(cx2,body_top),(cx2,body_bot)], fill=fc, width=2)
        draw.line([(cx2-16,body_top+8),(cx2+16,body_top+8)], fill=fc, width=2)
        draw.line([(cx2,body_bot),(cx2-12,body_bot+14)], fill=fc, width=2)
        draw.line([(cx2,body_bot),(cx2+12,body_bot+14)], fill=fc, width=2)
        name = el.get("name","")
        font = load_font(int(st.get("font",{}).get("size",11)))
        tw,_ = tbbox(draw, name, font)
        draw.text((cx2-tw/2, y+h-18), name, fill=fc, font=font)

    def _draw_use_case(self, draw, el):
        lo, st = el["layout"], el.get("style",{})
        x,y,w,h = self.cx(lo["x"]), self.cy(lo["y"]), lo["width"], lo["height"]
        fill   = parse_color(st.get("fill_color","#FFF0F0"))
        border = parse_color(st.get("border_color","#993333"))
        draw.ellipse([x,y,x+w,y+h], fill=fill, outline=border, width=2)
        font = load_font(int(st.get("font",{}).get("size",11)))
        fc   = parse_color(st.get("font",{}).get("color","#000000"))
        center_text(draw, x, y, w, h, el.get("name",""), font, fc)

    def _draw_system_boundary(self, draw, el):
        lo, st = el["layout"], el.get("style",{})
        x,y,w,h = self.cx(lo["x"]), self.cy(lo["y"]), lo["width"], lo["height"]
        border = parse_color(st.get("border_color","#555555"))
        draw.rectangle([x,y,x+w,y+h], outline=border, width=2)
        font = load_font(11)
        draw.text((x+6, y+4), el.get("name",""), fill=border, font=font)


# ---------------------------------------------------------------------------
# Requirements Renderer
# ---------------------------------------------------------------------------

class RequirementRenderer(MSMLRenderer):

    def _draw_requirement(self, draw, el):
        lo, st = el["layout"], el.get("style",{})
        x,y,w,h = self.cx(lo["x"]), self.cy(lo["y"]), lo["width"], lo["height"]
        fill   = parse_color(st.get("fill_color","#F5F5FF"))
        border = parse_color(st.get("border_color","#444488"))
        bw = int(st.get("border_width",2))
        draw.rectangle([x,y,x+w,y+h], fill=fill, outline=border, width=bw)
        fs   = int(st.get("font",{}).get("size",11))
        fc   = parse_color(st.get("font",{}).get("color","#000000"))
        sf   = load_font(fs-1)
        bf   = load_font(fs)
        # «requirement» + id row
        stereo = f"«requirement»  {el.get('req_id','')}"
        draw.text((x+6, y+5), stereo, fill=border, font=sf)
        div1 = y+20
        draw.line([(x+bw,div1),(x+w-bw,div1)], fill=border, width=1)
        # name
        nw,nh = tbbox(draw, el.get("name",""), bf)
        draw.text((x+(w-nw)/2, div1+4), el.get("name",""), fill=fc, font=bf)
        div2 = div1+nh+10
        draw.line([(x+bw,div2),(x+w-bw,div2)], fill=border, width=1)
        # text
        text = el.get("text","")
        draw.text((x+6, div2+4), text, fill=fc, font=sf)

    def _draw_test_case(self, draw, el):
        lo, st = el["layout"], el.get("style",{})
        x,y,w,h = self.cx(lo["x"]), self.cy(lo["y"]), lo["width"], lo["height"]
        fill   = parse_color(st.get("fill_color","#E8F5E9"))
        border = parse_color(st.get("border_color","#2E7D32"))
        self._stereotype_block(draw, x,y,w,h, "testCase", el.get("name",""), [],
                               fill, border, r=4, font_size=11)


# ---------------------------------------------------------------------------
# Parametric Renderer
# ---------------------------------------------------------------------------

class ParametricRenderer(MSMLRenderer):

    def _draw_constraint_property(self, draw, el):
        lo, st = el["layout"], el.get("style",{})
        x,y,w,h = self.cx(lo["x"]), self.cy(lo["y"]), lo["width"], lo["height"]
        fill   = parse_color(st.get("fill_color","#FFFDE7"))
        border = parse_color(st.get("border_color","#827717"))
        bw = int(st.get("border_width",2))
        draw.rectangle([x,y,x+w,y+h], fill=fill, outline=border, width=bw)
        fs = int(st.get("font",{}).get("size",11))
        fc = parse_color(st.get("font",{}).get("color","#000000"))
        sf = load_font(fs-1)
        bf = load_font(fs)
        draw.text((x+4, y+3), "«constraint»", fill=border, font=sf)
        header_h = 20
        div = y+header_h
        draw.line([(x+bw,div),(x+w-bw,div)], fill=border, width=1)
        nw,nh = tbbox(draw, el.get("name",""), bf)
        draw.text((x+(w-nw)/2, div+3), el.get("name",""), fill=fc, font=bf)
        # parameters
        params = el.get("parameters",[])
        if params:
            ty = div+nh+10
            draw.line([(x+bw,ty),(x+w-bw,ty)], fill=border, width=1)
            ty += 4
            pf = load_font(max(8,fs-2))
            for p in params:
                ptext = f"  {p.get('name','')} : {p.get('type','')}"
                draw.text((x+4, ty), ptext, fill=fc, font=pf)
                _,lh = tbbox(draw, ptext, pf)
                ty += lh+3

    def _draw_value_property(self, draw, el):
        lo, st = el["layout"], el.get("style",{})
        x,y,w,h = self.cx(lo["x"]), self.cy(lo["y"]), lo["width"], lo["height"]
        fill   = parse_color(st.get("fill_color","#FFFFFF"))
        border = parse_color(st.get("border_color","#555555"))
        draw.rectangle([x,y,x+w,y+h], fill=fill, outline=border, width=1)
        font = load_font(int(st.get("font",{}).get("size",10)))
        fc   = parse_color(st.get("font",{}).get("color","#000000"))
        center_text(draw, x, y, w, h, el.get("name",""), font, fc)


# ---------------------------------------------------------------------------
# Package Renderer
# ---------------------------------------------------------------------------

class PackageRenderer(MSMLRenderer):

    def _draw_package(self, draw, el):
        self._draw_pkg_shape(draw, el, "#F5F5F5", "#555555")

    def _draw_model(self, draw, el):
        self._draw_pkg_shape(draw, el, "#EEF0FF", "#445588", stereotype="model")

    def _draw_profile(self, draw, el):
        self._draw_pkg_shape(draw, el, "#FFF0FF", "#885588", stereotype="profile")

    def _draw_pkg_shape(self, draw, el, def_fill, def_border, stereotype=None):
        lo, st = el["layout"], el.get("style",{})
        x,y,w,h = self.cx(lo["x"]), self.cy(lo["y"]), lo["width"], lo["height"]
        fill   = parse_color(st.get("fill_color", def_fill))
        border = parse_color(st.get("border_color", def_border))
        bw = int(st.get("border_width",1))
        tab_w, tab_h = 60, 16
        # tab
        draw.rectangle([x,y,x+tab_w,y+tab_h], fill=fill, outline=border, width=bw)
        # body
        draw.rectangle([x,y+tab_h,x+w,y+h], fill=fill, outline=border, width=bw)
        font = load_font(int(st.get("font",{}).get("size",12)))
        fc   = parse_color(st.get("font",{}).get("color","#000000"))
        name = el.get("name","")
        if stereotype:
            sf = load_font(9)
            draw.text((x+4, y+1), f"«{stereotype}»", fill=border, font=sf)
            draw.text((x+4, y+tab_h+4), name, fill=fc, font=font)
        else:
            draw.text((x+4, y+1), name, fill=fc, font=font)

    def _draw_class(self, draw, el):
        lo, st = el["layout"], el.get("style",{})
        x,y,w,h = self.cx(lo["x"]), self.cy(lo["y"]), lo["width"], lo["height"]
        fill   = parse_color(st.get("fill_color","#FFFFFF"))
        border = parse_color(st.get("border_color","#333333"))
        bw = int(st.get("border_width",1))
        draw.rectangle([x,y,x+w,y+h], fill=fill, outline=border, width=bw)
        font = load_font(int(st.get("font",{}).get("size",11)))
        fc   = parse_color(st.get("font",{}).get("color","#000000"))
        center_text(draw, x, y, w, 30, el.get("name",""), font, fc)
        draw.line([(x+bw,y+30),(x+w-bw,y+30)], fill=border, width=1)


# ---------------------------------------------------------------------------
# Dispatch table + public API
# ---------------------------------------------------------------------------

RENDERER_MAP = {
    "bdd":           BDDRenderer,
    "ibd":           IBDRenderer,
    "activity":      ActivityRenderer,
    "sequence":      SequenceRenderer,
    "state_machine": StateMachineRenderer,
    "use_case":      UseCaseRenderer,
    "requirement":   RequirementRenderer,
    "parametric":    ParametricRenderer,
    "package":       PackageRenderer,
}


def render(msml_path, output_path=None):
    src = Path(msml_path)
    dst = Path(output_path) if output_path else src.with_suffix(".png")
    with open(src) as f:
        data = json.load(f)
    dtype = data["diagram"]["type"]
    RENDERER_MAP.get(dtype, MSMLRenderer)(data).render(dst)


def main():
    if len(sys.argv) < 2:
        print("Usage: python render_msml.py <file.msml> [output.png]")
        sys.exit(1)
    render(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)


if __name__ == "__main__":
    main()
