# Polish Presentation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create `polish_presentation.py` that opens the group's PPTX, inserts rendered diagram slides, fills the empty layout/mapofluxograma slides, corrects inconsistent data values, and standardizes font minimums.

**Architecture:** Single script, five sequential operations: render SVGs → PNG, insert 2 fluxograma slides at index 11, fill existing diagram slides by title search, text fix via run+paragraph pass, font floor. Reuses `_svg_to_png` pattern from `build_presentation.py`. Source file is never modified — output goes to `01_apresentacao/apresentacao_final.pptx`.

**Tech Stack:** python-pptx, Pillow, Playwright (Edge)

---

## Slide index map (source file, 0-based)

| Index | Title |
|---|---|
| 10 | PAIS E FILHOS ← insert fluxograma after this |
| 14 | DESENHO ESQUEMÁTICO DO ARRANJO FÍSICO ← fill with layout PNG |
| 15 | MAPOFLUXOGRAMA DA PRODUÇÃO ← fill with mapo PNG |
| 07 | 2.000 (meta slide) ← text fix |
| 17 | SELEÇÃO DE 1 EQUIPAMENTO (table) ← text fix |
| 19 | SELEÇÃO DE 1 EQUIPAMENTO (calc) ← text fix |
| 22 | MEMORIAL DE CÁLCULO / Dimensionamento ← text fix |

After inserting 2 slides at index 11, the layout and mapofluxograma slides shift to indices 16 and 17. **Always find them by title text, not hardcoded index.**

---

### Task 1: Script skeleton + SVG → PNG pipeline

**Files:**
- Create: `scripts/polish_presentation.py`

- [ ] **Step 1: Create the script**

```python
"""
polish_presentation.py — Polishes the group's PPTX with renders and data corrections.

Input:  C:\Users\dvill\Downloads\Projeto de Fábrica - Kit Churrasco Tramontina (1).pptx
Output: 01_apresentacao\apresentacao_final.pptx
"""

import tempfile
from pathlib import Path
from PIL import Image

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

ROOT    = Path(__file__).parent.parent
RENDERS = ROOT / "06_dashboard" / "renders"
OUT_DIR = ROOT / "01_apresentacao"
SOURCE  = Path(r"C:\Users\dvill\Downloads") / "Projeto de Fábrica - Kit Churrasco Tramontina (1).pptx"

W = 10.0
H = 5.625


def _svg_to_png(svg: Path, png: Path, width=1800, height=1000):
    from playwright.sync_api import sync_playwright
    edge = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
    kwargs = {"headless": True}
    if edge.exists():
        kwargs["executable_path"] = str(edge)
    with sync_playwright() as p:
        browser = p.chromium.launch(**kwargs)
        try:
            page = browser.new_page(viewport={"width": width, "height": height})
            page.goto("file:///" + str(svg).replace("\\", "/"), wait_until="load")
            page.screenshot(path=str(png))
        finally:
            browser.close()


def _split_png(src: Path, top: Path, bot: Path):
    """Split PNG: top covers 0–60%, bottom covers 40–100% (20% overlap)."""
    img = Image.open(str(src))
    w, h = img.size
    img.crop((0, 0,            w, int(h * 0.60))).save(str(top))
    img.crop((0, int(h * 0.40), w, h           )).save(str(bot))


def _render_pngs(tmp: Path) -> dict:
    pngs = {}
    print("  fluxograma_render.svg -> PNG ...")
    full = tmp / "fluxo_full.png"
    _svg_to_png(RENDERS / "fluxograma_render.svg", full, width=1800, height=1000)
    pngs["fluxo_top"] = tmp / "fluxo_top.png"
    pngs["fluxo_bot"] = tmp / "fluxo_bot.png"
    _split_png(full, pngs["fluxo_top"], pngs["fluxo_bot"])
    for name in ("layout_render", "mapofluxograma_render"):
        print(f"  {name}.svg -> PNG ...")
        png = tmp / f"{name}.png"
        _svg_to_png(RENDERS / f"{name}.svg", png)
        pngs[name] = png
    return pngs


def main():
    print("Rendering SVGs to PNG...")
    with tempfile.TemporaryDirectory() as tmp:
        pngs = _render_pngs(Path(tmp))
        for k, v in pngs.items():
            print(f"  {k}: {v.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run — verify 4 PNGs are created**

```powershell
cd C:\Users\dvill\Projeto_Fabrica_Tramontina_22399036
python scripts\polish_presentation.py
```

Expected: 4 lines printed (fluxo_top, fluxo_bot, layout_render, mapofluxograma_render), all > 0 KB.

---

### Task 2: Insert fluxograma slides

**Files:**
- Modify: `scripts/polish_presentation.py`

- [ ] **Step 1: Add `_add_img_slide` helper**

Add after `_render_pngs`:

```python
def _add_img_slide(prs, idx: int, title: str, img_path: Path):
    """Insert a new blank slide with a full-width image at 0-based position idx."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank, added at end

    # Move from end to target idx
    lst = prs.slides._sldIdLst
    ref = lst[-1]
    lst.remove(ref)
    lst.insert(idx, ref)

    # Dark title bar at bottom
    bar_h = 0.40
    bar = slide.shapes.add_shape(
        1, Inches(0), Inches(H - bar_h), Inches(W), Inches(bar_h)
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = RGBColor(0x17, 0x21, 0x2b)
    bar.line.fill.background()

    tb = slide.shapes.add_textbox(Inches(0), Inches(H - bar_h), Inches(W), Inches(bar_h))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = title
    run.font.size = Pt(15)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0xff, 0xff, 0xff)

    # Image fills area above bar
    slide.shapes.add_picture(
        str(img_path), Inches(0), Inches(0), Inches(W), Inches(H - bar_h - 0.02)
    )
    return slide
```

- [ ] **Step 2: Add `_insert_fluxograma_slides` and call it in `main`**

Add after `_add_img_slide`:

```python
def _insert_fluxograma_slides(prs, pngs: dict):
    """Insert 2 fluxograma slides after index 10 ('PAIS E FILHOS')."""
    _add_img_slide(prs, 11, "Fluxograma do Processo (1/2)", pngs["fluxo_top"])
    _add_img_slide(prs, 12, "Fluxograma do Processo (2/2)", pngs["fluxo_bot"])
```

Replace `main()`:

```python
def main():
    print("Rendering SVGs to PNG...")
    with tempfile.TemporaryDirectory() as tmp:
        pngs = _render_pngs(Path(tmp))

        print("Loading source PPTX...")
        prs = Presentation(str(SOURCE))
        print(f"  Slides before: {len(prs.slides)}")

        print("Inserting fluxograma slides...")
        _insert_fluxograma_slides(prs, pngs)
        print(f"  Slides after: {len(prs.slides)}")

        OUT_DIR.mkdir(exist_ok=True)
        out = OUT_DIR / "apresentacao_final.pptx"
        prs.save(str(out))
        print(f"Saved -> {out}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Run — verify slide count**

```powershell
python scripts\polish_presentation.py
```

Expected: `Slides before: 26` and `Slides after: 28`.

---

### Task 3: Fill layout and mapofluxograma slides

**Files:**
- Modify: `scripts/polish_presentation.py`

- [ ] **Step 1: Add `_fill_existing_slide` and `_fill_diagram_slides`**

Add after `_insert_fluxograma_slides`:

```python
def _fill_existing_slide(slide, img_path: Path):
    """Add image below the lowest existing shape on the slide."""
    lowest_emu = 0
    for shape in slide.shapes:
        bottom = shape.top + shape.height
        if bottom > lowest_emu:
            lowest_emu = bottom
    top_in = max(lowest_emu / 914400 + 0.08, 0.75)
    slide.shapes.add_picture(
        str(img_path),
        Inches(0.1), Inches(top_in),
        Inches(W - 0.2), Inches(H - top_in - 0.08)
    )


def _fill_diagram_slides(prs, pngs: dict):
    """Find diagram placeholder slides by title keyword and add renders."""
    targets = {
        "ESQUEMÁTICO": pngs["layout_render"],
        "MAPOFLUXOGRAMA": pngs["mapofluxograma_render"],
    }
    for slide in prs.slides:
        # Skip if already has a picture shape
        if any(s.shape_type == 13 for s in slide.shapes):
            continue
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            text = shape.text_frame.text.upper()
            for keyword, img_path in targets.items():
                if keyword in text:
                    print(f"  Filling: {shape.text_frame.text.strip()[:50]}")
                    _fill_existing_slide(slide, img_path)
                    break
```

Update `main()` — add call after `_insert_fluxograma_slides`:

```python
        print("Filling diagram slides...")
        _fill_diagram_slides(prs, pngs)
```

- [ ] **Step 2: Run — verify two fills are logged**

```powershell
python scripts\polish_presentation.py
```

Expected output includes two `Filling:` lines — one for ESQUEMÁTICO, one for MAPOFLUXOGRAMA.

---

### Task 4: Text corrections

**Files:**
- Modify: `scripts/polish_presentation.py`

- [ ] **Step 1: Add replacement table and `_fix_texts`**

Add after `_fill_diagram_slides`:

```python
# Longer/more-specific strings first to avoid partial-match shadowing
TEXT_FIXES = [
    # Meta — production target
    ("5.000 kits semanais",        "1.000 kits semanais"),
    ("5.000 kits por semana",      "1.000 kits por semana"),
    ("2.000 kits por semana",      "1.000 kits por semana"),
    ("Calcular a carga de máquinas e layout para atender à meta de 5.000 kits semanais.",
     "Calcular a carga de máquinas e layout para atender à meta de 1.000 kits semanais."),
    ("meta de 2.000 unidades/semana (400/dia + rejeitos)",
     "meta de 1.000 kits/semana (200/dia + rejeitos)"),
    ("Cálculo da quantidade de prensas para meta de 2.000 unidades/semana (400/dia + rejeitos).",
     "Cálculo da quantidade de lasers para meta de 1.000 kits/semana (200/dia + rejeitos)."),
    ("2.000",                      "1.000"),
    ("400 kits / dia",             "200 kits / dia"),
    ("400 kits/dia",               "200 kits/dia"),
    ("Capacidade Diária: 400 kits.", "Capacidade Diária: 200 kits."),
    ("400 / 8 = 50",               "200 / 8 = 25"),
    ("2000 kits / 5 dias = 400 kits / dia",
     "1000 kits / 5 dias = 200 kits / dia"),
    ("50 / 0,85 x 0,97 = 60,7 kits / hora",
     "25 / 0,85 x 0,97 = 30,3 kits / hora"),
    ("50 kits / hora",             "30 kits / hora"),
    ("60,7 kits / hora",           "30,3 kits / hora"),
    # Layout
    ("800m²",                      "384 m²"),
    ("800 m²",                     "384 m²"),
    ("40m x 20m",                  "24 × 16 m"),
    ("40 × 20",                    "24 × 16"),
    ("Planta dimensionada em 800m² (40m x 20m) focada em fluxo linear para minimizar movimentação de materiais.",
     "Planta dimensionada em 384 m² (24 × 16 m) com arranjo misto: setores funcionais para metal/madeira e linha para montagem/embalagem."),
    # Material
    ("350 x 220 x 18 mm",         "340 x 190 x 15 mm"),
    ("Madeira Certificada (Eucalipto/Pinus)", "Madeira Maçaranduba"),
    ("Eucalipto/Pinus",            "Maçaranduba"),
    # Equipment — specific phrases before generic
    ("A Prensa Excêntrica foi dimensionada para as operações de corte e estampagem dos componentes metálicos. Considerando a demanda de",
     "O Laser Fibra CNC foi dimensionado para o corte dos blanks de faca e garfo em chapa AISI 420. Considerando a demanda de"),
    ("1 Prensa Excêntrica é suficiente para a demanda, operando com uma folga de capacidade de 70%.",
     "1 Laser Fibra CNC é suficiente para a demanda, operando com utilização de 49%."),
    ("Resultado Final",            "Resultado Final"),   # no-op anchor — keep
    ("Harlo do Brasil\n(Guarulhos-SP)\nRHTC / ProfiPress", "Madetech (SP)"),
    ("Harlo do Brasil",            "Madetech (SP)"),
    ("60 golpes/min",              "20.000 mm/min"),
    ("60 tf",                      "1.500 W"),
    ("Prensa\nExcêntrica",         "Laser Fibra CNC"),
    ("Prensa Excêntrica",          "Laser Fibra CNC"),
    ("prensas para",               "lasers para"),
    ("quantidade de prensas",      "quantidade de lasers"),
    ("1 prensa",                   "1 laser"),
    ("da prensa",                  "do laser"),
    # Calculation numbers (equipment selection slide)
    ("N = 60,7 /3600 = 0,017 ≈ 1 prensa",  "N = 30,3 / 80 = 0,38 ≈ 1 laser"),
    ("N = 412,37 / 1360 = 0,3 -> 1 prensa", "N = 206,2 / 437 = 0,47 → 1 laser"),
    ("Db = 400 / 0,97 = 412,37 kits/dia",   "Db = 200 / 0,97 = 206,2 kits/dia"),
    ("Capacidade = 367,2 / 0,27 = 1360 kits / dia",
     "Capacidade = 80 × 7 × 0,85 × 0,92 = 437 kits/dia"),
    ("Capacidade da prensa:  60 golpes / min = 3600 ciclos / hora",
     "Capacidade do laser: 20.000 mm/min → ~80 kits/hora"),
    ("Produção necessária com perdas :\n50 / 0,85 x 0,97 = 60,7 kits / hora",
     "Produção necessária com perdas:\n25 / 0,85 × 0,97 = 30,3 kits / hora"),
    ("Produção necessária:\n2000 kits / 5 dias = 400 kits / dia\n400 / 8 = 50 kits / hora",
     "Produção necessária:\n1000 kits / 5 dias = 200 kits / dia\n200 / 8 = 25 kits / hora"),
]


def _replace_in_para(para, fixes):
    """Two-pass replacement: run-level first, then paragraph-level for split runs."""
    for run in para.runs:
        for old, new in fixes:
            if old in run.text:
                run.text = run.text.replace(old, new)
    # Paragraph-level pass catches strings split across runs
    full = "".join(r.text for r in para.runs)
    for old, new in fixes:
        if old in full:
            full = full.replace(old, new)
            if para.runs:
                para.runs[0].text = full
                for r in para.runs[1:]:
                    r.text = ""
            break


def _fix_texts(prs):
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    _replace_in_para(para, TEXT_FIXES)
            if hasattr(shape, "table"):
                for row in shape.table.rows:
                    for cell in row.cells:
                        for para in cell.text_frame.paragraphs:
                            _replace_in_para(para, TEXT_FIXES)
```

Update `main()`:

```python
        print("Applying text corrections...")
        _fix_texts(prs)
```

- [ ] **Step 2: Run and verify no bad strings remain**

```powershell
python scripts\polish_presentation.py
```

Then spot-check:

```powershell
python << 'EOF'
from pptx import Presentation
from pathlib import Path
prs = Presentation(r"C:\Users\dvill\Projeto_Fabrica_Tramontina_22399036\01_apresentacao\apresentacao_final.pptx")
bad = ["Eucalipto", "800m", "800 m", "40m x 20m", "Prensa Exc", "2.000\n", "5.000 kits"]
found = []
for i, slide in enumerate(prs.slides):
    for shape in slide.shapes:
        t = ""
        if shape.has_text_frame:
            t = shape.text_frame.text
        elif hasattr(shape, "table"):
            t = " ".join(c.text for r in shape.table.rows for c in r.cells)
        for b in bad:
            if b in t:
                found.append(f"slide {i+1}: {b!r}")
print("Issues:", found or "none")
EOF
```

Expected: `Issues: none`

---

### Task 5: Font normalization + final save

**Files:**
- Modify: `scripts/polish_presentation.py`

- [ ] **Step 1: Add `_normalize_fonts`**

Add after `_fix_texts`:

```python
def _normalize_fonts(prs):
    """Raise font sizes that fall below readability minimums. Never reduces."""
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    for run in para.runs:
                        if run.font.size and run.font.size < Pt(12):
                            run.font.size = Pt(12)
            if hasattr(shape, "table"):
                for row in shape.table.rows:
                    for cell in row.cells:
                        for para in cell.text_frame.paragraphs:
                            for run in para.runs:
                                if run.font.size and run.font.size < Pt(9):
                                    run.font.size = Pt(9)
```

- [ ] **Step 2: Replace `main()` with the final version**

```python
def main():
    print("Rendering SVGs to PNG...")
    with tempfile.TemporaryDirectory() as tmp:
        pngs = _render_pngs(Path(tmp))

        print("Loading source PPTX...")
        prs = Presentation(str(SOURCE))
        print(f"  Slides: {len(prs.slides)}")

        print("Inserting fluxograma slides...")
        _insert_fluxograma_slides(prs, pngs)

        print("Filling diagram slides...")
        _fill_diagram_slides(prs, pngs)

        print("Applying text corrections...")
        _fix_texts(prs)

        print("Normalizing fonts...")
        _normalize_fonts(prs)

        OUT_DIR.mkdir(exist_ok=True)
        out = OUT_DIR / "apresentacao_final.pptx"
        prs.save(str(out))
        print(f"\nPronto -> {out}  ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Full run**

```powershell
python scripts\polish_presentation.py
```

Expected: no errors, file printed with size > 1000 KB.

- [ ] **Step 4: Open and verify**

```powershell
Start-Process "C:\Users\dvill\Projeto_Fabrica_Tramontina_22399036\01_apresentacao\apresentacao_final.pptx"
```

Check manually:
- Total slides: 28
- Slides 12–13: fluxograma images (two halves)
- Slide with "ESQUEMÁTICO" in title: has layout render image
- Slide with "MAPOFLUXOGRAMA" in title: has mapo render image
- Slide 8 (meta): shows "1.000" not "2.000"
- Equipment selection slides: show "Laser Fibra CNC" not "Prensa Excêntrica"
- Layout slide: shows "384 m²" not "800 m²"

---

### Task 6: Wire into run_all.ps1 + commit

**Files:**
- Modify: `scripts/run_all.ps1`

- [ ] **Step 1: Update run_all.ps1**

In `scripts/run_all.ps1`, replace:

```powershell
  Write-Host "[4/4] build_presentation.py ..."
  & $Python (Join-Path $Root "scripts\build_presentation.py")
  Write-Host ""
  Write-Host "Done. Open 06_dashboard\index.html to review."
  Write-Host "LaTeX ready at 07_latex\relatorio_tecnico.tex — upload to Overleaf (XeLaTeX)."
  Write-Host "PPTX pronto em 01_apresentacao\apresentacao_tramontina_22399036.pptx"
```

With:

```powershell
  Write-Host "[4/5] build_presentation.py ..."
  & $Python (Join-Path $Root "scripts\build_presentation.py")
  Write-Host "[5/5] polish_presentation.py ..."
  & $Python (Join-Path $Root "scripts\polish_presentation.py")
  Write-Host ""
  Write-Host "Done. Open 06_dashboard\index.html to review."
  Write-Host "LaTeX ready at 07_latex\relatorio_tecnico.tex — upload to Overleaf (XeLaTeX)."
  Write-Host "PPTX final em 01_apresentacao\apresentacao_final.pptx"
```

- [ ] **Step 2: Commit**

```bash
git add scripts/polish_presentation.py scripts/run_all.ps1 01_apresentacao/apresentacao_final.pptx
git commit -m "feat: add polish_presentation.py — inserts renders and corrects data in group PPTX"
```

---

## Self-review

**Spec coverage:**
- SVG → PNG + fluxograma split ✅ Task 1
- Insert 2 fluxograma slides at index 11 ✅ Task 2
- Fill ESQUEMÁTICO slide with layout PNG ✅ Task 3
- Fill MAPOFLUXOGRAMA slide with mapo PNG ✅ Task 3
- All text fixes from spec table ✅ Task 4
- Font floor normalization ✅ Task 5
- Add to run_all.ps1 as step 5/5 ✅ Task 6
- Save to `apresentacao_final.pptx` ✅ Task 5

**No TBDs, no placeholder code.**

**Type consistency:** `pngs` dict keys (`fluxo_top`, `fluxo_bot`, `layout_render`, `mapofluxograma_render`) consistent across Tasks 1–3. `_add_img_slide(prs, idx, title, img_path)` signature used consistently. `shape_type == 13` used correctly to detect picture shapes.
