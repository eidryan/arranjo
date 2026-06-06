import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "..");
const resultsPath = path.join(root, "data", "resultados_calculo.json");
const outputPath = path.join(root, "02_calculos", "demonstrativo_calculos.xlsx");

const results = JSON.parse(await fs.readFile(resultsPath, "utf8"));
const workbook = Workbook.create();

function colName(n) {
  let name = "";
  while (n > 0) {
    const r = (n - 1) % 26;
    name = String.fromCharCode(65 + r) + name;
    n = Math.floor((n - 1) / 26);
  }
  return name;
}

function rangeAddress(row, col, rows, cols) {
  return `${colName(col)}${row}:${colName(col + cols - 1)}${row + rows - 1}`;
}

function writeBlock(sheet, row, col, values) {
  if (!values.length || !values[0].length) return;
  sheet.getRange(rangeAddress(row, col, values.length, values[0].length)).values = values;
}

function writeFormulas(sheet, row, col, formulas) {
  if (!formulas.length || !formulas[0].length) return;
  sheet.getRange(rangeAddress(row, col, formulas.length, formulas[0].length)).formulas = formulas;
}

function addTitle(sheet, title, cols = 8) {
  writeBlock(sheet, 1, 1, [[title]]);
  sheet.getRange(rangeAddress(1, 1, 1, cols)).format = {
    fill: "#17212B",
    font: { name: "Arial", size: 14, color: "#FFFFFF", bold: true },
    verticalAlignment: "center",
    wrapText: true,
  };
}

function styleTable(sheet, startRow, startCol, rowCount, colCount) {
  const header = sheet.getRange(rangeAddress(startRow, startCol, 1, colCount));
  header.format = {
    fill: "#E7EEF7",
    font: { name: "Arial", size: 10, bold: true, color: "#17212B" },
    borders: { preset: "all", style: "thin", color: "#D1D5DB" },
    wrapText: true,
  };
  if (rowCount > 1) {
    sheet.getRange(rangeAddress(startRow + 1, startCol, rowCount - 1, colCount)).format = {
      font: { name: "Arial", size: 10, color: "#17212B" },
      borders: { preset: "all", style: "thin", color: "#E5E7EB" },
      wrapText: true,
      verticalAlignment: "top",
    };
  }
}

function pct(value) {
  return Number(value);
}

function num(value) {
  return Number(value);
}

function addPremissas() {
  const sheet = workbook.worksheets.add("Premissas");
  addTitle(sheet, "Premissas auditaveis do projeto", 5);
  const p = results.premises;
  const layoutDims = p.layout_total_dimensions_m ?? { length: p.layout_target_width_m, width: p.layout_target_length_m };
  const rows = [
    ["Parametro", "Valor", "Unidade", "Origem/observacao"],
    ["Meta semanal de produtos bons", p.target_good_kits_per_week, "kits bons/semana", "Premissa de projeto"],
    ["Rendimento final bom", p.final_good_yield, "%", "Premissa para perdas/refugos no fluxo completo"],
    ["Dias de trabalho por semana", p.work_days_per_week, "dias", "Premissa"],
    ["Turnos por dia", p.shifts_per_day, "turno", "Premissa"],
    ["Horas programadas por turno", p.scheduled_hours_per_shift, "h", "Premissa"],
    ["Horas uteis por turno", p.useful_hours_per_shift, "h", "Premissa descontando pausas/preparacoes"],
    ["Eficiencia geral", p.general_efficiency, "%", "Premissa aplicada aos equipamentos"],
    ["Confiabilidade dos equipamentos", p.equipment_reliability, "%", "Premissa aplicada aos equipamentos"],
    ["Rendimento padrao de processo", p.process_yield_default, "%", "Premissa aplicada aos equipamentos"],
    ["Fator de area de servico padrao", p.service_area_factor_default, "x footprint", "Premissa de layout"],
    ["Area total do layout", layoutDims.length * layoutDims.width, "m2", `${layoutDims.length} m x ${layoutDims.width} m`],
  ];
  writeBlock(sheet, 3, 1, rows);
  styleTable(sheet, 3, 1, rows.length, 4);
}

function addMembers() {
  const sheet = workbook.worksheets.add("Integrantes");
  addTitle(sheet, "Integrantes do grupo", 5);
  const rows = [["Nome", "Status", "Observacao"]];
  for (const member of results.metadata?.group_members ?? []) {
    rows.push([member.name, member.status, member.note ?? ""]);
  }
  if (results.metadata?.pending_member_note) {
    rows.push(["Pendente", "a confirmar", results.metadata.pending_member_note]);
  }
  writeBlock(sheet, 3, 1, rows);
  styleTable(sheet, 3, 1, rows.length, 3);
}

function addResumo() {
  const sheet = workbook.worksheets.add("Resumo");
  addTitle(sheet, "Resumo executivo - Projeto de fabrica Tramontina 22399036", 7);
  const rows = [
    ["Indicador", "Valor", "Formula / leitura"],
    ["Meta semanal de produtos bons", null, "Premissas!B4"],
    ["Demanda bruta para cobrir rendimento", null, "ROUNDUP(meta boa / rendimento final)"],
    ["Horas uteis por semana", null, "dias * turnos * horas uteis"],
    ["Ritmo medio necessario", null, "demanda bruta / horas uteis"],
    ["Equipamento detalhado", `${results.selected_equipment_detail.supplier} ${results.selected_equipment_detail.model}`, "Selecionado por risco de gargalo e repetibilidade"],
    ["Quantidade do equipamento detalhado", null, "Calculo_Router!B17"],
    ["Area requerida estimada", null, "Areas_Layout!B7"],
    ["Area total proposta", null, "Areas_Layout!B8"],
    ["Ocupacao estimada", null, "Areas_Layout!B10"],
  ];
  writeBlock(sheet, 3, 1, rows);
  writeFormulas(sheet, 4, 2, [["=Premissas!B4"], ["=ROUNDUP(Premissas!B4/Premissas!B5,0)"], ["=Premissas!B6*Premissas!B7*Premissas!B9"], ["=B5/B6"]]);
  writeFormulas(sheet, 9, 2, [["=Calculo_Router!B17"], ["=Areas_Layout!B7"], ["=Areas_Layout!B8"], ["=Areas_Layout!B10"]]);
  styleTable(sheet, 3, 1, rows.length, 3);
}

function addResearch() {
  const sheet = workbook.worksheets.add("Matriz_Pesquisa");
  addTitle(sheet, "Matriz de pesquisa: fato, fonte, uso e confianca", 7);
  const rows = [["Fonte", "Fato extraido", "Uso", "Confianca", "Observacao"]];
  for (const row of results.research_matrix) {
    const source = results.sources[row.source_id] ?? {};
    rows.push([
      source.title ?? row.source_id,
      row.fact ?? `${row.topic ?? ""}: ${row.data ?? ""} ${row.value ?? ""}`.trim(),
      row.use ?? row.used_in ?? "",
      row.confidence,
      row.note ?? row.unit ?? "",
    ]);
  }
  writeBlock(sheet, 3, 1, rows);
  styleTable(sheet, 3, 1, rows.length, 5);
}

function addBom() {
  const sheet = workbook.worksheets.add("Tabela1_BOM");
  addTitle(sheet, "Tabela 1 - Componentes por unidade de produto embalado", 6);
  const rows = [["Componentes", "Quantidades", "Unidade de medida", "Fazer ou comprar", "Justificativa"]];
  for (const row of results.bom) {
    rows.push([row.component, row.quantity, row.unit, row.make_or_buy, row.justification]);
  }
  writeBlock(sheet, 3, 1, rows);
  styleTable(sheet, 3, 1, rows.length, 5);
}

function addProcesses() {
  const sheet = workbook.worksheets.add("Tabela2_Processos");
  addTitle(sheet, "Tabela 2 - Processos industriais e recursos", 7);
  const rows = [["No.", "Processo", "Tipo", "Recursos fisicos", "Equipamento vinculado"]];
  for (const p of results.processes) {
    rows.push([p.number, p.name, p.type, p.resources, p.equipment_id ?? ""]);
  }
  writeBlock(sheet, 3, 1, rows);
  styleTable(sheet, 3, 1, rows.length, 5);
}

function addEquipment() {
  const sheet = workbook.worksheets.add("Tabela3_Equipamentos");
  addTitle(sheet, "Tabela 3 - Equipamentos selecionados", 9);
  const rows = [["Tipo", "Fornecedor", "Modelo", "Medidas aprox. (m)", "Capacidade informada/assumida", "Fonte"]];
  for (const e of results.equipment_capacity) {
    rows.push([
      e.type,
      e.supplier,
      e.model,
      `${e.dimensions_m.length ?? ""} x ${e.dimensions_m.width ?? ""} x ${e.dimensions_m.height ?? ""}`,
      e.official_capacity,
      e.source,
    ]);
  }
  writeBlock(sheet, 3, 1, rows);
  styleTable(sheet, 3, 1, rows.length, 6);
}

function addMaterials() {
  const sheet = workbook.worksheets.add("Materiais");
  addTitle(sheet, "Estimativa de consumo de materiais", 9);
  const rows = [["Item", "Fonte", "Formula usada no codigo", "Entradas", "Massa liquida g/kit", "Fator perda", "Compra g/kit", "Compra kg/semana"]];
  for (const m of results.materials) {
    const inputs = m.inputs;
    rows.push([
      m.item,
      m.source,
      m.formula,
      JSON.stringify(inputs),
      m.net_g_per_kit,
      m.loss_factor,
      null,
      null,
    ]);
  }
  writeBlock(sheet, 3, 1, rows);
  const formulas = results.materials.map((_, i) => {
    const r = i + 4;
    return [`=E${r}*F${r}`, `=G${r}*ROUNDUP(Premissas!B4/Premissas!B5,0)/1000`];
  });
  writeFormulas(sheet, 4, 7, formulas);
  styleTable(sheet, 3, 1, rows.length, 8);
}

function addCapacity() {
  const sheet = workbook.worksheets.add("Capacidade");
  addTitle(sheet, "Capacidade e quantidade por equipamento", 14);
  const rows = [[
    "ID", "Tipo", "Fornecedor", "Modelo", "Taxa nominal kit/h", "Horas uteis/sem", "Eficiencia",
    "Confiabilidade", "Rend. processo", "Taxa efetiva kit/h", "Capacidade sem./maq.",
    "Qtd. necessaria", "Utilizacao", "Area planejada m2", "Base da taxa"
  ]];
  for (const e of results.equipment_capacity) {
    rows.push([
      e.id,
      e.type,
      e.supplier,
      e.model,
      e.nominal_rate_kits_per_hour,
      null,
      null,
      null,
      null,
      null,
      null,
      null,
      null,
      e.planned_area_m2,
      e.rate_basis,
    ]);
  }
  writeBlock(sheet, 3, 1, rows);
  const formulas = results.equipment_capacity.map((_, i) => {
    const r = i + 4;
    return [
      "=Premissas!B6*Premissas!B7*Premissas!B9",
      "=Premissas!B10",
      "=Premissas!B11",
      "=Premissas!B12",
      `=E${r}*G${r}*H${r}*I${r}`,
      `=J${r}*F${r}`,
      `=ROUNDUP(ROUNDUP(Premissas!B4/Premissas!B5,0)/K${r},0)`,
      `=ROUNDUP(Premissas!B4/Premissas!B5,0)/(L${r}*K${r})`,
    ];
  });
  writeFormulas(sheet, 4, 6, formulas);
  styleTable(sheet, 3, 1, rows.length, 15);
}

function addSelected() {
  const sheet = workbook.worksheets.add("Calculo_Router");
  addTitle(sheet, "Memoria de calculo - equipamento selecionado", 5);
  const s = results.selected_equipment_detail;
  const rows = [
    ["Entrada / resultado", "Valor", "Formula / premissa"],
    ["Equipamento", `${s.supplier} ${s.model}`, s.equipment_type],
    ["Operacoes", s.operations.join("; "), "Processos considerados na Tabela 2"],
    ["Meta semanal boa", null, "Premissas!B4"],
    ["Rendimento final", null, "Premissas!B5"],
    ["Demanda bruta", null, "ROUNDUP(B6/B7,0)"],
    ["Horas uteis semanais", null, "Premissas!B6*Premissas!B7*Premissas!B9"],
    ["Tempo padrao", s.standard_time_seconds_per_kit, "s/kit"],
    ["Taxa nominal", null, "3600 / tempo padrao"],
    ["Eficiencia", null, "Premissas!B10"],
    ["Confiabilidade", null, "Premissas!B11"],
    ["Rendimento do processo", null, "Premissas!B12"],
    ["Taxa efetiva", null, "taxa nominal * eficiencia * confiabilidade * rendimento"],
    ["Capacidade semanal por maquina", null, "taxa efetiva * horas uteis"],
    ["Quantidade necessaria", null, "ROUNDUP(demanda bruta / capacidade semanal,0)"],
    ["Utilizacao", null, "demanda bruta / (quantidade * capacidade semanal)"],
  ];
  writeBlock(sheet, 3, 1, rows);
  writeFormulas(sheet, 6, 2, [
    ["=Premissas!B4"],
    ["=Premissas!B5"],
    ["=ROUNDUP(B6/B7,0)"],
    ["=Premissas!B6*Premissas!B7*Premissas!B9"],
  ]);
  writeFormulas(sheet, 11, 2, [["=3600/B10"], ["=Premissas!B10"], ["=Premissas!B11"], ["=Premissas!B12"], ["=B11*B12*B13*B14"], ["=B15*B9"], ["=ROUNDUP(B8/B16,0)"], ["=B8/(B17*B16)"]]);
  styleTable(sheet, 3, 1, rows.length, 3);
}

function addAreas() {
  const sheet = workbook.worksheets.add("Areas_Layout");
  addTitle(sheet, "Calculo de areas para layout esquematico", 6);
  const l = results.layout;
  const fixedStart = 13;
  const rows = [
    ["Area", "m2", "Formula / criterio"],
    ["Area de equipamentos", null, "SUM(Capacidade!N:N)"],
    ["Areas fixas", null, "SUM(B13:B18)"],
    ["Circulacao", null, "30% * (equipamentos + areas fixas)"],
    ["Area total requerida", null, "equipamentos + fixas + circulacao"],
    ["Area total proposta", null, `${l.layout_dimensions_m.length} m * ${l.layout_dimensions_m.width} m`],
    ["Folga de area", null, "area proposta - area requerida"],
    ["Ocupacao", null, "area requerida / area proposta"],
    [],
    ["Areas fixas detalhadas", "m2", "Base"],
  ];
  for (const fixed of l.fixed_areas) {
    rows.push([fixed.area, fixed.m2, fixed.basis]);
  }
  writeBlock(sheet, 3, 1, rows.map(r => r.length ? r : ["", "", ""]));
  writeFormulas(sheet, 4, 2, [["=SUM(Capacidade!N4:N100)"], [`=SUM(B${fixedStart}:B${fixedStart + l.fixed_areas.length - 1})`], ["=(B4+B5)*0.30"], ["=B4+B5+B6"], [`=${l.layout_dimensions_m.length}*${l.layout_dimensions_m.width}`], ["=B8-B7"], ["=B7/B8"]]);
  styleTable(sheet, 3, 1, 8, 3);
  styleTable(sheet, 12, 1, l.fixed_areas.length + 1, 3);
}

function addFormulas() {
  const sheet = workbook.worksheets.add("Formulas");
  addTitle(sheet, "Transparencia das contas e arquivos de origem", 7);
  const rows = [
    ["Tema", "Formula / regra", "Arquivo auditavel"],
    ["Demanda bruta", "ceil(meta_boa / rendimento_final)", "scripts/generate_outputs.py; data/projeto.json"],
    ["Capacidade por equipamento", "taxa_nominal * horas_uteis * eficiencia * confiabilidade * rendimento_processo", "scripts/generate_outputs.py"],
    ["Quantidade de maquinas", "ceil(demanda_bruta / capacidade_semanal_por_maquina)", "scripts/generate_outputs.py; aba Capacidade"],
    ["Consumo de materiais", "massa_liquida * fator_perda * demanda_bruta", "scripts/generate_outputs.py; aba Materiais"],
    ["Area de equipamentos", "comprimento * largura * quantidade * fator_area_servico", "scripts/generate_outputs.py; aba Areas_Layout"],
    ["Ponto fraco controlado", "Dados sem fonte viram premissa declarada; nao entram como fato de fabricante.", "05_base_tecnica/revisao_plano_e_pontos_fracos.md"],
  ];
  writeBlock(sheet, 3, 1, rows);
  styleTable(sheet, 3, 1, rows.length, 3);
}

addPremissas();
addMembers();
addResumo();
addResearch();
addBom();
addProcesses();
addEquipment();
addMaterials();
addCapacity();
addSelected();
addAreas();
addFormulas();

const check = await workbook.inspect({
  kind: "table",
  range: "Resumo!A1:C13",
  include: "values,formulas",
  tableMaxRows: 20,
  tableMaxCols: 8,
});
console.log(check.ndjson);

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 200 },
  summary: "final formula error scan",
});
console.log(errors.ndjson);

await fs.mkdir(path.dirname(outputPath), { recursive: true });
const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(outputPath);
console.log(`Saved ${outputPath}`);
