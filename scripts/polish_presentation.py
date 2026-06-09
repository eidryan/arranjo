# polish_presentation.py -- Polishes the group's PPTX with renders and data corrections.
#
# Input:  C:/Users/dvill/Downloads/Projeto de Fabrica - Kit Churrasco Tramontina (1).pptx
# Output: 01_apresentacao/apresentacao_final.pptx


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
            page.goto(svg.as_uri(), wait_until="networkidle")
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
    fluxo_svg = RENDERS / "fluxograma_render.svg"
    if not fluxo_svg.exists():
        raise FileNotFoundError(f"Missing render: {fluxo_svg}")
    _svg_to_png(fluxo_svg, full, width=1800, height=1000)
    pngs["fluxo_top"] = tmp / "fluxo_top.png"
    pngs["fluxo_bot"] = tmp / "fluxo_bot.png"
    _split_png(full, pngs["fluxo_top"], pngs["fluxo_bot"])
    for name in ("layout_render", "mapofluxograma_render"):
        print(f"  {name}.svg -> PNG ...")
        svg_path = RENDERS / f"{name}.svg"
        if not svg_path.exists():
            raise FileNotFoundError(f"Missing render: {svg_path}")
        png = tmp / f"{name}.png"
        _svg_to_png(svg_path, png)
        pngs[name] = png
    return pngs


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


def _insert_fluxograma_slides(prs, pngs: dict):
    """Insert 2 fluxograma slides after index 10 ('PAIS E FILHOS')."""
    _add_img_slide(prs, 11, "Fluxograma do Processo (1/2)", pngs["fluxo_top"])
    _add_img_slide(prs, 12, "Fluxograma do Processo (2/2)", pngs["fluxo_bot"])


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
