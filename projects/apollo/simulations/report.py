"""Shared ESTIMATE banners. Simulation output is not a NASA fact."""

from __future__ import annotations

BANNER = (
    "ESTIMATE — educational only. Simulation output is not a NASA fact.\n"
    "Do not copy these numbers into architecture notes or shall statements."
)


def banner() -> None:
    print(BANNER)


def estimate(text: str) -> None:
    print(f"ESTIMATE  {text}")


def sourced(text: str) -> None:
    print(f"SOURCED   {text}")


def parameter(text: str) -> None:
    print(f"PARAMETER {text}")


def note(text: str) -> None:
    print(f"NOTE      {text}")
