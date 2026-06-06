"""
Build LaTeX report (abntex2) for Overleaf.

Usage:
    python scripts/build_latex.py

Outputs:
    07_latex/relatorio_tecnico.tex
    07_latex/referencias.bib
    07_latex/figuras/*.svg   (copies from 06_dashboard/renders/)

Compilation: Upload 07_latex/ to Overleaf. Set compiler to XeLaTeX.
"""
from __future__ import annotations
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "projeto.json"
RESULTS_PATH = ROOT / "data" / "resultados_calculo.json"
OUT_DIR = ROOT / "07_latex"
FIG_DIR = OUT_DIR / "figuras"


def load() -> tuple[dict, dict]:
    with DATA_PATH.open(encoding="utf-8") as f:
        project = json.load(f)
    with RESULTS_PATH.open(encoding="utf-8") as f:
        results = json.load(f)
    return project, results


def tex(s: str) -> str:
    """Escape special LaTeX characters."""
    return (s
        .replace("\\", "\\textbackslash{}")
        .replace("&",  "\\&")
        .replace("%",  "\\%")
        .replace("$",  "\\$")
        .replace("#",  "\\#")
        .replace("_",  "\\_")
        .replace("{",  "\\{")
        .replace("}",  "\\}")
        .replace("~",  "\\textasciitilde{}")
        .replace("^",  "\\textasciicircum{}")
    )


def members_block(project: dict) -> str:
    return " \\\\\n".join(
        tex(m["name"]) for m in project["metadata"].get("group_members", [])
    )


def bom_table(results: dict) -> str:
    rows = "".join(
        f"  {tex(r['component'])} & {r['quantity']} & {tex(r['unit'])} & {tex(r['make_or_buy'])} \\\\\n"
        for r in results["bom"]
    )
    return (
        "\\begin{table}[H]\n"
        "\\IBGEtab{\\caption{Tabela 1 --- Componentes, Quantidades e Fazer/Comprar}"
        "\\label{tab:bom}}{}\n"
        "\\begin{tabular}{p{8cm}ccc}\n"
        "\\toprule\n"
        "Componente & Qtd. & Unidade & Fazer/Comprar \\\\\n"
        "\\midrule\n"
        + rows +
        "\\bottomrule\n"
        "\\end{tabular}\n"
        "{\\legend{Fonte: elaborado pelos autores com base na composição oficial Tramontina SKU 22399036.}}\n"
        "\\end{table}\n"
    )


def process_table(results: dict) -> str:
    type_map = {
        "operacao": "Operação", "transporte": "Transporte",
        "inspecao": "Inspeção", "armazenagem": "Armazenagem", "espera": "Espera",
    }
    rows = "".join(
        f"  {p['number']} & {tex(p['name'])} & {type_map.get(p['type'], p['type'])} & {tex(p['resource'])} \\\\\n"
        for p in results["processes"]
    )
    return (
        "\\begin{longtable}{p{0.6cm}p{5.5cm}p{2.8cm}p{5.5cm}}\n"
        "\\caption{Tabela 2 --- Processos de Fabricação}\\label{tab:processos}\\\\\n"
        "\\toprule\n"
        "N° & Processo & Tipo & Recursos Físicos \\\\\n"
        "\\midrule\n"
        "\\endfirsthead\n"
        "\\multicolumn{4}{c}{\\tablename\\ \\thetable{} -- (continuação)}\\\\\n"
        "\\toprule N° & Processo & Tipo & Recursos Físicos \\\\\\midrule\n"
        "\\endhead\n"
        + rows +
        "\\bottomrule\n"
        "\\end{longtable}\n"
    )


def equipment_table(results: dict) -> str:
    rows = ""
    for eq in results["equipment_capacity"]:
        dims = eq.get("dimensions_m", {})
        dim_str = f"{dims.get('length','?')}×{dims.get('width','?')}×{dims.get('height','?')} m"
        rows += (
            f"  {tex(eq['type'])} & {tex(eq['supplier'])} & {tex(eq['model'])} & "
            f"{tex(dim_str)} & {tex(eq['official_capacity'])} \\\\\n"
        )
    return (
        "\\begin{longtable}{p{3.5cm}p{2.5cm}p{2.5cm}p{2.8cm}p{3.0cm}}\n"
        "\\caption{Tabela 3 --- Equipamentos Selecionados}\\label{tab:equipamentos}\\\\\n"
        "\\toprule\n"
        "Tipo & Fornecedor & Modelo & Dimensões & Cap. Fabricante \\\\\n"
        "\\midrule\n"
        "\\endfirsthead\n"
        "\\multicolumn{5}{c}{\\tablename\\ \\thetable{} -- (continuação)}\\\\\n"
        "\\toprule Tipo & Fornecedor & Modelo & Dimensões & Cap. \\\\\\midrule\n"
        "\\endhead\n"
        + rows +
        "\\bottomrule\n"
        "\\end{longtable}\n"
    )


def demand_table(results: dict) -> str:
    d = results["demand"]
    p = results["premises"]
    rows = (
        f"  Meta semanal de kits bons & {d['target_good_kits_per_week']:.0f} kits/semana \\\\\n"
        f"  Rendimento final assumido & {d['final_good_yield']:.0%} \\\\\n"
        f"  Demanda bruta calculada & {d['input_kits_per_week']:.0f} kits/semana \\\\\n"
        f"  Jornada de trabalho & {p['work_days_per_week']} dias × {p['shifts_per_day']} turno × {p['useful_hours_per_shift']} h úteis \\\\\n"
        f"  Horas úteis semanais & {d['useful_hours_per_week']:.1f} h/semana \\\\\n"
        f"  Ritmo médio necessário & {d['required_average_rate_kits_per_hour']:.2f} kits/h \\\\\n"
        f"  Eficiência geral & {p['general_efficiency']:.0%} \\\\\n"
        f"  Confiabilidade & {p['equipment_reliability']:.0%} \\\\\n"
    )
    return (
        "\\begin{table}[H]\n"
        "\\IBGEtab{\\caption{Quadro Resumo --- Meta e Premissas de Produção}\\label{tab:meta}}{}\n"
        "\\begin{tabular}{ll}\n"
        "\\toprule\n"
        "Premissa & Valor \\\\\n"
        "\\midrule\n"
        + rows +
        "\\bottomrule\n"
        "\\end{tabular}\n"
        "{\\legend{Fonte: elaborado pelos autores.}}\n"
        "\\end{table}\n"
    )


def selected_eq_section(results: dict) -> str:
    s = results["selected_equipment_detail"]
    rows = (
        f"  Tempo padrão por kit & {s['standard_time_seconds_per_kit']:.0f} s/kit \\\\\n"
        f"  Taxa nominal & 3600 / {s['standard_time_seconds_per_kit']:.0f} = {s['nominal_rate_from_standard_time']:.2f} kits/h \\\\\n"
        f"  Eficiência geral & {s['efficiency']:.0%} \\\\\n"
        f"  Confiabilidade & {s['reliability']:.0%} \\\\\n"
        f"  Rendimento do processo & {s['process_yield']:.0%} \\\\\n"
        f"  Taxa efetiva & {s['effective_rate_kits_per_hour']:.2f} kits/h \\\\\n"
        f"  Capacidade semanal/máquina & {s['weekly_capacity_per_machine']:.2f} kits/semana \\\\\n"
        f"  Demanda bruta semanal & {s['demand_input_kits_per_week']:.0f} kits/semana \\\\\n"
        f"  Quantidade necessária & $\\lceil {s['demand_input_kits_per_week']:.0f} / {s['weekly_capacity_per_machine']:.2f} \\rceil = {s['required_quantity']}$ \\\\\n"
        f"  Utilização estimada & {s['utilization']:.1%} \\\\\n"
    )
    return (
        f"O equipamento selecionado é \\textbf{{{tex(s['equipment_type'])}}} --- "
        f"{tex(s['supplier'])} {tex(s['model'])}.\n\n"
        f"\\textbf{{Motivo:}} {tex(s['reason'])}\n\n"
        f"\\textbf{{Operação(ões):}} {tex(', '.join(s['operations']))}\n\n"
        "\\begin{table}[H]\n"
        "\\IBGEtab{\\caption{Memória de Cálculo --- Router CNC Maksiwa RTC.1313}\\label{tab:calc}}{}\n"
        "\\begin{tabular}{ll}\n"
        "\\toprule\n"
        "Parâmetro & Valor \\\\\n"
        "\\midrule\n"
        + rows +
        "\\bottomrule\n"
        "\\end{tabular}\n"
        "{\\legend{Fonte: fabricante (Maksiwa Store) e premissas de engenharia. "
        "Fórmula: $N = \\lceil D / (T \\times H \\times E \\times C \\times R) \\rceil$.}}\n"
        "\\end{table}\n"
    )


def build_bib(project: dict) -> str:
    entries = []
    for src in project.get("sources", []):
        bib_id = src["id"].replace("-", "_")
        title = src.get("title", src["id"])
        url = src.get("url", "")
        note = f"Acesso em: {project['metadata']['access_date']}." if url.startswith("http") else ""
        howpub = f"\\url{{{url}}}" if url.startswith("http") else url
        entries.append(
            f"@misc{{{bib_id},\n"
            f"  title  = {{{{{title}}}}},\n"
            f"  howpublished = {{{howpub}}},\n"
            f"  note   = {{{note}}},\n"
            f"}}"
        )
    return "\n\n".join(entries)


def build_tex(project: dict, results: dict) -> str:
    d = results["demand"]
    layout = results["layout"]
    c = project.get("conclusions", {})
    objectives = "\n".join(f"  \\item {tex(o)}" for o in project.get("project_objectives", []))
    segments_body = "".join(
        f"\\textbf{{{tex(seg['name'])}}} --- {tex(seg['description'])} "
        f"{tex(seg['justification'])}\n\n"
        for seg in project.get("market_segments", [])
    )
    improvements = "\n".join(f"  \\item {tex(imp)}" for imp in c.get("improvements", []))

    return (
        "% =====================================================\n"
        "% Relatório Técnico — Projeto de Fábrica\n"
        "% Kit para Churrasco Tramontina 22399036 — UFF Niterói\n"
        "% Gerado por scripts/build_latex.py — NÃO EDITAR\n"
        "% Compilar no Overleaf com XeLaTeX\n"
        "% =====================================================\n"
        "\\documentclass[12pt,a4paper,oneside,english,brazil]{abntex2}\n\n"
        "\\usepackage[utf8]{inputenc}\n"
        "\\usepackage[T1]{fontenc}\n"
        "\\usepackage{lmodern}\n"
        "\\usepackage{graphicx}\n"
        "\\usepackage{booktabs}\n"
        "\\usepackage{longtable}\n"
        "\\usepackage{float}\n"
        "\\usepackage{microtype}\n"
        "\\usepackage{url}\n"
        "\\usepackage{svg}\n"
        "\\usepackage{amsmath}\n\n"
        f"\\titulo{{Projeto de Fábrica --- {tex(project['product']['name'])}}}\n"
        f"\\autor{{{members_block(project)}}}\n"
        "\\local{Niterói, RJ}\n"
        "\\data{\\the\\year}\n"
        "\\instituicao{Universidade Federal Fluminense (UFF)}\n\n"
        "\\begin{document}\n\n"
        "\\imprimircapa\n\n"
        "\\pdfbookmark[0]{\\contentsname}{toc}\n"
        "\\tableofcontents*\n"
        "\\clearpage\n\n"
        "\\chapter{Objetivos do Projeto}\n"
        "\\begin{itemize}\n"
        f"{objectives}\n"
        "\\end{itemize}\n\n"
        "\\chapter{Descrição do Produto}\n"
        f"O produto a ser fabricado é o \\textbf{{{tex(project['product']['name'])}}}, "
        f"referência \\textbf{{{tex(project['product']['sku'])}}}, composto por faca chef 8 polegadas, "
        "garfo trinchante e tábua retangular de madeira Maçaranduba.\n\n"
        "\\begin{figure}[H]\n"
        "  \\centering\n"
        "  \\includesvg[width=0.5\\textwidth]{figuras/fluxograma_render}\n"
        "  \\caption{Produto principal --- Kit Churrasco Tramontina 22399036}\n"
        "  \\legend{Fonte: Tramontina.}\n"
        "\\end{figure}\n\n"
        f"Dimensões da embalagem: {project['product']['package_dimensions_cm']['height']} cm × "
        f"{project['product']['package_dimensions_cm']['length']} cm × "
        f"{project['product']['package_dimensions_cm']['width']} cm. "
        f"Peso: {project['product']['package_weight_kg']} kg.\n\n"
        "\\chapter{Estrutura do Produto (Itens Pais e Filhos)}\n"
        "O kit embalado (item pai) é composto pelos seguintes itens filhos:\n"
        "\\begin{itemize}\n"
        + "".join(f"  \\item {tex(r['component'])} ({tex(r['make_or_buy'])})\n" for r in results["bom"]) +
        "\\end{itemize}\n\n"
        "\\chapter{Segmentos de Mercado}\n"
        f"{segments_body}\n"
        "\\chapter{Meta Semanal de Produção}\n"
        f"A meta estabelecida é de \\textbf{{{d['target_good_kits_per_week']:.0f} kits bons por semana}}.\n\n"
        + demand_table(results) + "\n"
        "\\chapter{Tabela 1 --- Componentes, Quantidades e Fazer/Comprar}\n"
        + bom_table(results) + "\n"
        "\\chapter{Tabela 2 --- Processos de Fabricação}\n"
        "O processo produtivo é dividido em 26 etapas distribuídas em trilha metálica (1--10), "
        "trilha madeira (2 e 11--17) e montagem/embalagem (18--26).\n\n"
        + process_table(results) + "\n"
        "\\chapter{Fluxograma do Processo}\n"
        "\\begin{figure}[H]\n"
        "  \\centering\n"
        "  \\includesvg[width=\\textwidth]{figuras/fluxograma_render}\n"
        "  \\caption{Fluxograma --- símbolos ASME, duas trilhas paralelas}\n"
        "  \\legend{Fonte: elaborado pelos autores.}\n"
        "\\end{figure}\n\n"
        "\\chapter{Tabela 3 --- Equipamentos Selecionados}\n"
        + equipment_table(results) + "\n"
        "\\chapter{Cálculo do Equipamento Selecionado}\n"
        + selected_eq_section(results) + "\n"
        "\\chapter{Arranjo Físico Esquemático}\n"
        f"A fábrica proposta ocupa {layout['layout_dimensions_m']['length']} m × "
        f"{layout['layout_dimensions_m']['width']} m = {layout['layout_total_area_m2']:.0f} m². "
        f"Área requerida: {layout['total_required_area_m2']:.1f} m². "
        f"Ocupação: {layout['occupancy']*100:.1f}\\%.\n\n"
        "\\begin{figure}[H]\n"
        "  \\centering\n"
        "  \\includesvg[width=\\textwidth]{figuras/layout_render}\n"
        "  \\caption{Arranjo físico --- equipamentos e zonas funcionais}\n"
        "  \\legend{Fonte: elaborado pelos autores.}\n"
        "\\end{figure}\n\n"
        "\\chapter{Mapofluxograma}\n"
        "\\begin{figure}[H]\n"
        "  \\centering\n"
        "  \\includesvg[width=\\textwidth]{figuras/mapofluxograma_render}\n"
        "  \\caption{Mapofluxograma --- 26 processos sobre o arranjo físico}\n"
        "  \\legend{Fonte: elaborado pelos autores.}\n"
        "\\end{figure}\n\n"
        "\\chapter{Conclusões}\n"
        f"{tex(c.get('summary', ''))}\n\n"
        f"\\textbf{{Gargalo:}} {tex(c.get('bottleneck_note', ''))}\n\n"
        f"\\textbf{{Layout:}} {tex(c.get('layout_note', ''))}\n\n"
        "\\textbf{O que seria necessário para aprimorar o projeto:}\n"
        "\\begin{itemize}\n"
        f"{improvements}\n"
        "\\end{itemize}\n\n"
        "\\bibliography{referencias}\n\n"
        "\\end{document}\n"
    )


def main() -> None:
    project, results = load()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    renders_dir = ROOT / "06_dashboard" / "renders"
    for svg_file in renders_dir.glob("*.svg"):
        shutil.copy2(svg_file, FIG_DIR / svg_file.name)
        print(f"  Copied {svg_file.name} -> 07_latex/figuras/")

    tex_content = build_tex(project, results)
    (OUT_DIR / "relatorio_tecnico.tex").write_text(tex_content, encoding="utf-8")
    print("  Written: 07_latex/relatorio_tecnico.tex")

    bib_content = build_bib(project)
    (OUT_DIR / "referencias.bib").write_text(bib_content, encoding="utf-8")
    print("  Written: 07_latex/referencias.bib")

    print()
    print("LaTeX package ready.")
    print("Upload 07_latex/ to Overleaf. Set compiler: XeLaTeX.")


if __name__ == "__main__":
    main()
