from __future__ import annotations

import json
import math
from datetime import datetime
from html import escape
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape as xml_escape


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "projeto.json"
RESULTS_PATH = ROOT / "data" / "resultados_calculo.json"


PROCESS_COLORS = {
    "operacao": "#D9EAD3",
    "transporte": "#D9EAF7",
    "inspecao": "#FFF2CC",
    "armazenagem": "#EADCF8",
    "espera": "#F4CCCC",
}

PROCESS_LABELS = {
    "operacao": "Operação",
    "transporte": "Transporte",
    "inspecao": "Inspeção",
    "armazenagem": "Armazenagem",
    "espera": "Espera",
}

PROCESS_STYLES = {
    "operacao": "ellipse;whiteSpace=wrap;html=1;",
    "transporte": "shape=singleArrow;direction=east;whiteSpace=wrap;html=1;",
    "inspecao": "rhombus;whiteSpace=wrap;html=1;",
    "armazenagem": "triangle;direction=south;whiteSpace=wrap;html=1;",
    "espera": "shape=mxgraph.flowchart.delay;whiteSpace=wrap;html=1;",
}


def load_project() -> dict[str, Any]:
    with DATA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def source_map(project: dict[str, Any]) -> dict[str, dict[str, Any]]:
    sources = project.get("sources", {})
    if isinstance(sources, dict):
        return sources
    mapped: dict[str, dict[str, Any]] = {}
    for source in sources:
        item = dict(source)
        item["url_or_path"] = item.get("url") or item.get("path") or item.get("url_or_path") or ""
        mapped[item["id"]] = item
    return mapped


def safe_source(project: dict[str, Any], source_id: str | None) -> str:
    if not source_id:
        return "premissa"
    first = source_id.split("/")[0]
    source = source_map(project).get(first)
    if not source:
        return source_id
    return source.get("title", first)


def round2(value: float) -> float:
    return round(float(value), 2)


def calc_demand(project: dict[str, Any]) -> dict[str, Any]:
    p = project["premises"]
    target_good = float(p["target_good_kits_per_week"])
    final_yield = float(p["final_good_yield"])
    gross_exact = target_good / final_yield
    gross_rounded = math.ceil(gross_exact)
    useful_hours = (
        float(p["work_days_per_week"])
        * float(p["shifts_per_day"])
        * float(p["useful_hours_per_shift"])
    )
    scheduled_hours = (
        float(p["work_days_per_week"])
        * float(p["shifts_per_day"])
        * float(p["scheduled_hours_per_shift"])
    )
    return {
        "target_good_kits_per_week": target_good,
        "final_good_yield": final_yield,
        "input_kits_per_week_exact": gross_exact,
        "input_kits_per_week": gross_rounded,
        "work_days_per_week": p["work_days_per_week"],
        "shifts_per_day": p["shifts_per_day"],
        "scheduled_hours_per_week": scheduled_hours,
        "useful_hours_per_week": useful_hours,
        "required_average_rate_kits_per_hour": gross_rounded / useful_hours,
        "formula": "demanda_bruta = ARREDONDAR.PARA.CIMA(meta_boa / rendimento_final)",
    }


def calc_material_row(row: dict[str, Any], demand: dict[str, Any], project: dict[str, Any]) -> dict[str, Any]:
    inputs = row["inputs"]
    formula = row["formula"]
    loss_factor = float(inputs.get("fator_perda", inputs.get("fator_perda_usinagem", 1)))

    if row["unit_output"] == "g/kit":
        # The formulas intentionally stay explicit instead of hidden in a generic parser.
        if "comprimento_blank_cm" in inputs:
            net_g = (
                inputs["comprimento_blank_cm"]
                * inputs["largura_media_cm"]
                * inputs["espessura_cm"]
                * inputs["densidade_g_cm3"]
            )
            purchase_g = net_g * loss_factor
        elif "comprimento_cm" in inputs:
            width = inputs.get("largura_cm", inputs.get("largura_media_cm"))
            net_g = (
                inputs["comprimento_cm"]
                * width
                * inputs["espessura_cm"]
                * inputs["densidade_g_cm3"]
            )
            purchase_g = net_g * loss_factor
        elif "volume_estimado_total_cm3" in inputs or "volume_estimado_cabos_cm3" in inputs:
            volume = inputs.get("volume_estimado_total_cm3", inputs.get("volume_estimado_cabos_cm3"))
            net_g = volume * inputs["densidade_g_cm3"]
            purchase_g = net_g * loss_factor
        elif "quantidade_rebites" in inputs:
            net_g = inputs["quantidade_rebites"] * inputs["massa_unitaria_g"]
            purchase_g = net_g * loss_factor
        else:
            raise ValueError(f"Unsupported material formula inputs: {row['item']}")
    else:
        raise ValueError(f"Unsupported material unit: {row['unit_output']}")

    weekly_kg = purchase_g * demand["input_kits_per_week"] / 1000
    return {
        "item": row["item"],
        "formula": formula,
        "inputs": inputs,
        "source": safe_source(project, row.get("source_id")),
        "net_g_per_kit": net_g,
        "loss_factor": loss_factor,
        "purchase_g_per_kit": purchase_g,
        "purchase_kg_per_week": weekly_kg,
    }


def calc_materials(project: dict[str, Any], demand: dict[str, Any]) -> list[dict[str, Any]]:
    return [calc_material_row(row, demand, project) for row in project["material_estimates"]]


def calc_equipment(project: dict[str, Any], demand: dict[str, Any]) -> list[dict[str, Any]]:
    p = project["premises"]
    useful_hours = demand["useful_hours_per_week"]
    efficiency = float(p["general_efficiency"])
    reliability = float(p["equipment_reliability"])
    default_yield = float(p["process_yield_default"])
    rows = []

    for equipment in project["equipment"]:
        nominal_rate = float(equipment["planned_rate_per_hour"])
        process_yield = float(equipment.get("process_yield", default_yield))
        effective_rate = nominal_rate * efficiency * reliability * process_yield
        weekly_capacity = effective_rate * useful_hours
        quantity = max(1, math.ceil(demand["input_kits_per_week"] / weekly_capacity))
        utilization = demand["input_kits_per_week"] / (quantity * weekly_capacity)
        dims = equipment.get("dimensions_m", {})
        footprint = float(dims.get("length", 0)) * float(dims.get("width", 0))
        service_factor = float(equipment.get("service_area_factor", p["service_area_factor_default"]))
        planned_area = footprint * quantity * service_factor
        rows.append(
            {
                "id": equipment["id"],
                "type": equipment["type"],
                "supplier": equipment["supplier"],
                "model": equipment["model"],
                "nominal_rate_kits_per_hour": nominal_rate,
                "rate_basis": equipment.get("rate_basis", ""),
                "efficiency": efficiency,
                "reliability": reliability,
                "process_yield": process_yield,
                "effective_rate_kits_per_hour": effective_rate,
                "weekly_capacity_per_machine": weekly_capacity,
                "required_quantity": quantity,
                "utilization": utilization,
                "dimensions_m": dims,
                "footprint_m2": footprint,
                "service_area_factor": service_factor,
                "planned_area_m2": planned_area,
                "official_capacity": equipment.get("official_capacity", ""),
                "source": safe_source(project, equipment.get("source_id")),
                "source_id": equipment.get("source_id"),
            }
        )
    return rows


def calc_selected_equipment(project: dict[str, Any], demand: dict[str, Any], capacity: list[dict[str, Any]]) -> dict[str, Any]:
    selected = project["selected_equipment_calculation"]
    equipment_id = selected["equipment_id"]
    row = next(item for item in capacity if item["id"] == equipment_id)
    operation_numbers = selected.get("operation_numbers", selected.get("operations", []))
    operations = [p for p in project["processes"] if p["number"] in operation_numbers]
    standard_time = float(selected["standard_time_seconds_per_kit"])
    nominal_rate_from_time = 3600 / standard_time

    return {
        "equipment_id": equipment_id,
        "equipment_type": row["type"],
        "supplier": row["supplier"],
        "model": row["model"],
        "reason": selected["reason"],
        "operation_numbers": operation_numbers,
        "operations": [f"{op['number']} - {op['name']}" for op in operations],
        "standard_time_seconds_per_kit": standard_time,
        "nominal_rate_from_standard_time": nominal_rate_from_time,
        "nominal_rate_used": row["nominal_rate_kits_per_hour"],
        "useful_hours_per_week": demand["useful_hours_per_week"],
        "efficiency": row["efficiency"],
        "reliability": row["reliability"],
        "process_yield": row["process_yield"],
        "effective_rate_kits_per_hour": row["effective_rate_kits_per_hour"],
        "weekly_capacity_per_machine": row["weekly_capacity_per_machine"],
        "demand_input_kits_per_week": demand["input_kits_per_week"],
        "required_quantity": row["required_quantity"],
        "utilization": row["utilization"],
        "formula": (
            "quantidade = teto(demanda_bruta_semana / "
            "(taxa_nominal_h * horas_uteis_semana * eficiencia * confiabilidade * rendimento_processo))"
        ),
    }


def calc_layout(project: dict[str, Any], demand: dict[str, Any], capacity: list[dict[str, Any]]) -> dict[str, Any]:
    p = project["premises"]
    dims = p.get(
        "layout_total_dimensions_m",
        {"length": p.get("layout_target_width_m", 24), "width": p.get("layout_target_length_m", 16)},
    )
    total_layout_area = float(dims["length"]) * float(dims["width"])

    equipment_area = sum(item["planned_area_m2"] for item in capacity)
    pack = project["product"]["package_dimensions_cm"]
    package_volume_m3 = (pack["length"] / 100) * (pack["width"] / 100) * (pack["height"] / 100)
    fg_units = (
        demand["target_good_kits_per_week"] / p["work_days_per_week"]
    ) * p.get("finished_goods_inventory_days", p.get("inventory_days_finished_goods", 3))
    fg_floor_area = max(12.0, (fg_units * package_volume_m3 / 1.2) * 2.0)

    fixed_areas = [
        {
            "area": "Estoque de materia-prima e embalagens",
            "m2": 30.0,
            "basis": "premissa: 5 dias de materiais, estantes, paletes e corredor de acesso",
        },
        {
            "area": "Estoque intermediario",
            "m2": 12.0,
            "basis": "premissa: pulmão entre setores metal, madeira e montagem",
        },
        {
            "area": "Estoque de produto acabado",
            "m2": fg_floor_area,
            "basis": (
                "max(12 m2; unidades de 3 dias * volume da embalagem / 1,2 m de empilhamento * fator 2)"
            ),
        },
        {
            "area": "Inspecao e controle de qualidade",
            "m2": 12.0,
            "basis": "premissa: bancada, instrumentos e area de retencao",
        },
        {
            "area": "Recebimento e expedicao",
            "m2": 24.0,
            "basis": "premissa: doca simples, conferencia e separacao",
        },
        {
            "area": "Apoio, manutencao, EPI e compressor",
            "m2": 20.0,
            "basis": "premissa de apoio operacional minimo",
        },
    ]

    subtotal_before_circulation = equipment_area + sum(item["m2"] for item in fixed_areas)
    circulation = subtotal_before_circulation * 0.30
    total_required = subtotal_before_circulation + circulation

    return {
        "layout_dimensions_m": dims,
        "layout_total_area_m2": total_layout_area,
        "equipment_area_m2": equipment_area,
        "fixed_areas": fixed_areas,
        "circulation_area_m2": circulation,
        "circulation_formula": "30% * (area_equipamentos + areas_fixas)",
        "total_required_area_m2": total_required,
        "free_area_m2": total_layout_area - total_required,
        "occupancy": total_required / total_layout_area,
        "package_volume_m3": package_volume_m3,
        "finished_goods_units_for_area": fg_units,
    }


def build_results(project: dict[str, Any]) -> dict[str, Any]:
    demand = calc_demand(project)
    materials = calc_materials(project, demand)
    capacity = calc_equipment(project, demand)
    selected = calc_selected_equipment(project, demand, capacity)
    layout = calc_layout(project, demand, capacity)
    bottleneck = min(capacity, key=lambda item: item["weekly_capacity_per_machine"])

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "project_name": project["metadata"]["project_name"],
        "metadata": project["metadata"],
        "product": project["product"],
        "premises": project["premises"],
        "demand": demand,
        "materials": materials,
        "equipment_capacity": capacity,
        "selected_equipment_detail": selected,
        "layout": layout,
        "bottleneck": bottleneck,
        "bom": project["bom"],
        "processes": project["processes"],
        "research_matrix": project["research_matrix"],
        "sources": source_map(project),
        "project_objectives": project.get("project_objectives", []),
        "market_segments": project.get("market_segments", []),
        "conclusions": project.get("conclusions", {}),
    }


def write_json(results: dict[str, Any]) -> None:
    RESULTS_PATH.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")


def write_sources_markdown(results: dict[str, Any]) -> None:
    lines = [
        "# Fontes e base tecnica pesquisada",
        "",
        "Este arquivo separa fatos de fonte e premissas adotadas. As contas usam `data/projeto.json` e `data/resultados_calculo.json`.",
        "",
        "| ID | Fonte | Uso no projeto | Confianca | Link |",
        "|---|---|---|---|---|",
    ]
    sources = results["sources"]
    for row in results["research_matrix"]:
        sid = row["source_id"]
        source = sources.get(sid, {})
        use = row.get("use", row.get("used_in", ""))
        lines.append(
            f"| {sid} | {source.get('title', sid)} | {use} | {row['confidence']} | {source.get('url_or_path', '')} |"
        )
    (ROOT / "05_base_tecnica" / "fontes_pesquisa_e_premissas.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def write_memory_markdown(results: dict[str, Any]) -> None:
    demand = results["demand"]
    selected = results["selected_equipment_detail"]
    layout = results["layout"]
    lines = [
        "# Memoria de calculo transparente",
        "",
        "Todas as contas abaixo foram geradas por `scripts/generate_outputs.py` a partir de `data/projeto.json`.",
        "",
        "## Demanda",
        "",
        f"- Meta de produtos bons: {demand['target_good_kits_per_week']:.0f} kits/semana.",
        f"- Rendimento final assumido: {demand['final_good_yield']:.2%}.",
        f"- Demanda bruta: ceil({demand['target_good_kits_per_week']:.0f} / {demand['final_good_yield']:.2f}) = {demand['input_kits_per_week']:.0f} kits/semana.",
        f"- Horas uteis: {demand['work_days_per_week']} dias * {demand['shifts_per_day']} turno * {results['premises']['useful_hours_per_shift']} h = {demand['useful_hours_per_week']:.1f} h/semana.",
        f"- Ritmo medio necessario: {demand['input_kits_per_week']:.0f} / {demand['useful_hours_per_week']:.1f} = {demand['required_average_rate_kits_per_hour']:.2f} kits/h.",
        "",
        "## Equipamento selecionado para memoria detalhada",
        "",
        f"- Equipamento: {selected['equipment_type']} - {selected['supplier']} {selected['model']}.",
        f"- Operacoes consideradas: {', '.join(selected['operations'])}.",
        f"- Motivo da selecao: {selected['reason']}.",
        f"- Tempo padrao: {selected['standard_time_seconds_per_kit']:.0f} s/kit.",
        f"- Taxa nominal: 3600 / {selected['standard_time_seconds_per_kit']:.0f} = {selected['nominal_rate_from_standard_time']:.2f} kits/h.",
        f"- Taxa efetiva: {selected['nominal_rate_used']:.2f} * {selected['efficiency']:.2f} * {selected['reliability']:.2f} * {selected['process_yield']:.2f} = {selected['effective_rate_kits_per_hour']:.2f} kits/h.",
        f"- Capacidade semanal por maquina: {selected['effective_rate_kits_per_hour']:.2f} * {selected['useful_hours_per_week']:.1f} = {selected['weekly_capacity_per_machine']:.2f} kits/semana.",
        f"- Quantidade necessaria: ceil({selected['demand_input_kits_per_week']:.0f} / {selected['weekly_capacity_per_machine']:.2f}) = {selected['required_quantity']} equipamento(s).",
        f"- Utilizacao estimada: {selected['utilization']:.1%}.",
        "",
        "## Areas",
        "",
        f"- Area total proposta: {layout['layout_dimensions_m']['length']} m * {layout['layout_dimensions_m']['width']} m = {layout['layout_total_area_m2']:.1f} m2.",
        f"- Area estimada necessaria: {layout['total_required_area_m2']:.1f} m2.",
        f"- Ocupacao: {layout['occupancy']:.1%}; folga: {layout['free_area_m2']:.1f} m2.",
    ]
    (ROOT / "02_calculos" / "memoria_calculo_transparente.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def write_slide_script(results: dict[str, Any]) -> None:
    selected = results["selected_equipment_detail"]
    members = [member["name"] for member in results.get("metadata", {}).get("group_members", [])]
    pending_member_note = results.get("metadata", {}).get("pending_member_note")
    lines = [
        "# Roteiro de apresentacao - Projeto de fabrica",
        "",
        "Tempo alvo: 20 minutos. Estrutura sugerida para gerar a apresentacao final em PDF. A montagem do PPTX fica por ultimo, depois da base tecnica fechada.",
        "",
        "## Integrantes",
        "",
        *[f"- {name}" for name in members],
    ]
    if pending_member_note:
        lines.append(f"- Pendente: {pending_member_note}")
    lines.extend(
        [
            "",
            "## Sequencia sugerida",
            "",
            "1. Capa: nome do produto, integrantes e objetivo.",
            "2. Objetivos do projeto: escala industrial, qualidade, capacidade e layout basico.",
            "3. Produto: imagem, desenho tecnico, dimensoes, materiais e embalagem.",
            "4. Estrutura pai-filho: kit embalado > faca, garfo, tabua, embalagem, etiquetas e caixa.",
            "5. Segmentos de mercado: churrasco domestico, presentes, varejo/e-commerce e kits promocionais.",
            "6. Meta semanal: 1.000 kits bons/semana; demanda bruta calculada no modelo.",
            "7. Tabela 1: componentes, quantidade, unidade e fazer/comprar.",
            "8. Processo produtivo: explicar a Tabela 2 e os cinco tipos de processo.",
            "9. Fluxograma: usar `03_diagramas/fluxograma_processo.drawio`.",
            "10. Equipamentos: mostrar Tabela 3, fornecedores, dimensoes e capacidades.",
            f"11. Memoria de calculo: detalhar {selected['supplier']} {selected['model']} e justificar {selected['required_quantity']} unidades.",
            "12. Layout esquematico: usar `03_diagramas/layout_esquematico.drawio`, dimensoes totais e areas.",
            "13. Mapofluxograma: usar `03_diagramas/mapofluxograma.drawio` para relacionar fluxo e arranjo fisico.",
            "14. Conclusoes: limitacoes, cotacoes pendentes, teste de tempos reais, melhoria de qualidade e sustentabilidade.",
        ]
    )
    lines.extend(
        [
        "",
        "Arquivos de apoio: `02_calculos/demonstrativo_calculos.xlsx`, `06_dashboard/index.html` e `05_base_tecnica/fontes_pesquisa_e_premissas.md`.",
        ]
    )
    (ROOT / "01_apresentacao" / "roteiro_slides.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def mx_cell(
    cell_id: str,
    value: str,
    style: str,
    x: float,
    y: float,
    w: float,
    h: float,
    parent: str = "1",
) -> str:
    return (
        f'<mxCell id="{cell_id}" value="{xml_escape(value)}" style="{style}" vertex="1" parent="{parent}">'
        f'<mxGeometry x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" as="geometry"/>'
        "</mxCell>"
    )


def mx_edge(edge_id: str, source: str, target: str, label: str = "") -> str:
    return (
        f'<mxCell id="{edge_id}" value="{xml_escape(label)}" '
        'style="endArrow=block;html=1;rounded=0;strokeWidth=2;strokeColor=#555555;" '
        f'edge="1" parent="1" source="{source}" target="{target}">'
        '<mxGeometry relative="1" as="geometry"/></mxCell>'
    )


def wrap_mxfile(name: str, cells: list[str], width: int = 1200, height: int = 800) -> str:
    content = "\n".join(['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>', *cells])
    return (
        '<mxfile host="app.diagrams.net" modified="2026-05-13T00:00:00.000Z" agent="Codex">'
        f'<diagram name="{xml_escape(name)}">'
        f'<mxGraphModel dx="{width}" dy="{height}" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" '
        'arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="1000" math="0" shadow="0">'
        f"<root>{content}</root></mxGraphModel></diagram></mxfile>"
    )


def write_flowchart(results: dict[str, Any]) -> None:
    cells: list[str] = []
    processes_by_num = {p["number"]: p for p in results["processes"]}
    metal  = [3, 4, 5, 6, 7, 8, 9, 10]
    wood   = [11, 12, 13, 14, 15, 16, 17]
    single = [18, 19, 20, 21, 22, 23, 24, 25, 26]
    COL_L, COL_R, COL_C = 80, 700, 390
    ROW_H = 110
    node_w, node_h = 200, 75
    legend_x = 1050

    cells.append(mx_cell("title", "Fluxograma do Processo — Kit Churrasco Tramontina 22399036",
                         "text;html=1;fontSize=18;fontStyle=1;", 80, 15, 700, 38))
    cells.append(mx_cell("lbl_metal",   "Trilha Metálica", "text;html=1;fontSize=13;fontStyle=2;", COL_L, 260, 200, 24))
    cells.append(mx_cell("lbl_madeira", "Trilha Madeira",        "text;html=1;fontSize=13;fontStyle=2;", COL_R, 260, 200, 24))
    for idx, key in enumerate(["operacao", "transporte", "inspecao", "armazenagem", "espera"]):
        style = PROCESS_STYLES[key] + f"fillColor={PROCESS_COLORS[key]};strokeColor=#555555;"
        cells.append(mx_cell(f"legend_{key}", PROCESS_LABELS[key], style, legend_x, 60 + idx * 85, 150, 65))

    pos_x: dict[int, float] = {}
    pos_y: dict[int, float] = {}
    pos_x[1] = pos_x[2] = COL_C
    pos_y[1] = 60; pos_y[2] = 170
    for i, n in enumerate([3,4,5,6,7,8,9,10]):
        pos_x[n] = COL_L; pos_y[n] = 290 + i * ROW_H
    for i, n in enumerate([11,12,13,14,15,16,17]):
        pos_x[n] = COL_R; pos_y[n] = 290 + i * ROW_H
    merge_start_y = 290 + 7 * ROW_H + 120
    for i, n in enumerate([18,19,20,21,22,23,24,25,26]):
        pos_x[n] = COL_C; pos_y[n] = merge_start_y + i * ROW_H

    node_ids: dict[int, str] = {}
    for num in range(1, 27):
        proc = processes_by_num[num]
        pid = f"p{num}"
        node_ids[num] = pid
        key = proc["type"]
        label = f"{num}. {proc['name']}"
        style = PROCESS_STYLES[key] + f"fillColor={PROCESS_COLORS[key]};strokeColor=#555555;fontSize=11;"
        cells.append(mx_cell(pid, label, style, pos_x[num], pos_y[num], node_w, node_h))

    flow_edges = (
        [(1,2), (2,3), (2,11)] +
        [(metal[i], metal[i+1]) for i in range(len(metal)-1)] +
        [(wood[i],  wood[i+1])  for i in range(len(wood)-1)] +
        [(10,18), (17,18)] +
        [(single[i], single[i+1]) for i in range(len(single)-1)]
    )
    seen: set[tuple[int,int]] = set()
    for idx, (a, b) in enumerate(flow_edges):
        if (a,b) not in seen:
            seen.add((a,b))
            cells.append(mx_edge(f"e_{a}_{b}", node_ids[a], node_ids[b]))

    canvas_h = int(merge_start_y + len(single) * ROW_H + 200)
    output = ROOT / "03_diagramas" / "fluxograma_processo.drawio"
    output.write_text(wrap_mxfile("Fluxograma", cells, width=1400, height=canvas_h), encoding="utf-8")


def layout_zones() -> list[dict[str, Any]]:
    # 9 zones covering exactly 24 m x 16 m = 384 m2, no gaps, no overlaps.
    return [
        {"id": "setor_metal",    "name": "Setor Metal",             "x_m": 0,  "y_m": 0,  "w_m": 13, "h_m": 8,  "fill": "#D9EAD3"},
        {"id": "setor_madeira",  "name": "Setor Madeira",           "x_m": 13, "y_m": 0,  "w_m": 11, "h_m": 9,  "fill": "#FFF2CC"},
        {"id": "montagem",       "name": "Montagem",                "x_m": 13, "y_m": 9,  "w_m": 7,  "h_m": 7,  "fill": "#D9EAF7"},
        {"id": "embalagem",      "name": "Embalagem",               "x_m": 20, "y_m": 9,  "w_m": 4,  "h_m": 7,  "fill": "#F4CCCC"},
        {"id": "inspecao_qc",    "name": "Inspeção / QC",           "x_m": 0,  "y_m": 8,  "w_m": 5,  "h_m": 4,  "fill": "#FCE5CD"},
        {"id": "apoio",          "name": "Apoio / Manutenção",      "x_m": 0,  "y_m": 12, "w_m": 5,  "h_m": 4,  "fill": "#F5F5F5"},
        {"id": "estoque_mp",     "name": "Estoque MP",              "x_m": 5,  "y_m": 8,  "w_m": 5,  "h_m": 4,  "fill": "#EADCF8"},
        {"id": "estoque_inter",  "name": "Est. Intermediário",      "x_m": 5,  "y_m": 12, "w_m": 5,  "h_m": 4,  "fill": "#EADCF8"},
        {"id": "recebimento",    "name": "Recebimento / Expedição", "x_m": 10, "y_m": 8,  "w_m": 3,  "h_m": 8,  "fill": "#CFE2F3"},
    ]


def write_layout(results: dict[str, Any], project: dict[str, Any]) -> None:
    cells: list[str] = []
    dims = results["layout"]["layout_dimensions_m"]
    SCALE_PX = 42
    ORIGIN_X, ORIGIN_Y = 30, 70

    cells.append(mx_cell("title", f"Layout Esquemático — {dims['length']} m × {dims['width']} m",
                         "text;html=1;fontSize=18;fontStyle=1;", 30, 20, 700, 38))
    cells.append(mx_cell("outer",
                         f"Área total: {dims['length']}×{dims['width']} = {results['layout']['layout_total_area_m2']:.0f} m²",
                         "rounded=0;whiteSpace=wrap;html=1;strokeWidth=3;fillColor=none;",
                         ORIGIN_X, ORIGIN_Y, dims["length"]*SCALE_PX, dims["width"]*SCALE_PX))

    for zone in layout_zones():
        cells.append(mx_cell(
            zone["id"],
            f"{zone['name']}\n{zone['w_m']*zone['h_m']} m²",
            f"rounded=0;whiteSpace=wrap;html=1;fillColor={zone['fill']};strokeColor=#555;fontStyle=1;fontSize=11;",
            ORIGIN_X + zone["x_m"]*SCALE_PX,
            ORIGIN_Y + zone["y_m"]*SCALE_PX,
            zone["w_m"]*SCALE_PX,
            zone["h_m"]*SCALE_PX,
        ))

    eq_map = {e["id"]: e for e in project["equipment"]}
    PLACEMENTS = [
        ("laser_fibra",        None,                     0.3,  0.3),
        ("forno_tt",           None,                     6.8,  0.3),
        ("politriz_metal",     None,                    11.5,  0.3),
        ("afiador",            None,                    11.5,  2.0),
        ("esquadrejadeira",    None,                    13.3,  0.3),
        ("router_cnc",         "Router CNC (1)",        16.8,  0.3),
        ("router_cnc",         "Router CNC (2)",        16.8,  2.8),
        ("lixadeira_madeira",  None,                    13.3,  4.5),
        ("acabamento_madeira", None,                    20.8,  0.3),
        ("rebitadeira",        None,                    13.3,  9.3),
        ("bancada_montagem",   "Bancada Montagem",      16.0,  9.3),
        ("seladora_blister",   None,                    20.3,  9.3),
        ("bancada_montagem",   "Bancada QC",             0.3,  8.3),
        ("bancada_montagem",   "Bancada Embalagem",     20.3, 13.3),
    ]
    for idx, (eq_id, lbl_override, ex_m, ey_m) in enumerate(PLACEMENTS):
        eq = eq_map.get(eq_id)
        if not eq:
            continue
        label = lbl_override or eq["model"]
        cells.append(mx_cell(
            f"eq{idx}", label,
            "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#333;fontSize=9;",
            ORIGIN_X + ex_m * SCALE_PX,
            ORIGIN_Y + ey_m * SCALE_PX,
            eq["dimensions_m"]["length"] * SCALE_PX,
            eq["dimensions_m"]["width"]  * SCALE_PX,
        ))

    output = ROOT / "03_diagramas" / "layout_esquematico.drawio"
    output.write_text(wrap_mxfile("Layout", cells, width=1400, height=900), encoding="utf-8")


def write_mapoflow(results: dict[str, Any], project: dict[str, Any]) -> None:
    cells: list[str] = []
    dims = results["layout"]["layout_dimensions_m"]
    SCALE_PX = 42
    ORIGIN_X, ORIGIN_Y = 30, 70

    cells.append(mx_cell("title", "Mapofluxograma — Fluxo sobre o Arranjo Físico",
                         "text;html=1;fontSize=18;fontStyle=1;", 30, 20, 700, 38))
    cells.append(mx_cell("outer",
                         f"Área total: {dims['length']} m × {dims['width']} m",
                         "rounded=0;whiteSpace=wrap;html=1;strokeWidth=3;fillColor=none;",
                         ORIGIN_X, ORIGIN_Y,
                         dims["length"]*SCALE_PX, dims["width"]*SCALE_PX))

    for zone in layout_zones():
        cells.append(mx_cell(
            zone["id"], zone["name"],
            f"rounded=0;whiteSpace=wrap;html=1;fillColor={zone['fill']};strokeColor=#888;fontStyle=2;fontSize=11;",
            ORIGIN_X + zone["x_m"]*SCALE_PX,
            ORIGIN_Y + zone["y_m"]*SCALE_PX,
            zone["w_m"]*SCALE_PX,
            zone["h_m"]*SCALE_PX,
        ))

    # Process positions on layout in meters (center of each process node)
    MAPO_POS = {
        1:  (11.5, 12.0),  2:  (7.5,  10.0),  3:  (5.5,  9.5),
        4:  (3.0,  2.5),   5:  (6.0,  2.5),    6:  (8.8,  1.3),
        7:  (8.8,  5.0),   8:  (11.5, 1.3),    9:  (11.5, 2.8),
        10: (6.5,  13.0),  11: (11.2, 9.5),    12: (15.3, 1.6),
        13: (18.5, 1.5),   14: (15.0, 5.3),    15: (22.0, 1.5),
        16: (22.0, 4.0),   17: (22.0, 7.0),    18: (12.5, 9.0),
        19: (15.0, 10.5),  20: (2.5,  9.5),    21: (17.5, 10.5),
        22: (21.5, 10.5),  23: (2.5,  11.5),   24: (21.5, 13.0),
        25: (7.5,  13.8),  26: (11.5, 14.5),
    }

    procs_by_num = {p["number"]: p for p in results["processes"]}
    node_ids: dict[int, str] = {}
    node_size = 40  # square pixels for each process circle node

    for num, (mx_pos, my_pos) in MAPO_POS.items():
        pid = f"mp{num}"
        node_ids[num] = pid
        proc = procs_by_num[num]
        fill = PROCESS_COLORS.get(proc["type"], "#FFFFFF")
        cells.append(mx_cell(
            pid, str(num),
            f"ellipse;whiteSpace=wrap;html=1;fillColor={fill};strokeColor=#333;fontStyle=1;fontSize=11;",
            ORIGIN_X + mx_pos*SCALE_PX - node_size//2,
            ORIGIN_Y + my_pos*SCALE_PX - node_size//2,
            node_size, node_size,
        ))

    flow_edges = (
        [(i, i+1) for i in range(1, 10)] +
        [(2, 11)] + [(i, i+1) for i in range(11, 17)] +
        [(10, 18), (17, 18)] +
        [(i, i+1) for i in range(18, 26)]
    )
    seen: set[tuple[int,int]] = set()
    for idx, (a, b) in enumerate(flow_edges):
        if (a, b) not in seen:
            seen.add((a, b))
            cells.append(mx_edge(f"mf{idx}", node_ids[a], node_ids[b], str(b)))

    output = ROOT / "03_diagramas" / "mapofluxograma.drawio"
    output.write_text(wrap_mxfile("Mapofluxograma", cells, width=1400, height=900), encoding="utf-8")


def split_svg_lines(text: str, max_chars: int = 21, max_lines: int = 3) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if len(trial) <= max_chars:
            current = trial
            continue
        if current:
            lines.append(current)
        current = word
        if len(lines) == max_lines:
            break
    if current and len(lines) < max_lines:
        lines.append(current)
    if len(lines) == max_lines and len(" ".join(words)) > len(" ".join(lines)):
        lines[-1] = lines[-1].rstrip(".") + "..."
    return lines


def svg_text(x: float, y: float, lines: list[str], size: int = 13, weight: str = "400") -> str:
    tspans = []
    for idx, line in enumerate(lines):
        dy = 0 if idx == 0 else size + 3
        tspans.append(
            f'<tspan x="{x:.0f}" dy="{dy:.0f}">{xml_escape(line)}</tspan>'
        )
    return (
        f'<text x="{x:.0f}" y="{y:.0f}" font-family="Arial, Helvetica, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="#17212b">{"".join(tspans)}</text>'
    )


def build_flowchart_svg(results: dict[str, Any]) -> str:
    processes_by_num = {p["number"]: p for p in results["processes"]}
    COLORS = {
        "operacao": "#D9EAD3", "transporte": "#D9EAF7",
        "inspecao": "#FFF2CC", "armazenagem": "#EADCF8", "espera": "#F4CCCC",
    }
    W = 1100
    COL_L, COL_R, COL_C = 220, 880, 550
    ROW_H = 118

    pos: dict[int, tuple[int, int]] = {}
    pos[1] = (COL_C, 75)
    pos[2] = (COL_C, 193)
    metal = [3, 4, 5, 6, 7, 8, 9, 10]
    wood  = [11, 12, 13, 14, 15, 16, 17]
    single = [18, 19, 20, 21, 22, 23, 24, 25, 26]
    for i, n in enumerate(metal):
        pos[n] = (COL_L, 320 + i * ROW_H)
    for i, n in enumerate(wood):
        pos[n] = (COL_R, 320 + i * ROW_H)
    merge_y = 320 + 7 * ROW_H + 130
    for i, n in enumerate(single):
        pos[n] = (COL_C, merge_y + i * ROW_H)
    total_h = merge_y + len(single) * ROW_H + 80

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {total_h}" '
        f'width="{W}" height="{total_h}" font-family="Arial,Helvetica,sans-serif">',
        '<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">'
        '<path d="M0,0 L0,6 L8,3 z" fill="#444"/></marker></defs>',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{W//2}" y="28" text-anchor="middle" font-size="17" font-weight="bold">'
        'Fluxograma do Processo — Kit Churrasco Tramontina 22399036</text>',
        f'<text x="{COL_L}" y="278" text-anchor="middle" font-size="13" fill="#555" font-style="italic">Trilha Metálica</text>',
        f'<text x="{COL_R}" y="278" text-anchor="middle" font-size="13" fill="#555" font-style="italic">Trilha Madeira</text>',
    ]

    def arr_line(x1, y1, x2, y2):
        return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                f'stroke="#444" stroke-width="2" marker-end="url(#arr)"/>')

    def poly_arr(pts):
        return (f'<polyline points="{pts}" fill="none" stroke="#444" '
                f'stroke-width="2" marker-end="url(#arr)"/>')

    parts.append(arr_line(COL_C, pos[1][1]+44, COL_C, pos[2][1]-44))
    branch_y = pos[2][1] + 44
    fork_y   = pos[2][1] + 90
    parts.append(poly_arr(f"{COL_C},{branch_y} {COL_C},{fork_y} {COL_L},{fork_y} {COL_L},{pos[3][1]-44}"))
    parts.append(poly_arr(f"{COL_C},{branch_y} {COL_C},{fork_y} {COL_R},{fork_y} {COL_R},{pos[11][1]-44}"))
    for i in range(len(metal)-1):
        parts.append(arr_line(COL_L, pos[metal[i]][1]+44, COL_L, pos[metal[i+1]][1]-44))
    for i in range(len(wood)-1):
        parts.append(arr_line(COL_R, pos[wood[i]][1]+44, COL_R, pos[wood[i+1]][1]-44))
    pre_y = pos[18][1] - 40
    parts.append(poly_arr(f"{COL_L},{pos[10][1]+44} {COL_L},{pre_y} {COL_C},{pre_y} {COL_C},{pos[18][1]-44}"))
    parts.append(f'<polyline points="{COL_R},{pos[17][1]+44} {COL_R},{pre_y} {COL_C},{pre_y}" '
                 f'fill="none" stroke="#444" stroke-width="2"/>')
    for i in range(len(single)-1):
        parts.append(arr_line(COL_C, pos[single[i]][1]+44, COL_C, pos[single[i+1]][1]-44))

    def node(proc):
        n = proc["number"]
        ptype = proc["type"]
        x, y = pos[n]
        color = COLORS[ptype]
        lines_txt = split_svg_lines(proc["name"], 22, 2)
        if ptype == "operacao":
            shape = (f'<ellipse cx="{x}" cy="{y}" rx="100" ry="42" '
                     f'fill="{color}" stroke="#444" stroke-width="1.8"/>')
        elif ptype == "inspecao":
            pts = f"{x},{y-46} {x+100},{y} {x},{y+46} {x-100},{y}"
            shape = f'<polygon points="{pts}" fill="{color}" stroke="#444" stroke-width="1.8"/>'
        elif ptype == "armazenagem":
            pts = f"{x-100},{y-42} {x+100},{y-42} {x},{y+46}"
            shape = f'<polygon points="{pts}" fill="{color}" stroke="#444" stroke-width="1.8"/>'
        elif ptype == "espera":
            shape = (f'<path d="M {x-100},{y-42} L {x+55},{y-42} '
                     f'Q {x+100},{y-42} {x+100},{y} Q {x+100},{y+42} {x+55},{y+42} '
                     f'L {x-100},{y+42} Z" fill="{color}" stroke="#444" stroke-width="1.8"/>')
        else:  # transporte
            pts = f"{x-100},{y-22} {x+58},{y-22} {x+58},{y-44} {x+100},{y} {x+58},{y+44} {x+58},{y+22} {x-100},{y+22}"
            shape = f'<polygon points="{pts}" fill="{color}" stroke="#444" stroke-width="1.8"/>'
        num_lbl = f'<text x="{x-80}" y="{y-20}" font-size="11" font-weight="bold" fill="#222">{n}</text>'
        tspans = []
        for li, lt in enumerate(lines_txt):
            dy = y - 5 + li * 14
            tspans.append(f'<text x="{x}" y="{dy}" text-anchor="middle" font-size="10" fill="#222">{xml_escape(lt)}</text>')
        return shape + "\n" + num_lbl + "\n" + "\n".join(tspans)

    for num in sorted(pos.keys()):
        parts.append(node(processes_by_num[num]))

    lx, ly = W - 235, 55
    parts.append(f'<rect x="{lx-8}" y="{ly-8}" width="225" height="178" fill="white" stroke="#aaa" stroke-width="1" rx="4"/>')
    parts.append(f'<text x="{lx+105}" y="{ly+10}" text-anchor="middle" font-size="12" font-weight="bold">Legenda</text>')
    for i, (ptype, lbl) in enumerate([("operacao","Operação"),("inspecao","Inspeção"),("armazenagem","Armazenagem"),("espera","Espera"),("transporte","Transporte")]):
        liy = ly + 32 + i * 28
        parts.append(f'<rect x="{lx}" y="{liy-11}" width="26" height="19" fill="{COLORS[ptype]}" stroke="#444" stroke-width="1"/>')
        parts.append(f'<text x="{lx+35}" y="{liy+3}" font-size="12" fill="#222">{lbl}</text>')

    parts.append("</svg>")
    return "\n".join(parts)


def build_layout_svg(results: dict[str, Any], project: dict[str, Any], with_flow: bool = False) -> str:
    SCALE = 38
    MARGIN = 65
    W_m = results["layout"]["layout_dimensions_m"]["length"]   # 24
    H_m = results["layout"]["layout_dimensions_m"]["width"]    # 16
    SVG_W = W_m * SCALE + MARGIN * 2
    SVG_H = H_m * SCALE + MARGIN * 2 + 50

    eq_map = {e["id"]: e for e in project["equipment"]}

    PLACEMENTS = [
        ("laser_fibra",        None,                     0.3,  0.3),
        ("forno_tt",           None,                     6.8,  0.3),
        ("politriz_metal",     None,                    11.5,  0.3),
        ("afiador",            None,                    11.5,  2.0),
        ("esquadrejadeira",    None,                    13.3,  0.3),
        ("router_cnc",         "Router CNC (1)",        16.8,  0.3),
        ("router_cnc",         "Router CNC (2)",        16.8,  2.8),
        ("lixadeira_madeira",  None,                    13.3,  4.5),
        ("acabamento_madeira", None,                    20.8,  0.3),
        ("rebitadeira",        None,                    13.3,  9.3),
        ("bancada_montagem",   "Bancada Montagem",      16.0,  9.3),
        ("seladora_blister",   None,                    20.3,  9.3),
        ("bancada_montagem",   "Bancada QC",             0.3,  8.3),
        ("bancada_montagem",   "Bancada Embalagem",     20.3, 13.3),
    ]

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SVG_W} {SVG_H}" '
        f'width="{SVG_W}" height="{SVG_H}" font-family="Arial,Helvetica,sans-serif">',
        '<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">'
        '<path d="M0,0 L0,6 L8,3 z" fill="#444"/></marker></defs>',
        '<rect width="100%" height="100%" fill="white"/>',
    ]
    title = "Mapofluxograma" if with_flow else "Arranjo Físico Esquemático"
    parts.append(
        f'<text x="{SVG_W//2}" y="24" text-anchor="middle" font-size="16" font-weight="bold">'
        f'{title} — Kit Churrasco Tramontina 22399036</text>'
    )
    layout = results["layout"]
    parts.append(
        f'<text x="{SVG_W//2}" y="42" text-anchor="middle" font-size="12" fill="#555">'
        f'Área total: {W_m} m × {H_m} m = {W_m*H_m} m²  |  '
        f'Área requerida: {layout["total_required_area_m2"]:.1f} m²  |  '
        f'Ocupação: {layout["occupancy"]*100:.1f}%</text>'
    )

    for z in layout_zones():
        px = MARGIN + z["x_m"] * SCALE
        py = 55 + z["y_m"] * SCALE
        pw = z["w_m"] * SCALE
        ph = z["h_m"] * SCALE
        parts.append(
            f'<rect x="{px:.1f}" y="{py:.1f}" width="{pw:.1f}" height="{ph:.1f}" '
            f'fill="{z["fill"]}" stroke="#888" stroke-width="1.5"/>'
        )
        parts.append(
            f'<text x="{px+pw/2:.1f}" y="{py+ph/2-6:.1f}" text-anchor="middle" '
            f'font-size="11" font-weight="bold" fill="#444">{xml_escape(z["name"])}</text>'
        )
        parts.append(
            f'<text x="{px+pw/2:.1f}" y="{py+ph/2+9:.1f}" text-anchor="middle" '
            f'font-size="9" fill="#888">{z["w_m"]*z["h_m"]} m²</text>'
        )

    if not with_flow:
        for eq_id, lbl_override, ex_m, ey_m in PLACEMENTS:
            eq = eq_map.get(eq_id)
            if not eq:
                continue
            ew = eq["dimensions_m"]["length"] * SCALE
            eh = eq["dimensions_m"]["width"]  * SCALE
            epx = MARGIN + ex_m * SCALE
            epy = 55 + ey_m * SCALE
            label = lbl_override or eq["model"]
            parts.append(
                f'<rect x="{epx:.1f}" y="{epy:.1f}" width="{ew:.1f}" height="{eh:.1f}" '
                f'fill="#444" fill-opacity="0.78" stroke="#111" stroke-width="1" rx="2"/>'
            )
            parts.append(
                f'<text x="{epx+ew/2:.1f}" y="{epy+eh/2+4:.1f}" text-anchor="middle" '
                f'font-size="8" fill="white">{xml_escape(label[:18])}</text>'
            )

    # Dimension annotations
    dim_y = 55 + H_m * SCALE + 22
    parts.append(
        f'<line x1="{MARGIN}" y1="{dim_y}" x2="{MARGIN + W_m*SCALE}" y2="{dim_y}" '
        f'stroke="#222" stroke-width="1.5"/>'
    )
    parts.append(
        f'<text x="{MARGIN + W_m*SCALE/2:.1f}" y="{dim_y+14}" text-anchor="middle" '
        f'font-size="12" font-weight="bold">{W_m} m</text>'
    )
    dim_x = MARGIN + W_m * SCALE + 20
    cx = dim_x + 12
    cy = 55 + H_m * SCALE / 2
    parts.append(
        f'<line x1="{dim_x}" y1="55" x2="{dim_x}" y2="{55+H_m*SCALE}" '
        f'stroke="#222" stroke-width="1.5"/>'
    )
    parts.append(
        f'<text x="{cx}" y="{cy}" text-anchor="middle" font-size="12" font-weight="bold" '
        f'transform="rotate(-90 {cx} {cy})">{H_m} m</text>'
    )

    if with_flow:
        MAPO_POS = {
            1:  (11.5, 12.0),  2:  (7.5,  10.0),  3:  (5.5,  9.5),
            4:  (3.0,  2.5),   5:  (6.0,  2.5),    6:  (8.8,  1.3),
            7:  (8.8,  5.0),   8:  (11.5, 1.3),    9:  (11.5, 2.8),
            10: (6.5,  13.0),  11: (11.2, 9.5),    12: (15.3, 1.6),
            13: (18.5, 1.5),   14: (15.0, 5.3),    15: (22.0, 1.5),
            16: (22.0, 4.0),   17: (22.0, 7.0),    18: (12.5, 9.0),
            19: (15.0, 10.5),  20: (2.5,  9.5),    21: (17.5, 10.5),
            22: (21.5, 10.5),  23: (2.5,  11.5),   24: (21.5, 13.0),
            25: (7.5,  13.8),  26: (11.5, 14.5),
        }
        PCOLORS = {
            "operacao": "#D9EAD3", "transporte": "#D9EAF7",
            "inspecao": "#FFF2CC", "armazenagem": "#EADCF8", "espera": "#F4CCCC",
        }
        procs_by_num = {p["number"]: p for p in results["processes"]}
        metal_set  = set(range(1, 11))
        wood_set   = {11,12,13,14,15,16,17}
        metal_color, wood_color, single_color = "#1e7a3c", "#a05000", "#17212b"

        flow_edges = (
            [(i, i+1) for i in range(1, 10)] +
            [(2, 11)] + [(i, i+1) for i in range(11, 17)] +
            [(10, 18), (17, 18)] +
            [(i, i+1) for i in range(18, 26)]
        )
        for (a, b) in flow_edges:
            if b in wood_set or (a == 2 and b == 11):
                color = wood_color
            elif a in metal_set and b in metal_set:
                color = metal_color
            else:
                color = single_color
            ax = MARGIN + MAPO_POS[a][0] * SCALE
            ay = 55     + MAPO_POS[a][1] * SCALE
            bx = MARGIN + MAPO_POS[b][0] * SCALE
            by_ = 55    + MAPO_POS[b][1] * SCALE
            parts.append(
                f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{bx:.1f}" y2="{by_:.1f}" '
                f'stroke="{color}" stroke-width="2.5" marker-end="url(#arr)" opacity="0.8"/>'
            )

        for num, (mx_pos, my_pos) in MAPO_POS.items():
            px_ = MARGIN + mx_pos * SCALE
            py_ = 55     + my_pos * SCALE
            proc = procs_by_num[num]
            fill = PCOLORS.get(proc["type"], "#FFFFFF")
            stroke = metal_color if num in metal_set else (wood_color if num in wood_set else single_color)
            parts.append(
                f'<circle cx="{px_:.1f}" cy="{py_:.1f}" r="16" '
                f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
            )
            parts.append(
                f'<text x="{px_:.1f}" y="{py_+5:.1f}" text-anchor="middle" '
                f'font-size="11" font-weight="bold" fill="{stroke}">{num}</text>'
            )

        lx, ly = SVG_W - 185, 58
        parts.append(f'<rect x="{lx-5}" y="{ly-5}" width="178" height="80" fill="white" stroke="#aaa" stroke-width="1" rx="3"/>')
        parts.append(f'<text x="{lx+85}" y="{ly+10}" text-anchor="middle" font-size="11" font-weight="bold">Legenda</text>')
        for li, (color, label) in enumerate([(metal_color,"Trilha Metálica"),(wood_color,"Trilha Madeira"),(single_color,"Montagem/Embalagem")]):
            iy = ly + 30 + li * 17
            parts.append(f'<line x1="{lx}" y1="{iy}" x2="{lx+22}" y2="{iy}" stroke="{color}" stroke-width="3"/>')
            parts.append(f'<text x="{lx+28}" y="{iy+4}" font-size="10" fill="#222">{label}</text>')

    parts.append("</svg>")
    return "\n".join(parts)


def write_render_assets(results: dict[str, Any], project: dict[str, Any]) -> None:
    render_dir = ROOT / "06_dashboard" / "renders"
    render_dir.mkdir(parents=True, exist_ok=True)

    (render_dir / "fluxograma_render.svg").write_text(
        build_flowchart_svg(results), encoding="utf-8"
    )

    (render_dir / "layout_render.svg").write_text(
        build_layout_svg(results, project, with_flow=False), encoding="utf-8"
    )
    (render_dir / "mapofluxograma_render.svg").write_text(
        build_layout_svg(results, project, with_flow=True), encoding="utf-8"
    )


def markdown_to_html(markdown: str) -> str:
    html: list[str] = []
    in_ul = False
    in_pre = False
    table_buffer: list[str] = []

    def flush_ul() -> None:
        nonlocal in_ul
        if in_ul:
            html.append("</ul>")
            in_ul = False

    def flush_table() -> None:
        nonlocal table_buffer
        if not table_buffer:
            return
        rows = [row.strip().strip("|").split("|") for row in table_buffer if row.strip()]
        if len(rows) >= 2 and all(set(cell.strip()) <= {"-", ":"} for cell in rows[1]):
            html.append("<table>")
            html.append("<thead><tr>" + "".join(f"<th>{escape(cell.strip())}</th>" for cell in rows[0]) + "</tr></thead>")
            html.append("<tbody>")
            for row in rows[2:]:
                html.append("<tr>" + "".join(f"<td>{escape(cell.strip())}</td>" for cell in row) + "</tr>")
            html.append("</tbody></table>")
        else:
            for row in table_buffer:
                html.append(f"<p>{escape(row)}</p>")
        table_buffer = []

    for raw in markdown.splitlines():
        line = raw.rstrip()
        if line.startswith("```"):
            flush_table()
            flush_ul()
            if in_pre:
                html.append("</code></pre>")
                in_pre = False
            else:
                html.append("<pre><code>")
                in_pre = True
            continue
        if in_pre:
            html.append(escape(line) + "\n")
            continue
        if line.startswith("|"):
            flush_ul()
            table_buffer.append(line)
            continue
        flush_table()
        if not line.strip():
            flush_ul()
            continue
        if line.startswith("# "):
            flush_ul()
            html.append(f"<h1>{escape(line[2:].strip())}</h1>")
        elif line.startswith("## "):
            flush_ul()
            html.append(f"<h2>{escape(line[3:].strip())}</h2>")
        elif line.startswith("### "):
            flush_ul()
            html.append(f"<h3>{escape(line[4:].strip())}</h3>")
        elif line.startswith("- "):
            if not in_ul:
                html.append("<ul>")
                in_ul = True
            html.append(f"<li>{escape(line[2:].strip())}</li>")
        elif len(line) > 2 and line[0].isdigit() and ". " in line[:4]:
            flush_ul()
            html.append(f"<p>{escape(line)}</p>")
        else:
            flush_ul()
            html.append(f"<p>{escape(line)}</p>")
    flush_table()
    flush_ul()
    if in_pre:
        html.append("</code></pre>")
    return "\n".join(html)


def write_html_page(slug: str, title: str, body: str, actions: list[tuple[str, str, bool]] | None = None) -> str:
    pages_dir = ROOT / "06_dashboard" / "entregaveis"
    pages_dir.mkdir(parents=True, exist_ok=True)
    actions = actions or []
    action_html = "\n".join(
        f"<a href='{escape(href)}'{(' download' if download else '')}>{escape(label)}</a>"
        for label, href, download in actions
    )
    html = f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)} - Projeto Tramontina</title>
  <style>
    body {{ margin:0; font-family:Arial, Helvetica, sans-serif; color:#17212b; background:#ffffff; }}
    header {{ padding:24px clamp(20px,4vw,56px); background:#f8fafc; border-bottom:1px solid #d7dde5; }}
    main {{ padding:28px clamp(20px,4vw,56px) 48px; max-width:1320px; margin:0 auto; }}
    h1 {{ margin:0 0 8px; font-size:34px; letter-spacing:0; }}
    h2 {{ margin:28px 0 12px; font-size:23px; }}
    h3 {{ margin:22px 0 8px; font-size:18px; }}
    p, li {{ line-height:1.48; }}
    a {{ color:#17212b; }}
    .actions {{ display:flex; flex-wrap:wrap; gap:8px; margin-top:14px; }}
    .actions a, .back {{ display:inline-block; text-decoration:none; border:1px solid #d7dde5; padding:8px 11px; background:#fff; }}
    .render {{ width:100%; max-height:720px; object-fit:contain; border:1px solid #d7dde5; background:#f8fafc; }}
    table {{ width:100%; border-collapse:collapse; margin:12px 0 18px; font-size:14px; }}
    th, td {{ border:1px solid #d7dde5; padding:8px 10px; text-align:left; vertical-align:top; }}
    th {{ background:#edf2f7; }}
    pre {{ white-space:pre-wrap; background:#f8fafc; border:1px solid #d7dde5; padding:12px; overflow:auto; }}
    .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:14px; }}
    .card {{ border:1px solid #d7dde5; padding:14px; }}
    .note {{ color:#5d6977; }}
  </style>
</head>
<body>
  <header>
    <a class="back" href="../index.html">Voltar para a central</a>
    <h1>{escape(title)}</h1>
    <div class="actions">{action_html}</div>
  </header>
  <main>{body}</main>
</body>
</html>
"""
    output = pages_dir / f"{slug}.html"
    output.write_text(html, encoding="utf-8")
    return f"entregaveis/{slug}.html"


def render_objectives_page(results: dict[str, Any]) -> str:
    objectives = results.get("project_objectives", [])
    items_html = "\n".join(f"<li>{escape(obj)}</li>" for obj in objectives)
    body = f"""
<h2>Objetivos do Projeto</h2>
<p>Projeto de fábrica para o <strong>{escape(results['product']['name'])}</strong> (ref. {escape(results['product']['sku'])}) — UFF, Niterói.</p>
<ul>{items_html}</ul>
"""
    return write_html_page(
        "objetivos",
        "Objetivos do Projeto",
        body,
        [("Baixar OBJETIVO.md", "../../OBJETIVO.md", True)],
    )


def render_market_page(results: dict[str, Any]) -> str:
    segments = results.get("market_segments", [])
    cards_html = ""
    for seg in segments:
        cards_html += f"""
<div class="card">
  <h3>{escape(seg['name'])}</h3>
  <p><strong>Descrição:</strong> {escape(seg['description'])}</p>
  <p><strong>Justificativa:</strong> {escape(seg['justification'])}</p>
</div>"""
    body = f"""
<h2>Segmentos de Mercado Visados</h2>
<p>Justificativa da meta de 1.000 kits bons/semana e seleção dos principais canais de venda.</p>
<div class="grid">{cards_html}</div>
"""
    return write_html_page(
        "mercado",
        "Segmentos de Mercado",
        body,
    )


def render_conclusions_page(results: dict[str, Any]) -> str:
    c = results.get("conclusions", {})
    improvements_html = "\n".join(
        f"<li>{escape(item)}</li>" for item in c.get("improvements", [])
    )
    body = f"""
<h2>Conclusões</h2>
<h3>Resumo dos Resultados</h3>
<p>{escape(c.get('summary', ''))}</p>
<h3>Gargalo Identificado</h3>
<p>{escape(c.get('bottleneck_note', ''))}</p>
<h3>Observação sobre o Layout</h3>
<p>{escape(c.get('layout_note', ''))}</p>
<h3>O que Seria Necessário para Aprimorar o Projeto</h3>
<ul>{improvements_html}</ul>
"""
    return write_html_page(
        "conclusoes",
        "Conclusões",
        body,
    )


def write_deliverable_pages(results: dict[str, Any]) -> dict[str, str]:
    pages: dict[str, str] = {}
    root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
    pages["readme"] = write_html_page(
        "readme",
        "README geral",
        markdown_to_html(root_readme),
        [("Baixar README.md", "../../README.md", True)],
    )
    roteiro = (ROOT / "01_apresentacao" / "roteiro_slides.md").read_text(encoding="utf-8")
    pages["roteiro"] = write_html_page(
        "roteiro",
        "Roteiro da apresentação",
        markdown_to_html(roteiro),
        [("Baixar roteiro .md", "../../01_apresentacao/roteiro_slides.md", True)],
    )
    memoria = (ROOT / "02_calculos" / "memoria_calculo_transparente.md").read_text(encoding="utf-8")
    pages["memoria"] = write_html_page(
        "memoria",
        "Memória de cálculo",
        markdown_to_html(memoria),
        [("Abrir Excel editável", "../../02_calculos/demonstrativo_calculos.xlsx", False), ("Baixar memória .md", "../../02_calculos/memoria_calculo_transparente.md", True)],
    )
    calc_rows = "\n".join(
        f"<tr><td>{escape(row['type'])}</td><td>{escape(row['supplier'])}</td><td>{row['nominal_rate_kits_per_hour']:.0f}</td><td>{row['weekly_capacity_per_machine']:.0f}</td><td>{row['required_quantity']}</td><td>{row['utilization']:.1%}</td></tr>"
        for row in results["equipment_capacity"]
    )
    material_rows = "\n".join(
        f"<tr><td>{escape(row['item'])}</td><td>{row['purchase_g_per_kit']:.1f} g/kit</td><td>{row['purchase_kg_per_week']:.1f} kg/semana</td><td>{escape(row['source'])}</td></tr>"
        for row in results["materials"]
    )
    pages["calculos"] = write_html_page(
        "calculos",
        "Excel de cálculos",
        f"""
        <p class="note">Frente HTML do demonstrativo. O arquivo editável continua no Excel.</p>
        <div class="grid">
          <div class="card"><h3>Meta boa</h3><p>{results['demand']['target_good_kits_per_week']:.0f} kits/semana</p></div>
          <div class="card"><h3>Demanda bruta</h3><p>{results['demand']['input_kits_per_week']:.0f} kits/semana</p></div>
          <div class="card"><h3>Horas úteis</h3><p>{results['demand']['useful_hours_per_week']:.1f} h/semana</p></div>
          <div class="card"><h3>Router CNC</h3><p>{results['selected_equipment_detail']['required_quantity']} unidade(s)</p></div>
        </div>
        <h2>Capacidade por equipamento</h2>
        <table><thead><tr><th>Equipamento</th><th>Fornecedor</th><th>Taxa nominal</th><th>Capacidade semanal</th><th>Qtd.</th><th>Utilização</th></tr></thead><tbody>{calc_rows}</tbody></table>
        <h2>Consumo estimado de materiais</h2>
        <table><thead><tr><th>Material</th><th>Consumo por kit</th><th>Consumo semanal</th><th>Base</th></tr></thead><tbody>{material_rows}</tbody></table>
        """,
        [("Abrir Excel editável", "../../02_calculos/demonstrativo_calculos.xlsx", False)],
    )
    pages["fluxograma"] = write_html_page(
        "fluxograma",
        "Fluxograma renderizado",
        "<img class='render' src='../renders/fluxograma_render.svg' alt='Fluxograma renderizado'>",
        [("Baixar .drawio editável", "../../03_diagramas/fluxograma_processo.drawio", True), ("Abrir SVG", "../renders/fluxograma_render.svg", False)],
    )
    pages["layout"] = write_html_page(
        "layout",
        "Layout esquemático renderizado",
        "<img class='render' src='../renders/layout_render.svg' alt='Layout esquemático renderizado'>",
        [("Baixar .drawio editável", "../../03_diagramas/layout_esquematico.drawio", True), ("Abrir SVG", "../renders/layout_render.svg", False)],
    )
    pages["mapofluxograma"] = write_html_page(
        "mapofluxograma",
        "Mapofluxograma renderizado",
        "<img class='render' src='../renders/mapofluxograma_render.svg' alt='Mapofluxograma renderizado'>",
        [("Baixar .drawio editável", "../../03_diagramas/mapofluxograma.drawio", True), ("Abrir SVG", "../renders/mapofluxograma_render.svg", False)],
    )
    contexto = (ROOT / "05_base_tecnica" / "contexto_produto_tramontina_22399036.md").read_text(encoding="utf-8")
    pages["contexto"] = write_html_page(
        "contexto-produto",
        "Contexto do produto",
        markdown_to_html(contexto),
        [("Baixar contexto .md", "../../05_base_tecnica/contexto_produto_tramontina_22399036.md", True)],
    )
    fontes = (ROOT / "05_base_tecnica" / "fontes_pesquisa_e_premissas.md").read_text(encoding="utf-8")
    pages["fontes"] = write_html_page(
        "fontes-premissas",
        "Fontes e premissas",
        markdown_to_html(fontes),
        [("Baixar fontes .md", "../../05_base_tecnica/fontes_pesquisa_e_premissas.md", True)],
    )
    revisao = (ROOT / "05_base_tecnica" / "revisao_plano_e_pontos_fracos.md").read_text(encoding="utf-8")
    pages["revisao"] = write_html_page(
        "revisao-plano",
        "Revisão crítica do plano",
        markdown_to_html(revisao),
        [("Baixar revisão .md", "../../05_base_tecnica/revisao_plano_e_pontos_fracos.md", True)],
    )
    pages["objetivos"] = render_objectives_page(results)
    pages["mercado"] = render_market_page(results)
    pages["conclusoes"] = render_conclusions_page(results)
    return pages


def write_dashboard(results: dict[str, Any]) -> None:
    dashboard = ROOT / "06_dashboard" / "index.html"
    product = results["product"]
    demand = results["demand"]
    layout = results["layout"]
    selected = results["selected_equipment_detail"]
    members = [member["name"] for member in results.get("metadata", {}).get("group_members", [])]
    pending_member_note = results.get("metadata", {}).get("pending_member_note", "")
    pages = write_deliverable_pages(results)

    equipment_rows = "\n".join(
        f"<tr><td>{escape(row['type'])}</td><td>{escape(row['supplier'])}</td><td>{row['nominal_rate_kits_per_hour']:.0f}</td><td>{row['weekly_capacity_per_machine']:.0f}</td><td>{row['required_quantity']}</td><td>{row['utilization']:.0%}</td></tr>"
        for row in results["equipment_capacity"]
    )
    bom_rows = "\n".join(
        f"<tr><td>{escape(row['component'])}</td><td>{row['quantity']}</td><td>{escape(row['unit'])}</td><td>{escape(row['make_or_buy'])}</td></tr>"
        for row in results["bom"]
    )
    bars = "\n".join(
        f"<div class='bar-row'><span>{escape(row['type'])}</span><div class='bar'><i style='width:{min(100, row['utilization']*100):.0f}%'></i></div><b>{row['required_quantity']}x</b></div>"
        for row in results["equipment_capacity"]
    )
    source_links = "\n".join(
        f"<li><a href='{escape(str(source.get('url_or_path', '#')))}'>{escape(source.get('title', sid))}</a></li>"
        for sid, source in results["sources"].items()
        if source.get("url_or_path", "").startswith("http")
    )
    members_html = "\n".join(f"<li>{escape(name)}</li>" for name in members)
    pending_html = f"<p class='note'>{escape(pending_member_note)}</p>" if pending_member_note else ""
    product_cards = [
        {
            "title": "Kit principal",
            "image": "../04_fontes/assets_tramontina/22399036_produto_principal_G.jpg",
            "text": "Produto vendido: kit churrasco com faca, garfo, tábua e embalagem.",
            "link": "../04_fontes/assets_tramontina/22399036_produto_principal_G.jpg",
        },
        {
            "title": "Kit aberto",
            "image": "../04_fontes/assets_tramontina/22399036_item_aberto_G.jpg",
            "text": "Visão dos itens fora da embalagem, útil para estrutura pai-filho.",
            "link": "../04_fontes/assets_tramontina/22399036_item_aberto_G.jpg",
        },
        {
            "title": "Embalagem",
            "image": "../04_fontes/assets_tramontina/22399036_embalagem_G.jpg",
            "text": f"{product['package_dimensions_cm']['height']} x {product['package_dimensions_cm']['width']} x {product['package_dimensions_cm']['length']} cm; {product['package_weight_kg']} kg.",
            "link": "../04_fontes/assets_tramontina/22399036_embalagem_G.jpg",
        },
        {
            "title": "Desenho técnico",
            "image": "../04_fontes/assets_tramontina/22399036_desenho_tecnico.jpg",
            "text": "Base visual para dimensões e desenho técnico no trabalho.",
            "link": "../04_fontes/assets_tramontina/22399036_desenho_tecnico.jpg",
        },
        {
            "title": "Faca chef 8 pol.",
            "image": "../04_fontes/assets_tramontina/22315008_faca_chef_8.jpg",
            "text": "Item filho 22315008; lâmina em aço inox, cabo de madeira e rebites.",
            "link": "../04_fontes/assets_tramontina/22315008_faca_chef_8.jpg",
        },
        {
            "title": "Garfo trinchante",
            "image": "../04_fontes/assets_tramontina/22330000_garfo_trinchante.jpg",
            "text": "Item filho 22330000; peça metálica com cabo de madeira.",
            "link": "../04_fontes/assets_tramontina/22330000_garfo_trinchante.jpg",
        },
        {
            "title": "Tábua retangular",
            "image": "../04_fontes/assets_tramontina/13102152_tabua_retangular.jpg",
            "text": "Item filho 13102152; madeira Maçaranduba com acabamento natural.",
            "link": "../04_fontes/assets_tramontina/13102152_tabua_retangular.jpg",
        },
    ]
    product_gallery = "\n".join(
        f"<a class='media-card' href='{escape(card['link'])}'><img src='{escape(card['image'])}' alt='{escape(card['title'])}'><strong>{escape(card['title'])}</strong><span>{escape(card['text'])}</span></a>"
        for card in product_cards
    )
    deliverables = [
        ("README geral", pages["readme"], "Mapa do pacote e resumo dos resultados"),
        ("Roteiro da apresentação", pages["roteiro"], "Estrutura para montar os slides no fim"),
        ("Excel de cálculos", pages["calculos"], "Frente HTML do workbook com link para o editável"),
        ("Memória de cálculo", pages["memoria"], "Texto renderizado com fórmulas, entradas e resultados"),
        ("Fluxograma", pages["fluxograma"], "Diagrama renderizado do processo"),
        ("Layout esquemático", pages["layout"], "Arranjo físico renderizado"),
        ("Mapofluxograma", pages["mapofluxograma"], "Fluxo renderizado sobre o layout"),
        ("Contexto do produto", pages["contexto"], "Dados extraídos da página da Tramontina"),
        ("Fontes e premissas", pages["fontes"], "Rastreabilidade das fontes pesquisadas"),
        ("Revisão crítica do plano", pages["revisao"], "Riscos, lacunas e correções de rota"),
        ("Objetivos do Projeto", pages["objetivos"], "5 objetivos do projeto básico de fábrica"),
        ("Segmentos de Mercado", pages["mercado"], "4 segmentos com justificativa"),
        ("Conclusões", pages["conclusoes"], "Gargalo, layout, melhorias"),
    ]
    deliverable_cards = "\n".join(
        f"<a class='deliverable' href='{escape(href)}'><strong>{escape(title)}</strong><span>{escape(desc)}</span></a>"
        for title, href, desc in deliverables
    )
    technical_files = [
        ("Base de entradas", "../data/projeto.json"),
        ("Resultados calculados", "../data/resultados_calculo.json"),
        ("Script principal", "../scripts/generate_outputs.py"),
        ("Builder do Excel", "../scripts/build_workbook.mjs"),
        ("Regenerar pacote", "../scripts/run_all.ps1"),
        ("Prints da página", "../04_fontes/prints_tramontina/01_topo_produto_preco.png"),
        ("Folheto oficial PDF", "../04_fontes/assets_tramontina/21198770_folheto.pdf"),
    ]
    technical_links = "\n".join(
        f"<li><a href='{escape(href)}'>{escape(title)}</a></li>" for title, href in technical_files
    )
    render_cards = "\n".join(
        [
            f"<article class='render-card'><a href='{pages['fluxograma']}'><img src='renders/fluxograma_render.svg' alt='Fluxograma renderizado'></a><div><h3>Fluxograma renderizado</h3><p>Sequência completa dos 26 processos com cores por tipo.</p><a href='{pages['fluxograma']}'>Abrir frente renderizada</a></div></article>",
            f"<article class='render-card'><a href='{pages['layout']}'><img src='renders/layout_render.svg' alt='Layout esquemático renderizado'></a><div><h3>Layout renderizado</h3><p>Arranjo físico com áreas de recebimento, metal, madeira, montagem, inspeção e expedição.</p><a href='{pages['layout']}'>Abrir frente renderizada</a></div></article>",
            f"<article class='render-card'><a href='{pages['mapofluxograma']}'><img src='renders/mapofluxograma_render.svg' alt='Mapofluxograma renderizado'></a><div><h3>Mapofluxograma renderizado</h3><p>Fluxo macro sobre o layout, conectando recebimento, produção, inspeção e expedição.</p><a href='{pages['mapofluxograma']}'>Abrir frente renderizada</a></div></article>",
        ]
    )
    process_rows = "\n".join(
        f"<tr><td>{process['number']}</td><td>{escape(process['name'])}</td><td><span class='tag tag-{escape(process['type'])}'>{escape(PROCESS_LABELS.get(process['type'], process['type']))}</span></td><td>{escape(process.get('resources', process.get('resource', '')))}</td></tr>"
        for process in results["processes"]
    )
    process_flow = "\n".join(
        f"<div class='flow-node type-{escape(process['type'])}'><b>{process['number']}</b><span>{escape(process['name'])}</span></div>"
        for process in results["processes"]
    )
    material_rows = "\n".join(
        f"<tr><td>{escape(row['item'])}</td><td>{row['purchase_g_per_kit']:.1f} g/kit</td><td>{row['purchase_kg_per_week']:.1f} kg/sem.</td><td>{escape(row['source'])}</td></tr>"
        for row in results["materials"]
    )
    selected_calc_rows = "\n".join(
        [
            f"<tr><td>Demanda bruta</td><td>{demand['input_kits_per_week']:.0f} kits/semana</td><td>ceil({demand['target_good_kits_per_week']:.0f} / {demand['final_good_yield']:.2f})</td></tr>",
            f"<tr><td>Horas úteis</td><td>{demand['useful_hours_per_week']:.1f} h/semana</td><td>{demand['work_days_per_week']} dias * {demand['shifts_per_day']} turno * {results['premises']['useful_hours_per_shift']} h</td></tr>",
            f"<tr><td>Taxa nominal</td><td>{selected['nominal_rate_used']:.2f} kits/h</td><td>3600 / {selected['standard_time_seconds_per_kit']:.0f} s</td></tr>",
            f"<tr><td>Taxa efetiva</td><td>{selected['effective_rate_kits_per_hour']:.2f} kits/h</td><td>nominal * eficiência * confiabilidade * rendimento</td></tr>",
            f"<tr><td>Capacidade semanal por máquina</td><td>{selected['weekly_capacity_per_machine']:.2f} kits/semana</td><td>taxa efetiva * horas úteis</td></tr>",
            f"<tr><td>Quantidade necessária</td><td>{selected['required_quantity']} unidade(s)</td><td>ceil(demanda bruta / capacidade por máquina)</td></tr>",
            f"<tr><td>Utilização estimada</td><td>{selected['utilization']:.1%}</td><td>demanda / (quantidade * capacidade)</td></tr>",
        ]
    )
    layout_cards = "\n".join(
        f"<div class='zone' style='left:{zone['x_m'] / 24 * 100:.2f}%;top:{zone['y_m'] / 16 * 100:.2f}%;width:{zone['w_m'] / 24 * 100:.2f}%;height:{zone['h_m'] / 16 * 100:.2f}%;background:{zone['fill']}'>{escape(zone['name'])}</div>"
        for zone in layout_zones()
    )
    flow_points = [
        ("1-2", 95, 170),
        ("3-10", 405, 200),
        ("11-17", 760, 200),
        ("18-22", 460, 485),
        ("23", 790, 430),
        ("24-26", 130, 485),
    ]
    map_points = "\n".join(
        f"<div class='map-point' style='left:{(x - 30) / 910 * 100:.2f}%;top:{(y - 70) / 540 * 100:.2f}%'>{escape(label)}</div>"
        for label, x, y in flow_points
    )
    polyline_points = " ".join(f"{x + 37 - 30},{y + 24 - 70}" for _, x, y in flow_points)
    source_rows = "\n".join(
        f"<tr><td>{escape(row['source_id'])}</td><td>{escape(str(row.get('topic', row.get('fact', ''))))}</td><td>{escape(str(row.get('data', row.get('use', row.get('used_in', '')))))}</td><td>{escape(str(row.get('confidence', '')))}</td></tr>"
        for row in results["research_matrix"]
    )

    html = f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Projeto de Fábrica - Tramontina 22399036</title>
  <style>
    :root {{
      --ink:#17212b; --muted:#5d6977; --line:#d7dde5; --paper:#f8fafc;
      --green:#2f7d57; --blue:#315f9f; --gold:#b07820; --red:#a63d40; --soft:#fff8ef;
    }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; font-family:Arial, Helvetica, sans-serif; color:var(--ink); background:#ffffff; }}
    nav {{ position:sticky; top:0; z-index:3; display:flex; gap:8px; flex-wrap:wrap; padding:10px clamp(20px,4vw,56px); border-bottom:1px solid var(--line); background:rgba(255,255,255,.96); }}
    nav a {{ color:var(--ink); text-decoration:none; border:1px solid var(--line); padding:7px 10px; font-size:13px; background:#fff; }}
    header {{ display:grid; grid-template-columns:minmax(260px, 1.05fr) minmax(260px, .95fr); gap:28px; padding:34px clamp(20px,4vw,56px); border-bottom:1px solid var(--line); background:var(--paper); }}
    h1 {{ margin:0 0 10px; font-size:clamp(26px,3.2vw,44px); line-height:1.08; letter-spacing:0; }}
    h2 {{ margin:0 0 14px; font-size:22px; }}
    h3 {{ margin:0 0 8px; font-size:15px; color:var(--muted); text-transform:uppercase; letter-spacing:.04em; }}
    p {{ line-height:1.45; }}
    img.product {{ width:100%; max-height:340px; object-fit:contain; background:#fff; border:1px solid var(--line); }}
    main {{ padding:28px clamp(20px,4vw,56px) 48px; }}
    section {{ margin:0 0 32px; }}
    .kpis {{ display:grid; grid-template-columns:repeat(5,minmax(150px,1fr)); gap:12px; }}
    .kpi {{ border-left:5px solid var(--blue); padding:14px 16px; background:#fff; border-top:1px solid var(--line); border-right:1px solid var(--line); border-bottom:1px solid var(--line); }}
    .kpi:nth-child(2) {{ border-left-color:var(--green); }}
    .kpi:nth-child(3) {{ border-left-color:var(--gold); }}
    .kpi:nth-child(4) {{ border-left-color:var(--red); }}
    .kpi b {{ display:block; font-size:24px; margin-top:4px; }}
    .grid {{ display:grid; grid-template-columns:minmax(280px,.9fr) minmax(360px,1.1fr); gap:24px; align-items:start; }}
    .three-grid {{ display:grid; grid-template-columns:repeat(3,minmax(220px,1fr)); gap:18px; align-items:start; }}
    .wide-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:14px; }}
    .media-card, .deliverable {{ display:flex; flex-direction:column; min-height:100%; color:var(--ink); text-decoration:none; border:1px solid var(--line); background:#fff; }}
    .media-card img {{ width:100%; aspect-ratio:4/3; object-fit:contain; background:#f7f7f7; border-bottom:1px solid var(--line); }}
    .media-card strong, .deliverable strong {{ display:block; padding:12px 12px 4px; font-size:15px; }}
    .media-card span, .deliverable span {{ display:block; padding:0 12px 12px; color:var(--muted); font-size:13px; line-height:1.35; }}
    .deliverable {{ min-height:96px; border-left:5px solid var(--blue); }}
    .deliverable:nth-child(3n+2) {{ border-left-color:var(--green); }}
    .deliverable:nth-child(3n) {{ border-left-color:var(--gold); }}
    .render-grid {{ display:grid; grid-template-columns:repeat(3,minmax(250px,1fr)); gap:18px; }}
    .render-card {{ border:1px solid var(--line); background:#fff; }}
    .render-card img {{ display:block; width:100%; aspect-ratio:16/10; object-fit:contain; background:#f8fafc; border-bottom:1px solid var(--line); }}
    .render-card div {{ padding:14px; }}
    .render-card h3 {{ color:var(--ink); text-transform:none; letter-spacing:0; font-size:18px; margin-bottom:8px; }}
    .render-card a {{ display:inline-block; color:var(--ink); text-decoration:none; border:1px solid var(--line); background:#fff; padding:7px 10px; font-size:13px; }}
    .tree {{ display:grid; gap:8px; padding:14px; border:1px solid var(--line); background:var(--soft); }}
    .tree b, .tree span {{ display:block; padding:9px 10px; border:1px solid var(--line); background:#fff; }}
    .tree .children {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(160px,1fr)); gap:8px; }}
    .file-list {{ columns:2 260px; line-height:1.65; }}
    .front {{ border:1px solid var(--line); background:#fff; padding:18px; }}
    .front h3 {{ color:var(--ink); text-transform:none; letter-spacing:0; font-size:18px; margin-bottom:10px; }}
    .front-actions {{ display:flex; flex-wrap:wrap; gap:8px; margin-top:12px; }}
    .front-actions a {{ color:var(--ink); text-decoration:none; border:1px solid var(--line); background:#fff; padding:7px 10px; font-size:13px; }}
    .tag {{ display:inline-block; padding:3px 7px; border:1px solid var(--line); font-size:12px; background:#fff; }}
    .tag-operacao, .type-operacao {{ background:#D9EAD3; }}
    .tag-transporte, .type-transporte {{ background:#D9EAF7; }}
    .tag-inspecao, .type-inspecao {{ background:#FFF2CC; }}
    .tag-armazenagem, .type-armazenagem {{ background:#EADCF8; }}
    .tag-espera, .type-espera {{ background:#F4CCCC; }}
    .flow-strip {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(140px,1fr)); gap:10px; }}
    .flow-node {{ min-height:88px; padding:10px; border:1px solid #9ca3af; }}
    .flow-node b {{ display:block; font-size:18px; }}
    .flow-node span {{ display:block; font-size:12px; line-height:1.25; }}
    .layout-preview {{ position:relative; width:100%; aspect-ratio:24/16; min-height:320px; border:2px solid #334155; background:#f8fafc; overflow:hidden; }}
    .zone {{ position:absolute; display:flex; align-items:center; justify-content:center; text-align:center; padding:6px; border:1px solid #334155; font-size:12px; font-weight:bold; }}
    .map-point {{ position:absolute; transform:translate(-50%,-50%); z-index:2; min-width:52px; padding:7px 8px; text-align:center; border:2px solid #111827; background:#fff; font-weight:bold; font-size:12px; }}
    .map-svg {{ position:absolute; inset:0; width:100%; height:100%; pointer-events:none; }}
    .scroll-table {{ overflow:auto; border:1px solid var(--line); }}
    .scroll-table table {{ min-width:760px; }}
    table {{ width:100%; border-collapse:collapse; font-size:14px; }}
    th, td {{ border:1px solid var(--line); padding:9px 10px; text-align:left; vertical-align:top; }}
    th {{ background:#edf2f7; }}
    .bar-row {{ display:grid; grid-template-columns:190px 1fr 42px; gap:10px; align-items:center; margin:9px 0; font-size:13px; }}
    .bar {{ height:13px; background:#e9edf2; border:1px solid #d6dde6; }}
    .bar i {{ display:block; height:100%; background:linear-gradient(90deg,var(--green),var(--gold)); }}
    .note {{ color:var(--muted); font-size:14px; }}
    code {{ background:#edf2f7; padding:2px 5px; border-radius:4px; }}
    .formula {{ border:1px solid var(--line); padding:14px 16px; background:#fbfbfd; }}
    @media (max-width: 900px) {{
      header, .grid, .three-grid, .render-grid {{ grid-template-columns:1fr; }}
      .kpis {{ grid-template-columns:repeat(2,minmax(140px,1fr)); }}
    }}
    @media (max-width: 560px) {{
      .kpis {{ grid-template-columns:1fr; }}
      .bar-row {{ grid-template-columns:1fr; }}
    }}
  </style>
</head>
<body>
  <nav>
    <a href="#produtos">Produtos</a>
    <a href="#entregaveis">Entregáveis</a>
    <a href="#renders">Renderizações</a>
    <a href="#fronts">Frentes</a>
    <a href="#calculos">Cálculos</a>
    <a href="#tabela-processos">Processos</a>
    <a href="#layout">Layout</a>
    <a href="#fontes">Fontes</a>
  </nav>
  <header>
    <div>
      <h3>Projeto de fábrica</h3>
      <h1>{escape(product['name'])}</h1>
      <p>{escape(product['official_description_short'])}</p>
      <p class="note">SKU {escape(product['sku'])} · Embalagem {product['package_dimensions_cm']['height']} x {product['package_dimensions_cm']['width']} x {product['package_dimensions_cm']['length']} cm · {product['package_weight_kg']} kg.</p>
      <h3>Integrantes</h3>
      <ul>{members_html}</ul>
      {pending_html}
    </div>
    <img class="product" src="../04_fontes/assets_tramontina/22399036_produto_principal_G.jpg" alt="Produto Tramontina 22399036">
  </header>
  <main>
    <section id="entregaveis">
      <h2>Central de entregáveis</h2>
      <div class="wide-grid">{deliverable_cards}</div>
    </section>
    <section id="renders">
      <h2>Renderizações dos entregáveis</h2>
      <div class="render-grid">{render_cards}</div>
    </section>
    <section id="produtos">
      <h2>Produto, componentes e embalagem</h2>
      <div class="wide-grid">{product_gallery}</div>
    </section>
    <section class="grid">
      <div>
        <h2>Estrutura pai-filho</h2>
        <div class="tree">
          <b>Kit 22399036 embalado para envio</b>
          <div class="children">
            <span>Faca chef 8 pol.</span>
            <span>Garfo trinchante</span>
            <span>Tábua retangular</span>
            <span>Cartela/cinta</span>
            <span>Blister/suporte</span>
            <span>Etiqueta e caixa</span>
          </div>
        </div>
      </div>
      <div>
        <h2>Arquivos técnicos</h2>
        <ul class="file-list">{technical_links}</ul>
      </div>
    </section>
    <section id="fronts">
      <h2>Frentes visuais dos entregáveis</h2>
      <div class="three-grid">
        <article class="front">
          <h3>Descrição do produto</h3>
          <p>{escape(product['official_description_short'])}</p>
          <p class="note">Materiais: {escape('; '.join(product['official_materials']))}</p>
          <div class="front-actions"><a href="{pages['contexto']}">Abrir contexto renderizado</a><a href="../04_fontes/assets_tramontina/22399036_desenho_tecnico.jpg">Desenho técnico</a></div>
        </article>
        <article class="front">
          <h3>Tabela 1 - BOM</h3>
          <p>{len(results['bom'])} itens, separando fazer/comprar para uma unidade embalada para envio.</p>
          <div class="front-actions"><a href="#bom">Ver tabela</a><a href="{pages['calculos']}">Abrir frente dos cálculos</a></div>
        </article>
        <article class="front">
          <h3>Tabela 2 - Processos</h3>
          <p>{len(results['processes'])} processos classificados em operação, transporte, inspeção, armazenagem e espera.</p>
          <div class="front-actions"><a href="#tabela-processos">Ver tabela</a><a href="{pages['fluxograma']}">Abrir fluxograma renderizado</a></div>
        </article>
        <article class="front">
          <h3>Tabela 3 - Equipamentos</h3>
          <p>{len(results['equipment_capacity'])} recursos principais dimensionados com eficiência, confiabilidade e rendimento.</p>
          <div class="front-actions"><a href="#equipamentos">Ver capacidade</a><a href="{pages['calculos']}">Abrir frente dos cálculos</a></div>
        </article>
        <article class="front">
          <h3>Cálculo do equipamento</h3>
          <p>{escape(selected['supplier'])} {escape(selected['model'])}: {selected['required_quantity']} unidade(s) para atender a demanda.</p>
          <div class="front-actions"><a href="#calculo-detalhado">Ver memória</a><a href="{pages['memoria']}">Abrir memória renderizada</a></div>
        </article>
        <article class="front">
          <h3>Layout e mapofluxograma</h3>
          <p>Área proposta de {layout['layout_total_area_m2']:.0f} m², com ocupação estimada de {layout['occupancy']:.1%}.</p>
          <div class="front-actions"><a href="#layout">Ver layout</a><a href="{pages['mapofluxograma']}">Abrir mapofluxograma renderizado</a></div>
        </article>
      </div>
    </section>
    <section id="calculos" class="kpis">
      <div class="kpi">Meta boa semanal<b>{demand['target_good_kits_per_week']:.0f}</b></div>
      <div class="kpi">Demanda bruta<b>{demand['input_kits_per_week']:.0f}</b></div>
      <div class="kpi">Horas úteis/semana<b>{demand['useful_hours_per_week']:.1f}</b></div>
      <div class="kpi">Router CNC necessário<b>{selected['required_quantity']}x</b></div>
      <div class="kpi">Área ocupada estimada<b>{layout['total_required_area_m2']:.0f} m²</b></div>
    </section>
    <section id="bom" class="grid">
      <div>
        <h2>Estrutura do produto</h2>
        <table>
          <thead><tr><th>Componente</th><th>Qtd.</th><th>Un.</th><th>F/C</th></tr></thead>
          <tbody>{bom_rows}</tbody>
        </table>
      </div>
      <div>
        <h2>Capacidade por equipamento</h2>
        {bars}
      </div>
    </section>
    <section id="tabela-processos">
      <h2>Tabela 2 - Processos com tipos e recursos</h2>
      <div class="scroll-table">
        <table>
          <thead><tr><th>No.</th><th>Processo</th><th>Tipo</th><th>Recursos físicos</th></tr></thead>
          <tbody>{process_rows}</tbody>
        </table>
      </div>
    </section>
    <section>
      <h2>Fluxograma do processo</h2>
      <div class="flow-strip">{process_flow}</div>
      <div class="front-actions"><a href="{pages['fluxograma']}">Abrir frente do fluxograma</a></div>
    </section>
    <section id="equipamentos">
      <h2>Tabela de equipamentos</h2>
      <table>
        <thead><tr><th>Tipo</th><th>Fornecedor</th><th>Taxa nom. kit/h</th><th>Capacidade sem./máq.</th><th>Qtd.</th><th>Utilização</th></tr></thead>
        <tbody>{equipment_rows}</tbody>
      </table>
    </section>
    <section id="calculo-detalhado" class="grid">
      <div class="formula">
        <h2>Conta crítica</h2>
        <p><b>{escape(selected['supplier'])} {escape(selected['model'])}</b>: {escape(selected['reason'])}</p>
        <p><code>qtd = teto(demanda_bruta / (taxa_nominal * horas_úteis * eficiência * confiabilidade * rendimento))</code></p>
        <p>{selected['required_quantity']} unidade(s), com utilização estimada de {selected['utilization']:.1%}.</p>
        <table>
          <thead><tr><th>Item</th><th>Valor</th><th>Conta</th></tr></thead>
          <tbody>{selected_calc_rows}</tbody>
        </table>
      </div>
      <div class="formula">
        <h2>Arquivos transparentes</h2>
        <p>Entradas: <code>data/projeto.json</code></p>
        <p>Código de cálculo: <code>scripts/generate_outputs.py</code></p>
        <p>Resultados: <code>data/resultados_calculo.json</code> e <code>02_calculos/demonstrativo_calculos.xlsx</code></p>
      </div>
    </section>
    <section>
      <h2>Consumo estimado de materiais</h2>
      <table>
        <thead><tr><th>Material</th><th>Consumo por kit</th><th>Consumo semanal</th><th>Base</th></tr></thead>
        <tbody>{material_rows}</tbody>
      </table>
    </section>
    <section id="layout" class="grid">
      <div>
        <h2>Layout esquemático</h2>
        <div class="layout-preview">{layout_cards}</div>
        <div class="front-actions"><a href="{pages['layout']}">Abrir frente do layout</a></div>
      </div>
      <div>
        <h2>Mapofluxograma</h2>
        <div class="layout-preview">
          {layout_cards}
          <svg class="map-svg" viewBox="0 0 910 540" preserveAspectRatio="none">
            <polyline points="{polyline_points}" fill="none" stroke="#17212b" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>
          </svg>
          {map_points}
        </div>
        <div class="front-actions"><a href="{pages['mapofluxograma']}">Abrir frente do mapofluxograma</a></div>
      </div>
    </section>
    <section id="fontes">
      <h2>Fontes principais</h2>
      <ul>{source_links}</ul>
      <div class="scroll-table">
        <table>
          <thead><tr><th>ID</th><th>Tema</th><th>Dado / uso</th><th>Confiança</th></tr></thead>
          <tbody>{source_rows}</tbody>
        </table>
      </div>
    </section>
  </main>
</body>
</html>
"""
    dashboard.write_text(html, encoding="utf-8")


def main() -> None:
    project = load_project()
    results = build_results(project)
    write_json(results)
    write_sources_markdown(results)
    write_memory_markdown(results)
    write_slide_script(results)
    write_flowchart(results)
    write_layout(results, project)
    write_mapoflow(results, project)
    write_render_assets(results, project)
    write_dashboard(results)
    print(f"Generated outputs from {DATA_PATH}")
    print(f"Results: {RESULTS_PATH}")
    print(f"Selected equipment qty: {results['selected_equipment_detail']['required_quantity']}")


if __name__ == "__main__":
    main()
