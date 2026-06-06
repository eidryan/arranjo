# Design: Mapofluxograma Visual Fix — Clean Routing, No Crossings

**Date:** 2026-06-06  
**File to edit:** `scripts/generate_outputs.py` — `build_layout_svg()` function (with_flow=True branch)  
**Regeneration:** `.\scripts\run_all.ps1` (updates `06_dashboard/renders/mapofluxograma_render.svg` and the drawio file)

---

## Problem

The current mapofluxograma uses straight `<line>` elements between fixed MAPO_POS coordinates. This causes:

1. **QC ping-pong**: P20 and P23 are in the far-left Inspeção/QC zone; the steps they connect (P19, P21, P22, P24) are on the right side — producing long left-right crossings that make the flow unreadable.
2. **Wood track zig-zag**: P14 is placed to the left of P13, so 13→14 goes backward-left and 14→15 goes forward-right, creating an X pattern.
3. **Metal track up-down-up**: P8 (politriz) sits above P7 (espera), so the flow goes 6↓7 then 7↗8 then 8↓9 — visually inconsistent.
4. **2→11 crosses Recebimento**: The direct diagonal from Estoque MP (P2) to Setor Madeira boundary (P11) passes through the Recebimento/Expedição zone, which is unrelated to that transport step.
5. **Legend overlaps P4**: Legend box was in top-left, covering the P4 node at (160,131).

---

## Solution

Two changes: **comprehensive MAPO_POS repositioning** + **elbow routing for zone-crossing edges**.

### Draw order

Edges rendered first, nodes rendered on top. Arrowheads land behind circles cleanly.

---

## New MAPO_POS

All coordinates in meters on the 24 m × 16 m layout. Scale: 38 px/m, origin offset: x=65px, y=55px.

### Metal track (green, Setor Metal x=0–13 m, y=0–8 m)

| # | Process | x_m | y_m | SVG x | SVG y | Note |
|---|---------|-----|-----|-------|-------|------|
| 1 | Receber | 11.5 | 12.0 | 502 | 511 | Recebimento zone |
| 2 | Armazenar MP | 7.5 | 10.0 | 350 | 435 | Estoque MP |
| 3 | Transportar aço | 3.5 | 8.3 | 198 | 370 | Metal/bottom boundary |
| 4 | Laser corte | 2.5 | 2.0 | 160 | 131 | top-left Metal |
| 5 | Insp. blanks | 5.5 | 2.0 | 274 | 131 | top Metal — 4→5 horizontal |
| 6 | Forno TT | 8.5 | 2.0 | 388 | 131 | top Metal — 5→6 horizontal |
| 7 | Esperar resfr. | 8.5 | 4.5 | 388 | 226 | 6→7 straight down |
| 8 | Politriz | 11.0 | 4.5 | 483 | 226 | **same y as P7** — 7→8 horizontal |
| 9 | Afiador | 11.0 | 6.5 | 483 | 302 | 8→9 straight down |
| 10 | Armazenar semi | 9.5 | 7.0 | 426 | 321 | bottom Metal |

**Metal track pattern:** 4→5→6 all horizontal at y=2 m. 6↓7 down. 7→8 horizontal at y=4.5 m. 8↓9 down. 9↘10 small diagonal. No up-then-down jumps.

### Wood track (brown, Setor Madeira x=13–24 m, y=0–9 m)

| # | Process | x_m | y_m | SVG x | SVG y | Note |
|---|---------|-----|-----|-------|-------|------|
| 11 | Transportar madeira | 14.0 | 7.5 | 597 | 340 | boundary Wood — moved up from 8.3 |
| 12 | Esquadrejadeira | 15.0 | 2.0 | 635 | 131 | top-left Wood |
| 13 | Router CNC | 19.0 | 2.0 | 787 | 131 | top-center — 12→13 horizontal |
| 14 | Lixadeira | 19.0 | 5.0 | 787 | 245 | **same x as P13** — 13→14 straight down |
| 15 | Acabamento | 22.0 | 5.0 | 901 | 245 | **same y as P14** — 14→15 horizontal |
| 16 | Esperar cura | 22.0 | 7.0 | 901 | 321 | 15→16 straight down |
| 17 | Insp. madeira | 21.0 | 8.5 | 863 | 378 | 16→17 small diagonal; offset from P15/16 column |

**Wood track pattern:** 12→13 horizontal. 13↓14 straight down. 14→15 horizontal. 15↓16 straight down. 16↘17 small diagonal. Clean grid, no zig-zag.

### Assembly / shipping (dark, Montagem + Embalagem + Recebimento)

| # | Process | x_m | y_m | SVG x | SVG y | Note |
|---|---------|-----|-----|-------|-------|------|
| 18 | Transportar montagem | 14.0 | 9.5 | 597 | 416 | entry Montagem |
| 19 | Rebitagem | 14.5 | 11.5 | 616 | 492 | Montagem left |
| 20 | Insp. montagem | 16.5 | 11.5 | 692 | 492 | **INLINE** next to P19 — was (2.5, 9.5) |
| 21 | Montar kit | 18.5 | 11.5 | 768 | 492 | Montagem right — 19→20→21 all horizontal |
| 22 | Selar blister | 21.5 | 11.0 | 882 | 473 | Embalagem top |
| 23 | Insp. embalado | 21.5 | 12.5 | 882 | 530 | **INLINE** below P22 — was (2.5, 11.5) |
| 24 | Embalar envio | 21.5 | 14.0 | 882 | 587 | Embalagem bottom — 22↓23↓24 straight down |
| 25 | Armazenar PA | 7.5 | 14.5 | 350 | 606 | Est. Intermediário |
| 26 | Transportar exped. | 11.5 | 15.0 | 502 | 625 | Recebimento |

---

## Elbow Routing

Four edges use `<polyline>` instead of `<line>`. All others use `<line>`.

| Edge | Type | Waypoints (SVG px) | Reason |
|------|------|--------------------|--------|
| 2→11 | V-then-H | 350,435 → 350,340 → 597,340 | Goes UP first, then right — avoids crossing Recebimento zone |
| 10→18 | H-then-V | 426,321 → 597,321 → 597,416 | Exits Metal rightward at zone boundary, then drops into Montagem |
| 17→18 | V-then-H | 863,378 → 863,416 → 597,416 | Drops from P17 (offset x=863, not x=901), then goes left to P18 — avoids visual merge with P15/P16 column |
| 24→25 | V-H-V | 882,587 → 882,655 → 350,655 → 350,606 | Routes along bottom border below all zones, then comes up to P25 |

All elbows use `marker-end` on the final segment only.

---

## Legend

Moved to **bottom-right** of SVG at approximately (810, 600), clear of all process nodes. Contains three color-coded lines: Trilha Metálica (1–10), Trilha Madeira (11–17), Montagem/Embalagem (18–26).

---

## What Does NOT Change

- Zone rectangles and colors — unchanged
- Zone labels — unchanged
- Dimension annotations (24 m, 16 m) — unchanged
- Node circle style (r=15, color by process type, stroke by track) — unchanged
- `write_mapoflow()` drawio function — update to match new MAPO_POS for consistency
- Layout SVG (`with_flow=False`) — unchanged

---

## Implementation Scope

Edit only `scripts/generate_outputs.py`:
- Replace `MAPO_POS` dict inside `build_layout_svg()` with_flow branch
- Replace straight `<line>` edges with elbow `<polyline>` for the 4 edges listed above
- Move legend rect to bottom-right position
- Update `write_mapoflow()` to use the same MAPO_POS coordinates

Then run `.\scripts\run_all.ps1` and commit.
