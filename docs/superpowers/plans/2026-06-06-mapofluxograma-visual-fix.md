# Mapofluxograma Visual Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix crossing/inconsistent arrows in the mapofluxograma SVG by repositioning all 26 process nodes and adding elbow routing for 4 zone-crossing edges.

**Architecture:** All changes are in `scripts/generate_outputs.py`. Task 1 replaces the `if with_flow:` block (lines 934–998) inside `build_layout_svg()`. Task 2 updates the matching `MAPO_POS` in `write_mapoflow()` (line 644). Task 3 regenerates, verifies, and deploys.

**Tech Stack:** Python 3.x, SVG, PowerShell, Vercel CLI.

---

## File Map

| File | Change |
|------|--------|
| `scripts/generate_outputs.py` | Replace `if with_flow:` block (lines 934–998) + update `MAPO_POS` in `write_mapoflow()` (lines 644–654) |

---

## Task 1: Replace `if with_flow:` block in `build_layout_svg()`

**Files:**
- Modify: `scripts/generate_outputs.py` lines 934–998

- [ ] **Step 1: Replace lines 934–998 with the new block**

In `scripts/generate_outputs.py`, find the `if with_flow:` block starting at line 934 and ending at line 998 (the last line before `parts.append("</svg>")`). Replace the entire block with:

```python
    if with_flow:
        MAPO_POS = {
            # Metal track — Setor Metal (x=0–13 m, y=0–8 m)
            1:  (11.5, 12.0),  # Recebimento
            2:  ( 7.5, 10.0),  # Estoque MP
            3:  ( 3.5,  8.3),  # boundary Metal
            4:  ( 2.5,  2.0),  # top-left Metal (laser)
            5:  ( 5.5,  2.0),  # top Metal — 4→5 horizontal
            6:  ( 8.5,  2.0),  # top-center (forno) — 5→6 horizontal
            7:  ( 8.5,  4.5),  # center Metal (espera) — 6→7 down
            8:  (11.0,  4.5),  # right Metal (politriz) — 7→8 horizontal
            9:  (11.0,  6.5),  # right-lower (afiador) — 8→9 down
            10: ( 9.5,  7.0),  # bottom Metal (armazenar semi)
            # Wood track — Setor Madeira (x=13–24 m, y=0–9 m)
            11: (14.0,  7.5),  # boundary Wood
            12: (15.0,  2.0),  # top-left Wood
            13: (19.0,  2.0),  # top-center — 12→13 horizontal
            14: (19.0,  5.0),  # below P13 — 13→14 straight down
            15: (22.0,  5.0),  # right of P14 — 14→15 horizontal
            16: (22.0,  7.0),  # below P15 — 15→16 straight down
            17: (21.0,  8.5),  # bottom-right (offset from P15/P16 column)
            # Assembly / shipping (x=13–24 m, y=9–16 m)
            18: (14.0,  9.5),  # entry Montagem
            19: (14.5, 11.5),  # Montagem left (rebitagem)
            20: (16.5, 11.5),  # INLINE next to P19 (insp. montagem) — was (2.5, 9.5)
            21: (18.5, 11.5),  # Montagem right — 19→20→21 horizontal
            22: (21.5, 11.0),  # Embalagem top (selar blister)
            23: (21.5, 12.5),  # INLINE below P22 (insp. embalado) — was (2.5, 11.5)
            24: (21.5, 14.0),  # Embalagem bottom — 22↓23↓24 down
            25: ( 7.5, 14.5),  # Est. Intermediário
            26: (11.5, 15.0),  # Recebimento (expedição)
        }
        PCOLORS = {
            "operacao": "#D9EAD3", "transporte": "#D9EAF7",
            "inspecao": "#FFF2CC", "armazenagem": "#EADCF8", "espera": "#F4CCCC",
        }
        procs_by_num = {p["number"]: p for p in results["processes"]}
        metal_set  = set(range(1, 11))
        wood_set   = {11, 12, 13, 14, 15, 16, 17}
        metal_color, wood_color, single_color = "#1e7a3c", "#a05000", "#17212b"

        # Pre-compute SVG pixel coordinates for each node
        svgx = {n: MARGIN + x * SCALE for n, (x, _) in MAPO_POS.items()}
        svgy = {n: 55     + y * SCALE for n, (_, y) in MAPO_POS.items()}

        # 4 edges routed as L-shaped polylines; all others are straight lines
        ELBOW_EDGES: dict[tuple[int, int], list[tuple[float, float]]] = {
            # 2→11: V-then-H — go UP first to avoid crossing Recebimento zone
            (2, 11):  [
                (svgx[2],  svgy[11]),   # same x as P2, same y as P11
                (svgx[11], svgy[11]),   # arrive at P11
            ],
            # 10→18: H-then-V — exit Metal rightward at zone boundary, then drop
            (10, 18): [
                (svgx[18], svgy[10]),   # same x as P18, same y as P10
                (svgx[18], svgy[18]),   # arrive at P18
            ],
            # 17→18: V-then-H — drop then go left (offset from P15/P16 column)
            (17, 18): [
                (svgx[17], svgy[18]),   # same x as P17, same y as P18
                (svgx[18], svgy[18]),   # arrive at P18
            ],
            # 24→25: V-H-V — route along bottom border below all zones
            (24, 25): [
                (svgx[24], 55 + 15.8 * SCALE),  # drop below layout flow
                (svgx[25], 55 + 15.8 * SCALE),  # travel left
                (svgx[25], svgy[25]),             # arrive at P25
            ],
        }

        flow_edges = (
            [(i, i + 1) for i in range(1, 10)] +
            [(2, 11)] + [(i, i + 1) for i in range(11, 17)] +
            [(10, 18), (17, 18)] +
            [(i, i + 1) for i in range(18, 26)]
        )

        # Draw edges FIRST (behind nodes)
        for (a, b) in flow_edges:
            if b in wood_set or (a == 2 and b == 11):
                color = wood_color
            elif a in metal_set and b in metal_set:
                color = metal_color
            else:
                color = single_color

            if (a, b) in ELBOW_EDGES:
                pts = (f"{svgx[a]:.1f},{svgy[a]:.1f} " +
                       " ".join(f"{wx:.1f},{wy:.1f}" for wx, wy in ELBOW_EDGES[(a, b)]))
                parts.append(
                    f'<polyline points="{pts}" fill="none" stroke="{color}" '
                    f'stroke-width="2.5" marker-end="url(#arr)" opacity="0.85"/>'
                )
            else:
                parts.append(
                    f'<line x1="{svgx[a]:.1f}" y1="{svgy[a]:.1f}" '
                    f'x2="{svgx[b]:.1f}" y2="{svgy[b]:.1f}" '
                    f'stroke="{color}" stroke-width="2.5" marker-end="url(#arr)" opacity="0.85"/>'
                )

        # Draw nodes ON TOP of edges
        for num, (mx_pos, my_pos) in MAPO_POS.items():
            px_ = MARGIN + mx_pos * SCALE
            py_ = 55     + my_pos * SCALE
            proc = procs_by_num[num]
            fill = PCOLORS.get(proc["type"], "#FFFFFF")
            stroke = (metal_color if num in metal_set
                      else wood_color if num in wood_set
                      else single_color)
            parts.append(
                f'<circle cx="{px_:.1f}" cy="{py_:.1f}" r="16" '
                f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
            )
            parts.append(
                f'<text x="{px_:.1f}" y="{py_ + 5:.1f}" text-anchor="middle" '
                f'font-size="11" font-weight="bold" fill="{stroke}">{num}</text>'
            )

        # Legend — bottom-right, clear of all nodes
        lx = SVG_W - 190
        ly = SVG_H - 102
        parts.append(
            f'<rect x="{lx - 5}" y="{ly - 5}" width="183" height="95" '
            f'fill="white" stroke="#ccc" stroke-width="1" rx="4"/>'
        )
        parts.append(
            f'<text x="{lx + 88}" y="{ly + 12}" text-anchor="middle" '
            f'font-size="11" font-weight="bold" fill="#333">Legenda</text>'
        )
        for li, (color, label) in enumerate([
            (metal_color,  "Trilha Metálica (1–10)"),
            (wood_color,   "Trilha Madeira (11–17)"),
            (single_color, "Montagem/Embalagem (18–26)"),
        ]):
            iy = ly + 32 + li * 22
            parts.append(
                f'<line x1="{lx}" y1="{iy}" x2="{lx + 22}" y2="{iy}" '
                f'stroke="{color}" stroke-width="3"/>'
            )
            parts.append(
                f'<text x="{lx + 30}" y="{iy + 4}" font-size="10" fill="#333">{label}</text>'
            )
```

- [ ] **Step 2: Run the generator to verify no Python errors**

```powershell
$Python = "C:\Users\dvill\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
Set-Location "C:\Users\dvill\Projeto_Fabrica_Tramontina_22399036"
& $Python scripts\generate_outputs.py
```

Expected: no exceptions, prints `Selected equipment qty: 2` or similar.

- [ ] **Step 3: Verify SVG updated and has polyline elements**

```powershell
(Get-Item "06_dashboard\renders\mapofluxograma_render.svg").LastWriteTime
Select-String -Path "06_dashboard\renders\mapofluxograma_render.svg" -Pattern "<polyline" | Measure-Object | Select-Object Count
```

Expected: modification time is recent (just now). Count = 4 (one polyline per elbow edge).

- [ ] **Step 4: Open mapofluxograma in browser and visually verify**

Open `06_dashboard\entregaveis\mapofluxograma.html` in a browser.

Check these specific things:
- Metal sector top row: nodes 4, 5, 6 are horizontally aligned
- Metal sector: 7→8 arrow is horizontal (not diagonal upward)
- Wood sector: 13↓14 is a straight vertical arrow downward
- Wood sector: 14→15 arrow is horizontal (not a long diagonal)
- 2→11 arrow goes UP then RIGHT (L-shape), not diagonally through Recebimento
- Nodes 20 and 23 are NOT in the far-left QC zone — they are inline with the production steps
- Legend is in the bottom-right corner, not overlapping any nodes

---

## Task 2: Update `write_mapoflow()` drawio MAPO_POS

**Files:**
- Modify: `scripts/generate_outputs.py` lines 644–654

- [ ] **Step 1: Replace the MAPO_POS dict in `write_mapoflow()`**

In `scripts/generate_outputs.py`, find the `MAPO_POS` dict inside `write_mapoflow()` (lines 644–654). Replace it with:

```python
    MAPO_POS = {
        # Metal track
        1:  (11.5, 12.0),  2:  ( 7.5, 10.0),  3:  ( 3.5,  8.3),
        4:  ( 2.5,  2.0),  5:  ( 5.5,  2.0),  6:  ( 8.5,  2.0),
        7:  ( 8.5,  4.5),  8:  (11.0,  4.5),  9:  (11.0,  6.5),
        10: ( 9.5,  7.0),
        # Wood track
        11: (14.0,  7.5),  12: (15.0,  2.0),  13: (19.0,  2.0),
        14: (19.0,  5.0),  15: (22.0,  5.0),  16: (22.0,  7.0),
        17: (21.0,  8.5),
        # Assembly / shipping
        18: (14.0,  9.5),  19: (14.5, 11.5),  20: (16.5, 11.5),
        21: (18.5, 11.5),  22: (21.5, 11.0),  23: (21.5, 12.5),
        24: (21.5, 14.0),  25: ( 7.5, 14.5),  26: (11.5, 15.0),
    }
```

- [ ] **Step 2: Run the generator again to verify no errors**

```powershell
$Python = "C:\Users\dvill\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
Set-Location "C:\Users\dvill\Projeto_Fabrica_Tramontina_22399036"
& $Python scripts\generate_outputs.py
```

Expected: clean run, no exceptions.

- [ ] **Step 3: Verify drawio file updated**

```powershell
(Get-Item "03_diagramas\mapofluxograma.drawio").LastWriteTime
Select-String -Path "03_diagramas\mapofluxograma.drawio" -Pattern 'id="mp20"' | Select-Object Line
```

Expected: recent timestamp. The mp20 cell position should now be around x=683 (≈ ORIGIN_X + 16.5*42 = 30 + 693 = 723 − half node) not near x=70 (old far-left QC position).

---

## Task 3: Full Regeneration, Verify, Commit, Push

**Files:**
- Run: `scripts/run_all.ps1`
- Commit + push

- [ ] **Step 1: Run full pipeline**

```powershell
Set-Location "C:\Users\dvill\Projeto_Fabrica_Tramontina_22399036"
.\scripts\run_all.ps1
```

Expected output:
```
[1/3] generate_outputs.py ...
[2/3] build_workbook.mjs ...
[3/3] build_latex.py ...
Done. Open 06_dashboard\index.html to review.
LaTeX ready at 07_latex\relatorio_tecnico.tex — upload to Overleaf (XeLaTeX).
```

- [ ] **Step 2: Check all 3 diagram renders updated**

```powershell
Get-Item "06_dashboard\renders\*.svg" | Select-Object Name, LastWriteTime, Length
```

Expected: all 3 SVG files have recent LastWriteTime.

- [ ] **Step 3: Visual spot-check — open mapofluxograma page**

Open `https://arranjo-red.vercel.app/06_dashboard/entregaveis/mapofluxograma.html` in a browser after deploy, or locally via `06_dashboard\entregaveis\mapofluxograma.html`.

Confirm no crossing arrows and the diagram is readable.

- [ ] **Step 4: Commit**

```powershell
git add scripts/generate_outputs.py 06_dashboard/renders/mapofluxograma_render.svg 03_diagramas/mapofluxograma.drawio data/resultados_calculo.json 06_dashboard/
git commit -m "fix: mapofluxograma — inline QC nodes, grid-pattern routing, elbow edges for zone crossings"
```

- [ ] **Step 5: Push to GitHub and redeploy to Vercel**

```powershell
git push
vercel --prod --yes 2>&1 | Select-String "Production:|Aliased:"
```

Expected: production URL printed. Vercel auto-deploys from push, or the explicit `vercel --prod` triggers it directly.

---

## Self-Review

**Spec coverage:**
- ✅ New MAPO_POS (26 nodes) — Task 1 Step 1
- ✅ Elbow routing for 4 edges (2→11, 10→18, 17→18, 24→25) — Task 1 Step 1 `ELBOW_EDGES`
- ✅ Draw order: edges first, nodes on top — Task 1 Step 1 (edges loop before nodes loop)
- ✅ Legend moved to bottom-right — Task 1 Step 1 (`lx = SVG_W - 190, ly = SVG_H - 102`)
- ✅ `write_mapoflow()` MAPO_POS updated — Task 2

**Placeholder scan:** None found. All coordinates are explicit numbers.

**Type consistency:** `MAPO_POS` is `dict[int, tuple[float, float]]` in both Task 1 and Task 2. `ELBOW_EDGES` is `dict[tuple[int,int], list[tuple[float,float]]]` — used only in Task 1. `svgx`/`svgy` are plain dicts computed from MAPO_POS — used only within the `if with_flow:` block. No cross-task type mismatches.
