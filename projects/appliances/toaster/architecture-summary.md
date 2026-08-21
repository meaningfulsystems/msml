# Toaster Architecture Summary

Two-slice pop-up toaster used as the **coverage canary** for all twelve MSML views. Namespace `Toaster`. File stem `toaster`.

## Parts

Toaster composed of BrowningControl, Timer, Lever, Carriage, HeatingElement, and ThermalCutoff. Context actors are the user and the power grid.

## Key numbers (from this model)

| Quantity | Value |
| --- | --- |
| Heat-up | Target temperature within 30 s |
| Browning timer | 1–5 min settings |
| Repeatability | ±5% energy variance at the same browning level |
| Thermal cutoff | Trip below 300 °C surface temperature |

This MSML toaster is the language canary. It does not copy every quantitative target from the SysML2d toaster example.

## Views

| View | File |
| --- | --- |
| BDD | `toaster-bdd` |
| IBD | `toaster-ibd` |
| Activity | `toaster-act` |
| Sequence | `toaster-seq` |
| STM | `toaster-stm` |
| Use case | `toaster-uc` |
| Requirements | `toaster-req` · `toaster-reqt` |
| Parametric | `toaster-par` |
| Package | `toaster-pkg` |
| Allocation | `toaster-alloc` · `toaster-amx` |

![Toaster block definitions](toaster-bdd.png)

![Toaster requirements table](toaster-reqt.png)

## Validate and render

```bash
msml-validate-all projects/appliances/toaster --strict
msml-render-all projects/appliances/toaster
```
