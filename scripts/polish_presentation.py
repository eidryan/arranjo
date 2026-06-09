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
