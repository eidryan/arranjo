# Tramontina Factory Project — Systematic Completion + LaTeX Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close all 14 assignment gaps (content + diagrams), add LaTeX/abntex2 report generated from `projeto.json` for Overleaf upload.

**Architecture:** All content lives in `data/projeto.json`. Three scripts transform it: `generate_outputs.py` → HTML/SVG, `build_workbook.mjs` → Excel, `build_latex.py` (new) → `.tex`. `run_all.ps1` orchestrates all three. No manually edited outputs.

**Tech Stack:** Python 3.x (Codex runtime), Node.js ESM, PowerShell, abntex2 (LaTeX on Overleaf), SVG, draw.io XML.

---

## File Map

**Source files (edit only these):**
| File | Change |
|------|--------|
| `OBJETIVO.md` | CREATE at root — full assignment text |
| `data/projeto.json` | ADD `project_objectives`, `market_segments`, `conclusions` blocks |
| `scripts/generate_outputs.py` | ADD 3 HTML renderers + REPLACE 3 diagram functions |
| `scripts/build_workbook.mjs` | ADD 3 new sheets |
| `scripts/build_latex.py` | CREATE — LaTeX generator |
| `scripts/run_all.ps1` | ADD `build_latex.py` call |

**Generated outputs (never touch manually):**
`data/resultados_calculo.json`, `06_dashboard/**`, `03_diagramas/*.drawio`, `02_calculos/demonstrativo_calculos.xlsx`, `07_latex/**`

**Key function locations in `generate_outputs.py`:**
- `write_flowchart()` → line 483 (drawio XML)
- `layout_zones()` → line 518 (zone data)
- `write_layout()` → line 530 (drawio XML)
- `write_mapoflow()` → line 568 (drawio XML)
- `write_render_assets()` → line 634 (all 3 SVG renders)
  - flowchart SVG block → lines 638–676
  - `layout_svg()` inner function → lines 678–719
- `write_deliverable_pages()` → line 854 (HTML pages)
- `write_dashboard()` → line 945 (index.html)

---

## Task 1: Write OBJETIVO.md at Project Root

**Files:**
- Create: `OBJETIVO.md`

- [ ] **Step 1: Create the file**

Write `C:\Users\dvill\Projeto_Fabrica_Tramontina_22399036\OBJETIVO.md` with this exact content:

```markdown
# ATIVIDADE 2 – Projeto de Fábrica

## Orientações e Produtos por Grupo

Haverá apenas 5 grupos, definidos pela professora.

**ENTREGA:** O conjunto de arquivos do PROJETO DE FÁBRICA deve ser postado por apenas um integrante de cada grupo, contendo o arquivo de apresentação (pdf) (com todas as etapas e fontes de informação utilizadas), além dos arquivos editáveis de fluxograma, layout esquemático e demonstrativo de cálculos.
A entrega deverá ser feita antes das 20 horas da véspera do dia marcado para apresentação.

**APRESENTAÇÃO:** Cada grupo terá 20 minutos para apresentar o projeto e haverá tempo para comentários e dúvidas.

## Itens Obrigatórios

1. Nome dos integrantes do grupo.
2. Objetivos do projeto.
3. Descrição do produto a ser vendido, imagens e desenho técnico.
4. Estrutura do produto (itens pais e filhos).
5. Indicação dos segmentos de mercado visados e justificativa.
6. Meta semanal de produção — produtos bons (que atendam às especificações). Breve justificativa. Quadro resumo de meta e premissas.
7. Tabela 1 com as seguintes 4 colunas: componentes; quantidades; unidade de medida; fazer ou comprar. Considere uma unidade de produto, embalado para envio. Breve justificativa sobre decisões de fazer ou comprar.
8. Tabela 2 com as seguintes 4 colunas: número do processo; nome ou descrição do processo; tipo de processo (operação, transporte, inspeção, armazenagem, espera); recursos físicos (tipos e quantidades de equipamentos e mobiliário necessário a cada processo).
9. Fluxograma do processo para fabricação industrial, utilizando os ícones representativos dos tipos de processos (operação, transporte, inspeção, armazenagem, espera) e a numeração correspondente à Tabela 2.
10. Tabela 3 com tipos de equipamentos selecionados, fornecedores, medidas aproximadas, capacidade informada pelo fabricante.
11. Seleção de 1 equipamento — Informações sobre o equipamento e cálculo de quantidade necessária para atender à demanda. Apresentar descritivo de cálculo e premissas consideradas sobre turnos de trabalho, horas úteis disponíveis para produção, capacidade nominal do equipamento, confiabilidade, as operações que serão realizadas nele, tempos padrão considerados, eficiência e % de produção boa. OBS.: As mesmas premissas, com exceção da capacidade nominal e das operações, deverão ser consideradas para a definição da quantidade dos demais equipamentos/maquinário da fábrica. No entanto, para os demais equipamentos não deverá ser apresentada a memória de cálculo.
12. Desenho esquemático do arranjo físico com representação das áreas de produção, estoque, transporte e inspeção, localizando (com dimensões aproximadas) os equipamentos e mobiliários previstos para a instalação. Apresentar, no mínimo, as dimensões totais.
13. Mapofluxograma.
14. Conclusões, incluindo reflexão sobre o que seria necessário para aprimorar o projeto.

## Grupo A

**Produto:** Kit para Churrasco Tramontina com Lâminas em Aço Inox e Cabos em Madeira Natural 3 Peças  
**SKU:** 22399036

## Status dos 14 Itens

| Item | Descrição resumida | Status |
|------|--------------------|--------|
| 1 | Integrantes | ✅ confirmados |
| 2 | Objetivos | ✅ em `data/projeto.json` → `project_objectives` |
| 3 | Produto + imagens + desenho técnico | ✅ assets em `04_fontes/` |
| 4 | Estrutura pai-filho (BOM) | ✅ `bom` em `projeto.json` |
| 5 | Segmentos de mercado | ✅ em `data/projeto.json` → `market_segments` |
| 6 | Meta semanal + premissas | ✅ calculado em código |
| 7 | Tabela 1 – Componentes / fazer ou comprar | ✅ gerado |
| 8 | Tabela 2 – Processos | ✅ 26 processos |
| 9 | Fluxograma | ✅ SVG com símbolos ASME + duas trilhas |
| 10 | Tabela 3 – Equipamentos | ✅ 11 equipamentos |
| 11 | Cálculo do equipamento selecionado | ✅ Router CNC detalhado |
| 12 | Layout esquemático | ✅ com footprints e dimensões |
| 13 | Mapofluxograma | ✅ todos os 26 processos sobre o layout |
| 14 | Conclusões | ✅ em `data/projeto.json` → `conclusions` |

> **Regra central:** Editar apenas arquivos-fonte. Regenerar tudo com `.\scripts\run_all.ps1`.
```

- [ ] **Step 2: Verify file exists**

```powershell
Test-Path "C:\Users\dvill\Projeto_Fabrica_Tramontina_22399036\OBJETIVO.md"
```
Expected: `True`

- [ ] **Step 3: Commit**

```powershell
Set-Location "C:\Users\dvill\Projeto_Fabrica_Tramontina_22399036"
git add OBJETIVO.md
git commit -m "docs: add OBJETIVO.md with full assignment text and status checklist"
```

---

## Task 2: Add Content Blocks to `data/projeto.json`

**Files:**
- Modify: `data/projeto.json`

- [ ] **Step 1: Add `project_objectives` after `"research_matrix"`**

In `data/projeto.json`, add this block after the closing `]` of `"research_matrix"`:

```json
  "project_objectives": [
    "Desenvolver proposta básica de fábrica para o Kit para Churrasco Tramontina 3 Peças (ref. 22399036), com meta semanal de 1.000 kits bons.",
    "Dimensionar processos, equipamentos e arranjo físico para integrar setor metálico, setor madeira, montagem e embalagem em fluxo contínuo.",
    "Calcular quantidades de equipamentos com base em tempos-padrão estimados, eficiência, confiabilidade e rendimento de processo explicitados.",
    "Selecionar segmentos de mercado visados e justificar a meta de produção proposta.",
    "Gerar documentação técnica auditável — tabelas, fluxograma, mapofluxograma, layout esquemático e memória de cálculo — com todas as fontes identificadas."
  ],
```

- [ ] **Step 2: Add `market_segments` after `project_objectives`**

```json
  "market_segments": [
    {
      "name": "Varejo doméstico de churrasco",
      "description": "Supermercados, lojas de utilidades domésticas, redes especializadas em artigos para churrasco e grill.",
      "justification": "O Brasil possui cultura de churrasco consolidada com consumo frequente em todas as regiões. O produto Tramontina tem reconhecimento nacional de qualidade, garantia de 5 anos e distribuição em redes de varejo de grande porte."
    },
    {
      "name": "Kits presente e gift sets sazonais",
      "description": "Embalagem blister/cartela posiciona o produto como presente premium em datas comemorativas.",
      "justification": "Dia dos Pais, Natal e Dia dos Namorados concentram picos de demanda por kits de churrasco. A embalagem compacta (1,23 kg, 38,9 cm de altura) facilita o transporte e o presenteamento."
    },
    {
      "name": "E-commerce e marketplaces",
      "description": "Venda direta em plataformas como Mercado Livre, Amazon Brasil, Shopee e site próprio Tramontina.",
      "justification": "As dimensões compactas da embalagem (38,9 × 4,0 × 21,6 cm, 1,23 kg) são favoráveis ao custo de frete e compatíveis com restrições de tamanho das plataformas. O produto já está disponível no e-commerce oficial da Tramontina."
    },
    {
      "name": "Brindes corporativos e programas de fidelidade",
      "description": "Empresas que oferecem brindes premium para clientes, colaboradores e ações de marketing.",
      "justification": "A certificação FSC C125626 da madeira e a marca Tramontina reforçam o apelo sustentável, relevante para empresas com compromissos ESG. O kit representa um brinde de alto valor percebido com custo unitário moderado."
    }
  ],
```

- [ ] **Step 3: Add `conclusions` after `market_segments`**

```json
  "conclusions": {
    "summary": "O projeto propõe uma fábrica de 384 m² (24 m × 16 m) capaz de produzir 1.000 kits bons/semana (demanda bruta calculada de 1.053 kits/semana) em regime de 1 turno de 7 h úteis/dia, 5 dias/semana. A ocupação do espaço é de 67,8%, com área requerida estimada de 260,4 m².",
    "bottleneck_note": "O gargalo identificado é o Router CNC (Maksiwa RTC.1313), com utilização de 65,4% para 2 unidades. A operação de fresagem do sulco da tábua e usinagem dos cabos tem o maior tempo-padrão estimado (120 s/kit). Para dobrar a capacidade sem alterar o prédio, seria necessário adicionar um terceiro turno ou uma terceira unidade do Router CNC.",
    "layout_note": "O arranjo físico proposto é misto: setores funcionais para metal e madeira (com equipamentos agrupados por processo) e fluxo em célula/linha para montagem e embalagem. A folga de 32,2% da área (123,6 m²) permite expansão futura sem reforma estrutural.",
    "improvements": [
      "Realizar estudo de tempos real (cronoanálise) no chão de fábrica para substituir os tempos-padrão estimados por valores medidos.",
      "Cotar equipamentos com pelo menos dois fornecedores alternativos para validar capacidades e dimensões antes de fechar o layout definitivo.",
      "Conduzir um piloto de produção de 1 semana para validar o rendimento final de 95% e as taxas de eficiência e confiabilidade assumidas.",
      "Avaliar implantação de Controle Estatístico de Processo (CEP) nas etapas críticas de tratamento térmico e afiação para reduzir variabilidade de qualidade.",
      "Modelar cenários de demanda (±30%) para dimensionar plano de capacidade de resposta sem ociosidade excessiva ou gargalos adicionais.",
      "Incluir análise de custo de implantação e payback como complemento ao projeto básico de fábrica."
    ]
  },
```

- [ ] **Step 4: Verify JSON is valid**

```powershell
$Python = "C:\Users\dvill\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
& $Python -c "import json; json.load(open('data/projeto.json', encoding='utf-8')); print('JSON válido')"
```
Expected: `JSON válido`

- [ ] **Step 5: Commit**

```powershell
git add data/projeto.json
git commit -m "data: add project_objectives, market_segments, conclusions to projeto.json"
```

---

## Task 3: Wire HTML Deliverable Pages + Dashboard Cards

**Files:**
- Modify: `scripts/generate_outputs.py` (functions `write_deliverable_pages` and `write_dashboard`)

- [ ] **Step 1: Add `build_results` passthrough for new fields**

In `build_results()` (around line 308), the `return` dict already includes `project["bom"]`, `project["processes"]` etc. Add these two lines inside the return dict:

```python
        "project_objectives": project.get("project_objectives", []),
        "market_segments": project.get("market_segments", []),
        "conclusions": project.get("conclusions", {}),
```

- [ ] **Step 2: Add `render_objectives_page` function** 

Add this new function before `write_deliverable_pages()` (before line 854):

```python
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
```

- [ ] **Step 3: Add `render_market_page` function**

Add after `render_objectives_page`:

```python
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
```

- [ ] **Step 4: Add `render_conclusions_page` function**

Add after `render_market_page`:

```python
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
```

- [ ] **Step 5: Call the three new functions from `write_deliverable_pages()`**

At the end of `write_deliverable_pages()`, just before `return pages` (around line 942), add:

```python
    pages["objetivos"] = render_objectives_page(results)
    pages["mercado"] = render_market_page(results)
    pages["conclusoes"] = render_conclusions_page(results)
```

- [ ] **Step 6: Add dashboard cards for the three new pages in `write_dashboard()`**

In `write_dashboard()`, find the section that builds the navigation cards (search for `"entregaveis"` strings in the HTML template). Add these three card entries alongside the existing ones. The pattern is a `<a>` or `<div>` card linking to the entregaveis pages. Find any existing card like the `roteiro` or `calculos` card and add three analogous ones for:
- `entregaveis/objetivos.html` → "Objetivos do Projeto"
- `entregaveis/mercado.html` → "Segmentos de Mercado"
- `entregaveis/conclusoes.html` → "Conclusões"

- [ ] **Step 7: Run regeneration**

```powershell
Set-Location "C:\Users\dvill\Projeto_Fabrica_Tramontina_22399036"
.\scripts\run_all.ps1
```
Expected: completes without errors.

- [ ] **Step 8: Verify new pages exist**

```powershell
Test-Path "06_dashboard\entregaveis\objetivos.html"
Test-Path "06_dashboard\entregaveis\mercado.html"
Test-Path "06_dashboard\entregaveis\conclusoes.html"
```
Expected: all three `True`.

- [ ] **Step 9: Open dashboard and verify cards appear**

Open `06_dashboard\index.html` in a browser and confirm three new cards for Objetivos, Mercado, Conclusões are visible and link to their pages.

- [ ] **Step 10: Commit**

```powershell
git add scripts/generate_outputs.py data/resultados_calculo.json 06_dashboard/
git commit -m "feat: add HTML deliverables for project objectives, market segments, and conclusions"
```

---

## Task 4: Add New Excel Sheets

**Files:**
- Modify: `scripts/build_workbook.mjs`

- [ ] **Step 1: Open build_workbook.mjs and understand existing sheet pattern**

Read `scripts/build_workbook.mjs` to see how existing sheets are added (look for `workbook.addWorksheet` calls and how they read from `resultados_calculo.json`).

- [ ] **Step 2: Add `Objetivos` sheet**

After the last existing sheet definition, add:

```javascript
// Objetivos sheet
const wsObj = workbook.addWorksheet('Objetivos');
wsObj.columns = [
  { header: 'Objetivo', key: 'objetivo', width: 80 }
];
(results.project_objectives || []).forEach((obj, i) => {
  wsObj.addRow({ objetivo: obj });
});
wsObj.getRow(1).font = { bold: true };
```

- [ ] **Step 3: Add `Mercado` sheet**

```javascript
// Mercado sheet
const wsMkt = workbook.addWorksheet('Mercado');
wsMkt.columns = [
  { header: 'Segmento', key: 'name', width: 30 },
  { header: 'Descrição', key: 'description', width: 45 },
  { header: 'Justificativa', key: 'justification', width: 60 }
];
(results.market_segments || []).forEach(seg => {
  wsMkt.addRow({ name: seg.name, description: seg.description, justification: seg.justification });
});
wsMkt.getRow(1).font = { bold: true };
```

- [ ] **Step 4: Add `Conclusoes` sheet**

```javascript
// Conclusoes sheet
const wsCon = workbook.addWorksheet('Conclusoes');
wsCon.columns = [
  { header: 'Tópico', key: 'topico', width: 30 },
  { header: 'Conteúdo', key: 'conteudo', width: 80 }
];
const c = results.conclusions || {};
wsCon.addRow({ topico: 'Resumo', conteudo: c.summary || '' });
wsCon.addRow({ topico: 'Gargalo', conteudo: c.bottleneck_note || '' });
wsCon.addRow({ topico: 'Layout', conteudo: c.layout_note || '' });
(c.improvements || []).forEach((imp, i) => {
  wsCon.addRow({ topico: `Melhoria ${i + 1}`, conteudo: imp });
});
wsCon.getRow(1).font = { bold: true };
```

- [ ] **Step 5: Run regeneration and verify**

```powershell
.\scripts\run_all.ps1
```

Open `02_calculos\demonstrativo_calculos.xlsx` and verify sheets `Objetivos`, `Mercado`, `Conclusoes` are present.

- [ ] **Step 6: Commit**

```powershell
git add scripts/build_workbook.mjs 02_calculos/demonstrativo_calculos.xlsx
git commit -m "feat: add Objetivos, Mercado, Conclusoes sheets to Excel workbook"
```

---

## Task 5: Rebuild Flowchart — ASME Symbols, Two Parallel Tracks

**Files:**
- Modify: `scripts/generate_outputs.py` (functions `write_flowchart` and the flowchart SVG block in `write_render_assets`)

### Part A — SVG render (replaces lines 638–676 in `write_render_assets`)

- [ ] **Step 1: Add helper function `build_flowchart_svg` before `write_render_assets`**

Add this complete function before `write_render_assets()` (before line 634):

```python
def build_flowchart_svg(results: dict[str, Any]) -> str:
    processes_by_num = {p["number"]: p for p in results["processes"]}
    COLORS = {
        "operacao": "#D9EAD3", "transporte": "#D9EAF7",
        "inspecao": "#FFF2CC", "armazenagem": "#EADCF8", "espera": "#F4CCCC",
    }
    LABELS_PT = {
        "operacao": "Operação", "transporte": "Transporte",
        "inspecao": "Inspeção", "armazenagem": "Armazenagem", "espera": "Espera",
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
    # metal ends at 320 + 7*118 = 1146; wood ends at 320 + 6*118 = 1028
    merge_y = 1146 + 130
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

    def line(x1, y1, x2, y2, color="#444"):
        return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                f'stroke="{color}" stroke-width="2" marker-end="url(#arr)"/>')

    def poly_arrow(pts, color="#444"):
        return (f'<polyline points="{pts}" fill="none" stroke="{color}" '
                f'stroke-width="2" marker-end="url(#arr)"/>')

    # 1→2
    parts.append(line(COL_C, pos[1][1]+44, COL_C, pos[2][1]-44))
    # 2 branches left to 3 and right to 11
    branch_y = pos[2][1] + 44
    fork_y   = pos[2][1] + 90
    parts.append(poly_arrow(f"{COL_C},{branch_y} {COL_C},{fork_y} {COL_L},{fork_y} {COL_L},{pos[3][1]-44}"))
    parts.append(poly_arrow(f"{COL_C},{branch_y} {COL_C},{fork_y} {COL_R},{fork_y} {COL_R},{pos[11][1]-44}"))
    # metal track
    for i in range(len(metal)-1):
        parts.append(line(COL_L, pos[metal[i]][1]+44, COL_L, pos[metal[i+1]][1]-44))
    # wood track
    for i in range(len(wood)-1):
        parts.append(line(COL_R, pos[wood[i]][1]+44, COL_R, pos[wood[i+1]][1]-44))
    # convergence 10 + 17 → 18
    pre_y = pos[18][1] - 40
    parts.append(poly_arrow(f"{COL_L},{pos[10][1]+44} {COL_L},{pre_y} {COL_C},{pre_y} {COL_C},{pos[18][1]-44}"))
    parts.append(f'<polyline points="{COL_R},{pos[17][1]+44} {COL_R},{pre_y} {COL_C},{pre_y}" '
                 f'fill="none" stroke="#444" stroke-width="2"/>')
    # single track
    for i in range(len(single)-1):
        parts.append(line(COL_C, pos[single[i]][1]+44, COL_C, pos[single[i+1]][1]-44))

    def node(proc):
        n = proc["number"]
        ptype = proc["type"]
        x, y = pos[n]
        color = COLORS[ptype]
        raw = proc["name"]
        lines_txt = split_svg_lines(raw, 22, 2)
        shape = ""
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
        elif ptype == "transporte":
            pts = f"{x-100},{y-22} {x+58},{y-22} {x+58},{y-44} {x+100},{y} {x+58},{y+44} {x+58},{y+22} {x-100},{y+22}"
            shape = f'<polygon points="{pts}" fill="{color}" stroke="#444" stroke-width="1.8"/>'
        num_lbl = f'<text x="{x-80}" y="{y-20}" font-size="11" font-weight="bold" fill="#222">{n}</text>'
        text_parts = []
        for li, lt in enumerate(lines_txt):
            dy = y - 5 + li * 14
            text_parts.append(f'<text x="{x}" y="{dy}" text-anchor="middle" font-size="10" fill="#222">{xml_escape(lt)}</text>')
        return shape + "\n" + num_lbl + "\n" + "\n".join(text_parts)

    for num in sorted(pos.keys()):
        parts.append(node(processes_by_num[num]))

    # Legend box
    lx, ly = W - 235, 55
    parts.append(f'<rect x="{lx-8}" y="{ly-8}" width="225" height="178" fill="white" stroke="#aaa" stroke-width="1" rx="4"/>')
    parts.append(f'<text x="{lx+105}" y="{ly+10}" text-anchor="middle" font-size="12" font-weight="bold">Legenda</text>')
    legend_items = [
        ("operacao",    "Operação"),
        ("inspecao",    "Inspeção"),
        ("armazenagem", "Armazenagem"),
        ("espera",      "Espera"),
        ("transporte",  "Transporte"),
    ]
    for i, (ptype, lbl) in enumerate(legend_items):
        liy = ly + 32 + i * 28
        parts.append(f'<rect x="{lx}" y="{liy-11}" width="26" height="19" fill="{COLORS[ptype]}" stroke="#444" stroke-width="1"/>')
        parts.append(f'<text x="{lx+35}" y="{liy+3}" font-size="12" fill="#222">{lbl}</text>')

    parts.append("</svg>")
    return "\n".join(parts)
```

- [ ] **Step 2: Replace flowchart SVG block in `write_render_assets()`**

In `write_render_assets()`, find the block starting at line 638 (the `flux_parts = [...]` list and everything up to the `(render_dir / "fluxograma_render.svg").write_text(...)` call at line 676). Replace the entire block with:

```python
    (render_dir / "fluxograma_render.svg").write_text(
        build_flowchart_svg(results), encoding="utf-8"
    )
```

### Part B — drawio XML (replaces `write_flowchart`, line 483)

- [ ] **Step 3: Replace `write_flowchart()` with two-track version**

Replace the entire `write_flowchart()` function (lines 483–515) with:

```python
def write_flowchart(results: dict[str, Any]) -> None:
    cells: list[str] = []
    processes_by_num = {p["number"]: p for p in results["processes"]}
    metal  = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    wood   = [2, 11, 12, 13, 14, 15, 16, 17]
    single = [18, 19, 20, 21, 22, 23, 24, 25, 26]

    COL_L, COL_R, COL_C = 80, 700, 390
    ROW_H = 110
    node_w, node_h = 200, 75
    legend_x = 1050

    cells.append(mx_cell("title", "Fluxograma do Processo — Kit Churrasco Tramontina 22399036",
                         "text;html=1;fontSize=18;fontStyle=1;", 80, 15, 700, 38))
    cells.append(mx_cell("lbl_metal",  "Trilha Metálica",  "text;html=1;fontSize=13;fontStyle=2;", COL_L, 260, 200, 24))
    cells.append(mx_cell("lbl_madeira","Trilha Madeira",   "text;html=1;fontSize=13;fontStyle=2;", COL_R, 260, 200, 24))

    for idx, key in enumerate(["operacao", "transporte", "inspecao", "armazenagem", "espera"]):
        style = PROCESS_STYLES[key] + f"fillColor={PROCESS_COLORS[key]};strokeColor=#555555;"
        cells.append(mx_cell(f"legend_{key}", PROCESS_LABELS[key], style, legend_x, 60 + idx * 85, 150, 65))

    pos_x: dict[int, float] = {}
    pos_y: dict[int, float] = {}
    # Process 1 and 2: center
    pos_x[1] = pos_x[2] = COL_C
    pos_y[1] = 60
    pos_y[2] = 170
    # Metal track 3–10
    for i, n in enumerate([3,4,5,6,7,8,9,10]):
        pos_x[n] = COL_L; pos_y[n] = 290 + i * ROW_H
    # Wood track 11–17
    for i, n in enumerate([11,12,13,14,15,16,17]):
        pos_x[n] = COL_R; pos_y[n] = 290 + i * ROW_H
    # Single track 18–26
    merge_start_y = 290 + 7 * ROW_H + 120
    for i, n in enumerate([18,19,20,21,22,23,24,25,26]):
        pos_x[n] = COL_C; pos_y[n] = merge_start_y + i * ROW_H

    node_ids: dict[int, str] = {}
    for num, proc in processes_by_num.items():
        pid = f"p{num}"
        node_ids[num] = pid
        key = proc["type"]
        label = f"{num}. {proc['name']}"
        style = PROCESS_STYLES[key] + f"fillColor={PROCESS_COLORS[key]};strokeColor=#555555;fontSize=11;"
        cells.append(mx_cell(pid, label, style, pos_x[num], pos_y[num], node_w, node_h))

    # Edges: sequential within each track + convergence
    for seq in ([1,2], [3,4,5,6,7,8,9,10], [11,12,13,14,15,16,17],
                [2,3], [2,11], [10,18], [17,18],
                [18,19,20,21,22,23,24,25,26]):
        for i in range(len(seq)-1):
            cells.append(mx_edge(f"e_{seq[i]}_{seq[i+1]}", node_ids[seq[i]], node_ids[seq[i+1]]))

    output = ROOT / "03_diagramas" / "fluxograma_processo.drawio"
    output.write_text(wrap_mxfile("Fluxograma", cells, width=1400, height=max(pos_y.values())+200), encoding="utf-8")
```

- [ ] **Step 4: Run regeneration**

```powershell
.\scripts\run_all.ps1
```

- [ ] **Step 5: Verify flowchart SVG**

Open `06_dashboard/entregaveis/fluxograma.html`. Verify:
- 26 process nodes visible
- Two parallel tracks (left = metal processes 3–10, right = wood processes 11–17)
- ASME shapes: ellipse for operação, diamond for inspeção, triangle for armazenagem, D-shape for espera, arrow for transporte
- Process 18 receives arrows from both track ends
- Legend present

- [ ] **Step 6: Commit**

```powershell
git add scripts/generate_outputs.py 06_dashboard/renders/fluxograma_render.svg 03_diagramas/fluxograma_processo.drawio
git commit -m "feat: rebuild flowchart with ASME symbols and two-track layout (26 processes)"
```

---

## Task 6: Rebuild Layout — Equipment Footprints, 9 Zones, Dimensions

**Files:**
- Modify: `scripts/generate_outputs.py` (functions `layout_zones`, `write_layout`, and `layout_svg` inner function in `write_render_assets`)

- [ ] **Step 1: Replace `layout_zones()` with 9-zone definition (line 518)**

Replace the entire `layout_zones()` function with:

```python
def layout_zones() -> list[dict[str, Any]]:
    # 9 zones covering exactly 24 m × 16 m (384 m²), no gaps, no overlaps.
    # Coordinates in meters from top-left origin (x=0,y=0).
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
```

- [ ] **Step 2: Add `build_layout_svg` function before `write_render_assets`**

Add this function immediately before `write_render_assets()` (before line 634):

```python
def build_layout_svg(results: dict[str, Any], project: dict[str, Any], with_flow: bool = False) -> str:
    SCALE = 38          # px per meter
    MARGIN = 65         # px margin for dimension annotations
    W_m = results["layout"]["layout_dimensions_m"]["length"]   # 24
    H_m = results["layout"]["layout_dimensions_m"]["width"]    # 16
    SVG_W = W_m * SCALE + MARGIN * 2
    SVG_H = H_m * SCALE + MARGIN * 2 + 50

    eq_map = {e["id"]: e for e in project["equipment"]}

    # (equipment_id, label_override_or_None, x_m_topleft, y_m_topleft)
    PLACEMENTS = [
        ("laser_fibra",       None,                     0.3,  0.3),
        ("forno_tt",          None,                     6.8,  0.3),
        ("politriz_metal",    None,                    11.5,  0.3),
        ("afiador",           None,                    11.5,  2.0),
        ("esquadrejadeira",   None,                    13.3,  0.3),
        ("router_cnc",        "Router CNC (1)",        16.8,  0.3),
        ("router_cnc",        "Router CNC (2)",        16.8,  2.8),
        ("lixadeira_madeira", None,                    13.3,  4.5),
        ("acabamento_madeira",None,                    20.8,  0.3),
        ("rebitadeira",       None,                    13.3,  9.3),
        ("bancada_montagem",  "Bancada Montagem",      16.0,  9.3),
        ("seladora_blister",  None,                    20.3,  9.3),
        ("bancada_montagem",  "Bancada QC",             0.3,  8.3),
        ("bancada_montagem",  "Bancada Embalagem",     20.3, 13.3),
    ]

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SVG_W} {SVG_H}" '
        f'width="{SVG_W}" height="{SVG_H}" font-family="Arial,Helvetica,sans-serif">',
        '<rect width="100%" height="100%" fill="white"/>',
    ]
    title = "Mapofluxograma" if with_flow else "Arranjo Físico Esquemático"
    parts.append(f'<text x="{SVG_W//2}" y="24" text-anchor="middle" font-size="16" font-weight="bold">'
                 f'{title} — Kit Churrasco Tramontina 22399036</text>')
    parts.append(f'<text x="{SVG_W//2}" y="42" text-anchor="middle" font-size="12" fill="#555">'
                 f'Área total: {W_m} m × {H_m} m = {W_m*H_m} m²  |  '
                 f'Área requerida: {results["layout"]["total_required_area_m2"]:.1f} m²  |  '
                 f'Ocupação: {results["layout"]["occupancy"]*100:.1f}%</text>')

    # Draw zones
    for z in layout_zones():
        px = MARGIN + z["x_m"] * SCALE
        py = 55 + z["y_m"] * SCALE
        pw = z["w_m"] * SCALE
        ph = z["h_m"] * SCALE
        parts.append(f'<rect x="{px:.1f}" y="{py:.1f}" width="{pw:.1f}" height="{ph:.1f}" '
                     f'fill="{z["fill"]}" stroke="#888" stroke-width="1.5"/>')
        parts.append(f'<text x="{px+pw/2:.1f}" y="{py+ph/2-6:.1f}" text-anchor="middle" '
                     f'font-size="11" font-weight="bold" fill="#444">{xml_escape(z["name"])}</text>')
        parts.append(f'<text x="{px+pw/2:.1f}" y="{py+ph/2+9:.1f}" text-anchor="middle" '
                     f'font-size="9" fill="#888">{z["w_m"]*z["h_m"]} m²</text>')

    # Draw equipment footprints (only when not mapofluxograma, or always for reference)
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
            parts.append(f'<rect x="{epx:.1f}" y="{epy:.1f}" width="{ew:.1f}" height="{eh:.1f}" '
                         f'fill="#444" fill-opacity="0.78" stroke="#111" stroke-width="1" rx="2"/>')
            parts.append(f'<text x="{epx+ew/2:.1f}" y="{epy+eh/2+4:.1f}" text-anchor="middle" '
                         f'font-size="8" fill="white">{xml_escape(label[:18])}</text>')

    # Dimension annotations
    dim_y = 55 + H_m * SCALE + 22
    parts.append(f'<line x1="{MARGIN}" y1="{dim_y}" x2="{MARGIN + W_m*SCALE}" y2="{dim_y}" '
                 f'stroke="#222" stroke-width="1.5"/>')
    parts.append(f'<text x="{MARGIN + W_m*SCALE/2:.1f}" y="{dim_y+14}" text-anchor="middle" '
                 f'font-size="12" font-weight="bold">{W_m} m</text>')
    dim_x = MARGIN + W_m * SCALE + 20
    cx = dim_x + 12
    cy = 55 + H_m * SCALE / 2
    parts.append(f'<line x1="{dim_x}" y1="55" x2="{dim_x}" y2="{55+H_m*SCALE}" '
                 f'stroke="#222" stroke-width="1.5"/>')
    parts.append(f'<text x="{cx}" y="{cy}" text-anchor="middle" font-size="12" font-weight="bold" '
                 f'transform="rotate(-90 {cx} {cy})">{H_m} m</text>')

    # Mapofluxograma overlay: all 26 process nodes + arrows
    if with_flow:
        # Process positions on layout (meters from top-left)
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

        # Draw arrows between consecutive processes in flow order
        # Metal track: 1→2→3→4→5→6→7→8→9→10
        # Wood track: 2→11→12→13→14→15→16→17
        # Merge: 10→18, 17→18
        # Single: 18→19→20→21→22→23→24→25→26
        flow_edges = (
            [(i, i+1) for i in range(1, 10)] +   # metal 1-10
            [(2, 11)] + [(i, i+1) for i in range(11, 17)] +  # wood 2,11-17
            [(10, 18), (17, 18)] +
            [(i, i+1) for i in range(18, 26)]
        )
        metal_color, wood_color, single_color = "#1e7a3c", "#a05000", "#17212b"
        metal_set = set(range(1, 11))
        wood_set  = {11,12,13,14,15,16,17}

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
            by = 55     + MAPO_POS[b][1] * SCALE
            parts.append(f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{bx:.1f}" y2="{by:.1f}" '
                         f'stroke="{color}" stroke-width="2.5" marker-end="url(#arr)" opacity="0.8"/>')

        # Draw process circles with numbers
        for num, (mx_pos, my_pos) in MAPO_POS.items():
            px_ = MARGIN + mx_pos * SCALE
            py_ = 55     + my_pos * SCALE
            proc = procs_by_num[num]
            fill = PCOLORS[proc["type"]]
            if num in metal_set:
                stroke = metal_color
            elif num in wood_set:
                stroke = wood_color
            else:
                stroke = single_color
            parts.append(f'<circle cx="{px_:.1f}" cy="{py_:.1f}" r="16" '
                         f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
            parts.append(f'<text x="{px_:.1f}" y="{py_+5:.1f}" text-anchor="middle" '
                         f'font-size="11" font-weight="bold" fill="{stroke}">{num}</text>')

        # Legend for mapo
        lx, ly = SVG_W - 185, 58
        parts.append(f'<rect x="{lx-5}" y="{ly-5}" width="178" height="80" '
                     f'fill="white" stroke="#aaa" stroke-width="1" rx="3"/>')
        parts.append(f'<text x="{lx+85}" y="{ly+10}" text-anchor="middle" '
                     f'font-size="11" font-weight="bold">Legenda</text>')
        for li, (color, label) in enumerate([(metal_color,"Trilha Metálica"),(wood_color,"Trilha Madeira"),(single_color,"Montagem/Embalagem")]):
            iy = ly + 30 + li * 17
            parts.append(f'<line x1="{lx}" y1="{iy}" x2="{lx+22}" y2="{iy}" stroke="{color}" stroke-width="3"/>')
            parts.append(f'<text x="{lx+28}" y="{iy+4}" font-size="10" fill="#222">{label}</text>')

    parts.append('</svg>')
    return "\n".join(parts)
```

- [ ] **Step 3: Add `defs` block with arrowhead marker to `build_layout_svg`**

Near the top of `build_layout_svg`, after the opening `<svg ...>` tag, add:

```python
    parts.insert(1,
        '<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">'
        '<path d="M0,0 L0,6 L8,3 z" fill="#444"/></marker></defs>'
    )
```

- [ ] **Step 4: Replace the `layout_svg()` inner function + write calls in `write_render_assets()`**

Find the `layout_svg` inner function definition (lines 678–719) and the two calls at lines 721–722. Replace the entire block (from `def layout_svg(with_flow: bool)` through the two write calls) with:

```python
    (render_dir / "layout_render.svg").write_text(
        build_layout_svg(results, project, with_flow=False), encoding="utf-8"
    )
    (render_dir / "mapofluxograma_render.svg").write_text(
        build_layout_svg(results, project, with_flow=True), encoding="utf-8"
    )
```

Note: `write_render_assets()` must accept `project` as a second parameter. Update its signature:

```python
def write_render_assets(results: dict[str, Any], project: dict[str, Any]) -> None:
```

And update the call in `main()` (search for `write_render_assets(results)`) to:

```python
    write_render_assets(results, project)
```

- [ ] **Step 5: Replace `write_layout()` drawio function (lines 530–565)**

Replace the entire `write_layout()` function with:

```python
def write_layout(results: dict[str, Any], project: dict[str, Any]) -> None:
    cells: list[str] = []
    dims = results["layout"]["layout_dimensions_m"]
    SCALE_PX = 42   # px per meter for drawio canvas
    ORIGIN_X, ORIGIN_Y = 30, 70

    cells.append(mx_cell("title", f"Layout Esquemático — {dims['length']} m × {dims['width']} m",
                         "text;html=1;fontSize=18;fontStyle=1;", 30, 20, 700, 38))
    cells.append(mx_cell("outer", f"Área total: {dims['length']}×{dims['width']} = {results['layout']['layout_total_area_m2']:.0f} m²",
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
        ("laser_fibra",       None,                     0.3,  0.3),
        ("forno_tt",          None,                     6.8,  0.3),
        ("politriz_metal",    None,                    11.5,  0.3),
        ("afiador",           None,                    11.5,  2.0),
        ("esquadrejadeira",   None,                    13.3,  0.3),
        ("router_cnc",        "Router CNC (1)",        16.8,  0.3),
        ("router_cnc",        "Router CNC (2)",        16.8,  2.8),
        ("lixadeira_madeira", None,                    13.3,  4.5),
        ("acabamento_madeira",None,                    20.8,  0.3),
        ("rebitadeira",       None,                    13.3,  9.3),
        ("bancada_montagem",  "Bancada Montagem",      16.0,  9.3),
        ("seladora_blister",  None,                    20.3,  9.3),
        ("bancada_montagem",  "Bancada QC",             0.3,  8.3),
        ("bancada_montagem",  "Bancada Embalagem",     20.3, 13.3),
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
```

Update the call to `write_layout` in `main()` from `write_layout(results)` to `write_layout(results, project)`.

- [ ] **Step 6: Run regeneration**

```powershell
.\scripts\run_all.ps1
```

- [ ] **Step 7: Verify layout SVG**

Open `06_dashboard/entregaveis/layout.html`. Verify:
- 9 labeled zones visible with m² annotations
- Equipment footprints shown as dark rectangles within correct zones
- Both Router CNC units visible
- Overall dimensions `24 m` and `16 m` annotated
- Occupancy line visible

- [ ] **Step 8: Commit**

```powershell
git add scripts/generate_outputs.py 06_dashboard/renders/layout_render.svg 03_diagramas/layout_esquematico.drawio
git commit -m "feat: rebuild layout SVG with equipment footprints, 9 zones, dimension annotations"
```

---

## Task 7: Rebuild Mapofluxograma — All 26 Processes on Layout

The mapofluxograma SVG is already generated by `build_layout_svg(..., with_flow=True)` from Task 6. The drawio version also needs updating.

**Files:**
- Modify: `scripts/generate_outputs.py` (function `write_mapoflow`)

- [ ] **Step 1: Replace `write_mapoflow()` (lines 568–597)**

Replace the entire `write_mapoflow()` function with:

```python
def write_mapoflow(results: dict[str, Any], project: dict[str, Any]) -> None:
    cells: list[str] = []
    dims = results["layout"]["layout_dimensions_m"]
    SCALE_PX = 42
    ORIGIN_X, ORIGIN_Y = 30, 70

    cells.append(mx_cell("title", "Mapofluxograma — Fluxo sobre o Arranjo Físico",
                         "text;html=1;fontSize=18;fontStyle=1;", 30, 20, 700, 38))
    cells.append(mx_cell("outer", f"Área total: {dims['length']} m × {dims['width']} m",
                         "rounded=0;whiteSpace=wrap;html=1;strokeWidth=3;fillColor=none;",
                         ORIGIN_X, ORIGIN_Y, dims["length"]*SCALE_PX, dims["width"]*SCALE_PX))

    for zone in layout_zones():
        cells.append(mx_cell(
            zone["id"],
            zone["name"],
            f"rounded=0;whiteSpace=wrap;html=1;fillColor={zone['fill']};strokeColor=#888;fontStyle=2;fontSize=11;",
            ORIGIN_X + zone["x_m"]*SCALE_PX,
            ORIGIN_Y + zone["y_m"]*SCALE_PX,
            zone["w_m"]*SCALE_PX,
            zone["h_m"]*SCALE_PX,
        ))

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

    node_ids: dict[int, str] = {}
    procs_by_num = {p["number"]: p for p in results["processes"]}
    for num, (mx_pos, my_pos) in MAPO_POS.items():
        pid = f"mp{num}"
        node_ids[num] = pid
        proc = procs_by_num[num]
        fill = PROCESS_COLORS.get(proc["type"], "#FFFFFF")
        cells.append(mx_cell(pid, str(num),
            f"ellipse;whiteSpace=wrap;html=1;fillColor={fill};strokeColor=#333;fontStyle=1;fontSize=11;",
            ORIGIN_X + mx_pos*SCALE_PX - 20,
            ORIGIN_Y + my_pos*SCALE_PX - 20,
            40, 40,
        ))

    flow_order = (
        list(range(1, 11)) +
        [2, 11, 12, 13, 14, 15, 16, 17] +
        [10, 18] + [17, 18] +
        list(range(18, 27))
    )
    seen_edges: set[tuple[int,int]] = set()
    flow_edges = (
        [(i, i+1) for i in range(1, 10)] +
        [(2, 11)] + [(i, i+1) for i in range(11, 17)] +
        [(10, 18), (17, 18)] +
        [(i, i+1) for i in range(18, 26)]
    )
    for idx, (a, b) in enumerate(flow_edges):
        if (a, b) not in seen_edges:
            seen_edges.add((a, b))
            cells.append(mx_edge(f"mf{idx}", node_ids[a], node_ids[b], str(b)))

    output = ROOT / "03_diagramas" / "mapofluxograma.drawio"
    output.write_text(wrap_mxfile("Mapofluxograma", cells, width=1400, height=900), encoding="utf-8")
```

Update the call to `write_mapoflow` in `main()` from `write_mapoflow(results)` to `write_mapoflow(results, project)`.

- [ ] **Step 2: Run regeneration**

```powershell
.\scripts\run_all.ps1
```

- [ ] **Step 3: Verify mapofluxograma**

Open `06_dashboard/entregaveis/mapofluxograma.html`. Verify:
- All 26 process circles visible, each labeled with its number
- Arrows connect consecutive processes following flow order
- Metal track (green arrows), wood track (brown arrows), single track (black) visible
- Both process 10 and process 17 arrows converge at process 18
- Process nodes positioned within their correct functional zones

- [ ] **Step 4: Commit**

```powershell
git add scripts/generate_outputs.py 06_dashboard/renders/mapofluxograma_render.svg 03_diagramas/mapofluxograma.drawio
git commit -m "feat: rebuild mapofluxograma with all 26 process nodes and color-coded flow tracks"
```

---

## Task 8: Write `scripts/build_latex.py`

**Files:**
- Create: `scripts/build_latex.py`
- Create dir: `07_latex/figuras/`

- [ ] **Step 1: Create `07_latex/` directory**

```powershell
New-Item -ItemType Directory -Force "C:\Users\dvill\Projeto_Fabrica_Tramontina_22399036\07_latex\figuras"
```

- [ ] **Step 2: Create `scripts/build_latex.py`**

Create `C:\Users\dvill\Projeto_Fabrica_Tramontina_22399036\scripts\build_latex.py` with this content:

```python
"""
Build LaTeX report (abntex2) for Overleaf.

Usage:
    python scripts/build_latex.py

Outputs:
    07_latex/relatorio_tecnico.tex
    07_latex/figuras/*.svg   (copies from 06_dashboard/renders/)

Compilation: Upload 07_latex/ to Overleaf. Set compiler to XeLaTeX.
             The svg package requires shell-escape (enabled on Overleaf by default).
"""

from __future__ import annotations
import json
import shutil
from html import escape as he
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


def tex_escape(s: str) -> str:
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


def members_str(project: dict) -> str:
    return " \\\\\n".join(
        tex_escape(m["name"]) for m in project["metadata"].get("group_members", [])
    )


def bom_table(results: dict) -> str:
    rows = ""
    for i, row in enumerate(results["bom"]):
        rows += (
            f"  {tex_escape(row['component'])} & {row['quantity']} & "
            f"{tex_escape(row['unit'])} & {tex_escape(row['make_or_buy'])} \\\\\n"
        )
    return (
        "\\begin{table}[H]\n"
        "\\IBGEtab{\\caption{Tabela 1 — Componentes, Quantidades e Decisão Fazer/Comprar}\\label{tab:bom}}{}\n"
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
    rows = ""
    type_map = {
        "operacao": "Operação", "transporte": "Transporte",
        "inspecao": "Inspeção", "armazenagem": "Armazenagem", "espera": "Espera",
    }
    for p in results["processes"]:
        rows += (
            f"  {p['number']} & {tex_escape(p['name'])} & "
            f"{type_map.get(p['type'], p['type'])} & "
            f"{tex_escape(p['resource'])} \\\\\n"
        )
    return (
        "\\begin{longtable}{p{0.6cm}p{5.5cm}p{2.8cm}p{5.5cm}}\n"
        "\\caption{Tabela 2 — Processos de Fabricação}\\label{tab:processos}\\\\\n"
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
        dim_str = f"{dims.get('length','?')} × {dims.get('width','?')} × {dims.get('height','?')} m"
        rows += (
            f"  {tex_escape(eq['type'])} & {tex_escape(eq['supplier'])} & "
            f"{tex_escape(eq['model'])} & {tex_escape(dim_str)} & "
            f"{tex_escape(eq['official_capacity'])} \\\\\n"
        )
    return (
        "\\begin{longtable}{p{3.5cm}p{2.5cm}p{2.5cm}p{2.8cm}p{3.0cm}}\n"
        "\\caption{Tabela 3 — Equipamentos Selecionados}\\label{tab:equipamentos}\\\\\n"
        "\\toprule\n"
        "Tipo & Fornecedor & Modelo & Dimensões (m) & Capacidade Fabricante \\\\\n"
        "\\midrule\n"
        "\\endfirsthead\n"
        "\\multicolumn{5}{c}{\\tablename\\ \\thetable{} -- (continuação)}\\\\\n"
        "\\toprule Tipo & Fornecedor & Modelo & Dimensões & Capacidade \\\\\\midrule\n"
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
        f"  Jornada de trabalho & {p['work_days_per_week']} dias × {p['shifts_per_day']} turno × {p['useful_hours_per_shift']} h úteis/dia \\\\\n"
        f"  Horas úteis semanais & {d['useful_hours_per_week']:.1f} h/semana \\\\\n"
        f"  Ritmo médio necessário & {d['required_average_rate_kits_per_hour']:.2f} kits/h \\\\\n"
        f"  Eficiência geral & {p['general_efficiency']:.0%} \\\\\n"
        f"  Confiabilidade dos equipamentos & {p['equipment_reliability']:.0%} \\\\\n"
    )
    return (
        "\\begin{table}[H]\n"
        "\\IBGEtab{\\caption{Quadro Resumo — Meta e Premissas de Produção}\\label{tab:meta}}{}\n"
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
    return (
        f"O equipamento selecionado para apresentação detalhada da memória de cálculo é "
        f"\\textbf{{{tex_escape(s['equipment_type'])}}} — {tex_escape(s['supplier'])} {tex_escape(s['model'])}.\n\n"
        f"\\textbf{{Motivo da seleção:}} {tex_escape(s['reason'])}\n\n"
        f"\\textbf{{Operação(ões):}} {tex_escape(', '.join(s['operations']))}\n\n"
        "\\begin{table}[H]\n"
        "\\IBGEtab{\\caption{Memória de Cálculo — Router CNC Maksiwa RTC.1313}\\label{tab:calc_router}}{}\n"
        "\\begin{tabular}{ll}\n"
        "\\toprule\n"
        "Parâmetro & Valor \\\\\n"
        "\\midrule\n"
        f"  Tempo padrão por kit & {s['standard_time_seconds_per_kit']:.0f} s/kit \\\\\n"
        f"  Taxa nominal & 3600 / {s['standard_time_seconds_per_kit']:.0f} s = {s['nominal_rate_from_standard_time']:.2f} kits/h \\\\\n"
        f"  Eficiência geral & {s['efficiency']:.0%} \\\\\n"
        f"  Confiabilidade & {s['reliability']:.0%} \\\\\n"
        f"  Rendimento do processo & {s['process_yield']:.0%} \\\\\n"
        f"  Taxa efetiva & {s['nominal_rate_used']:.2f} × {s['efficiency']:.2f} × {s['reliability']:.2f} × {s['process_yield']:.2f} = {s['effective_rate_kits_per_hour']:.2f} kits/h \\\\\n"
        f"  Capacidade semanal por máquina & {s['weekly_capacity_per_machine']:.2f} kits/semana \\\\\n"
        f"  Demanda bruta semanal & {s['demand_input_kits_per_week']:.0f} kits/semana \\\\\n"
        f"  Quantidade necessária & $\\lceil {s['demand_input_kits_per_week']:.0f} / {s['weekly_capacity_per_machine']:.2f} \\rceil = {s['required_quantity']}$ unidade(s) \\\\\n"
        f"  Utilização estimada & {s['utilization']:.1%} \\\\\n"
        "\\bottomrule\n"
        "\\end{tabular}\n"
        "{\\legend{Fonte: dados do fabricante (Maksiwa Store) e premissas de engenharia. "
        "Fórmula: $N = \\lceil D / (T \\times H \\times E \\times C \\times R) \\rceil$.}}\n"
        "\\end{table}\n"
    )


def references_section(project: dict) -> str:
    lines = []
    for src in project.get("sources", []):
        url = src.get("url", "")
        title = tex_escape(src.get("title", src["id"]))
        if url.startswith("http"):
            lines.append(
                f"\\bibitem{{{src['id']}}} {title}. "
                f"Disponível em: \\url{{{url}}}. Acesso em: {project['metadata']['access_date']}."
            )
        else:
            lines.append(f"\\bibitem{{{src['id']}}} {title}.")
    return "\n".join(lines)


def build_tex(project: dict, results: dict) -> str:
    members = members_str(project)
    objectives = "\n".join(f"  \\item {tex_escape(o)}" for o in project.get("project_objectives", []))
    segments_body = ""
    for seg in project.get("market_segments", []):
        segments_body += (
            f"\\textbf{{{tex_escape(seg['name'])}}} --- {tex_escape(seg['description'])} "
            f"{tex_escape(seg['justification'])}\n\n"
        )
    c = project.get("conclusions", {})
    improvements = "\n".join(f"  \\item {tex_escape(imp)}" for imp in c.get("improvements", []))
    layout = results["layout"]

    return rf"""% =======================================================
% Relatório Técnico — Projeto de Fábrica
% Kit para Churrasco Tramontina 22399036
% UFF — Niterói
% Gerado automaticamente por scripts/build_latex.py
% NÃO EDITAR MANUALMENTE — editar data/projeto.json
% Compilar no Overleaf com XeLaTeX (svg package requer shell-escape)
% =======================================================
\documentclass[12pt,a4paper,oneside,english,brazil]{{abntex2}}

\usepackage[utf8]{{inputenc}}
\usepackage[T1]{{fontenc}}
\usepackage{{lmodern}}
\usepackage{{graphicx}}
\usepackage{{booktabs}}
\usepackage{{longtable}}
\usepackage{{float}}
\usepackage{{microtype}}
\usepackage{{url}}
\usepackage{{svg}}
\usepackage{{setspace}}
\usepackage{{amsmath}}

% Dados do trabalho
\titulo{{Projeto de Fábrica --- Kit para Churrasco Tramontina com Lâminas em Aço Inox e Cabos em Madeira Natural 3 Peças (ref. 22399036)}}
\autor{{{members}}}
\local{{Niterói, RJ}}
\data{{\the\year}}
\instituicao{{Universidade Federal Fluminense (UFF)}}

\begin{{document}}

\imprimircapa

\pdfbookmark[0]{{\contentsname}}{{toc}}
\tableofcontents*
\clearpage

% -------------------------------------------------------
\chapter{{Objetivos do Projeto}}
% -------------------------------------------------------
\begin{{itemize}}
{objectives}
\end{{itemize}}

% -------------------------------------------------------
\chapter{{Descrição do Produto}}
% -------------------------------------------------------
O produto a ser fabricado é o \textbf{{Kit para Churrasco Tramontina com Lâminas em Aço Inox e Cabos em Madeira Natural 3 Peças}}, referência \textbf{{22399036}}, composto por faca chef 8 polegadas, garfo trinchante e tábua retangular de madeira Maçaranduba.

\begin{{figure}}[H]
  \centering
  \includesvg[width=0.7\textwidth]{{figuras/fluxograma_render}}
  \caption{{Produto principal — Kit Churrasco Tramontina 22399036}}
  \legend{{Fonte: Tramontina. Disponível em: tramontina.com.br.}}
\end{{figure}}

Dimensões da embalagem: {results['product']['package_dimensions_cm']['height']} cm (altura) × {results['product']['package_dimensions_cm']['length']} cm (comprimento) × {results['product']['package_dimensions_cm']['width']} cm (largura). Peso: {results['product']['package_weight_kg']} kg.

Materiais: lâminas em aço inox AISI 420, cabos em madeira natural, rebites de alumínio, tábua em madeira Maçaranduba com certificação FSC C125626.

% -------------------------------------------------------
\chapter{{Estrutura do Produto (Itens Pais e Filhos)}}
% -------------------------------------------------------
O kit embalado (item pai) é composto pelos seguintes itens filhos:

\begin{{itemize}}
  \item Faca chef 8 pol. com lâmina em aço inox, cabo de madeira natural e rebites de alumínio (Fazer)
  \item Garfo trinchante com lâmina em aço inox, cabo de madeira natural e rebites de alumínio (Fazer)
  \item Tábua retangular em madeira Maçaranduba com acabamento natural (Fazer)
  \item Cartela/cinta impressa da embalagem (Comprar)
  \item Blister/suporte plástico transparente (Comprar)
  \item Etiqueta/código de barras/rastreabilidade (Comprar)
  \item Caixa de transporte para envio (Comprar)
\end{{itemize}}

% -------------------------------------------------------
\chapter{{Segmentos de Mercado}}
% -------------------------------------------------------
{segments_body}

% -------------------------------------------------------
\chapter{{Meta Semanal de Produção}}
% -------------------------------------------------------
A meta estabelecida é de \textbf{{{results['demand']['target_good_kits_per_week']:.0f} kits bons por semana}}, definida com base no porte de uma operação industrial de médio porte para produtos de cutelaria com demanda nacional consolidada.

{demand_table(results)}

% -------------------------------------------------------
\chapter{{Tabela 1 --- Componentes, Quantidades e Fazer/Comprar}}
% -------------------------------------------------------
A tabela a seguir apresenta os componentes considerados para uma unidade de produto embalada para envio.

{bom_table(results)}

% -------------------------------------------------------
\chapter{{Tabela 2 --- Processos de Fabricação}}
% -------------------------------------------------------
O processo produtivo é dividido em 26 etapas, distribuídas em trilha metálica (processos 1–10), trilha madeira (processos 2 e 11–17), montagem e embalagem (processos 18–26).

{process_table(results)}

% -------------------------------------------------------
\chapter{{Fluxograma do Processo}}
% -------------------------------------------------------

\begin{{figure}}[H]
  \centering
  \includesvg[width=\textwidth]{{figuras/fluxograma_render}}
  \caption{{Fluxograma do processo industrial --- símbolos ASME}}
  \legend{{Fonte: elaborado pelos autores.}}
\end{{figure}}

% -------------------------------------------------------
\chapter{{Tabela 3 --- Equipamentos Selecionados}}
% -------------------------------------------------------

{equipment_table(results)}

% -------------------------------------------------------
\chapter{{Cálculo do Equipamento Selecionado}}
% -------------------------------------------------------

{selected_eq_section(results)}

% -------------------------------------------------------
\chapter{{Arranjo Físico Esquemático}}
% -------------------------------------------------------
A fábrica proposta ocupa uma área de {layout['layout_dimensions_m']['length']} m × {layout['layout_dimensions_m']['width']} m = {layout['layout_total_area_m2']:.0f} m². A área requerida calculada é de {layout['total_required_area_m2']:.1f} m², resultando em uma taxa de ocupação de {layout['occupancy']*100:.1f}\%.

\begin{{figure}}[H]
  \centering
  \includesvg[width=\textwidth]{{figuras/layout_render}}
  \caption{{Arranjo físico esquemático --- equipamentos e zonas funcionais}}
  \legend{{Fonte: elaborado pelos autores.}}
\end{{figure}}

% -------------------------------------------------------
\chapter{{Mapofluxograma}}
% -------------------------------------------------------

\begin{{figure}}[H]
  \centering
  \includesvg[width=\textwidth]{{figuras/mapofluxograma_render}}
  \caption{{Mapofluxograma --- fluxo dos 26 processos sobre o arranjo físico}}
  \legend{{Fonte: elaborado pelos autores.}}
\end{{figure}}

% -------------------------------------------------------
\chapter{{Conclusões}}
% -------------------------------------------------------

{tex_escape(c.get('summary', ''))}

\textbf{{Gargalo identificado:}} {tex_escape(c.get('bottleneck_note', ''))}

\textbf{{Observação sobre o arranjo físico:}} {tex_escape(c.get('layout_note', ''))}

\textbf{{O que seria necessário para aprimorar o projeto:}}

\begin{{itemize}}
{improvements}
\end{{itemize}}

% -------------------------------------------------------
\bibliography{{referencias}}
% -------------------------------------------------------

\end{{document}}
"""


def build_bib(project: dict) -> str:
    lines = ["@misc{placeholder,"]
    for src in project.get("sources", []):
        url = src.get("url", "")
        title = src.get("title", src["id"])
        bib_id = src["id"].replace("-", "_")
        if url.startswith("http"):
            lines.append(
                f"@misc{{{bib_id},\n"
                f"  author = {{{{Tramontina/Fabricante}}}},\n"
                f"  title  = {{{{{title}}}}},\n"
                f"  howpublished = {{\\url{{{url}}}}},\n"
                f"  note   = {{Acesso em: {project['metadata']['access_date']}}},\n"
                "}"
            )
    return "\n\n".join(lines[1:])


def main() -> None:
    project, results = load()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    # Copy SVG renders to figuras/
    renders_dir = ROOT / "06_dashboard" / "renders"
    for svg_file in renders_dir.glob("*.svg"):
        shutil.copy2(svg_file, FIG_DIR / svg_file.name)
        print(f"  Copied {svg_file.name} → 07_latex/figuras/")

    # Write .tex
    tex_content = build_tex(project, results)
    (OUT_DIR / "relatorio_tecnico.tex").write_text(tex_content, encoding="utf-8")
    print("  Written: 07_latex/relatorio_tecnico.tex")

    # Write .bib
    bib_content = build_bib(project)
    (OUT_DIR / "referencias.bib").write_text(bib_content, encoding="utf-8")
    print("  Written: 07_latex/referencias.bib")

    print()
    print("LaTeX package ready.")
    print("Upload the contents of 07_latex/ to Overleaf.")
    print("Set compiler: XeLaTeX (required for svg package).")


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Run the script manually to verify**

```powershell
$Python = "C:\Users\dvill\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
Set-Location "C:\Users\dvill\Projeto_Fabrica_Tramontina_22399036"
& $Python scripts\build_latex.py
```

Expected output:
```
  Copied fluxograma_render.svg → 07_latex/figuras/
  Copied layout_render.svg → 07_latex/figuras/
  Copied mapofluxograma_render.svg → 07_latex/figuras/
  Written: 07_latex/relatorio_tecnico.tex
  Written: 07_latex/referencias.bib

LaTeX package ready.
Upload the contents of 07_latex/ to Overleaf.
Set compiler: XeLaTeX (required for svg package).
```

- [ ] **Step 4: Verify output files**

```powershell
Test-Path "07_latex\relatorio_tecnico.tex"
Test-Path "07_latex\referencias.bib"
Test-Path "07_latex\figuras\fluxograma_render.svg"
```
Expected: all `True`.

- [ ] **Step 5: Spot-check .tex file**

```powershell
Select-String "\\chapter{" 07_latex\relatorio_tecnico.tex
```

Expected: 13 lines output (one chapter per section — Objetivos through Conclusões).

- [ ] **Step 6: Commit**

```powershell
git add scripts/build_latex.py 07_latex/
git commit -m "feat: add build_latex.py — generates abntex2 report for Overleaf"
```

---

## Task 9: Update `run_all.ps1`

**Files:**
- Modify: `scripts/run_all.ps1`

- [ ] **Step 1: Add `build_latex.py` call**

Replace the content of `scripts/run_all.ps1` with:

```powershell
$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Python = "C:\Users\dvill\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
$Node = "C:\Users\dvill\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe"
$NodeModules = Join-Path $Root "node_modules"
$BundledNodeModules = "C:\Users\dvill\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules"

if (-not (Test-Path $NodeModules)) {
  New-Item -ItemType Junction -Path $NodeModules -Target $BundledNodeModules | Out-Null
}

Push-Location $Root
try {
  Write-Host "[1/3] generate_outputs.py ..."
  & $Python (Join-Path $Root "scripts\generate_outputs.py")
  Write-Host "[2/3] build_workbook.mjs ..."
  & $Node (Join-Path $Root "scripts\build_workbook.mjs")
  Write-Host "[3/3] build_latex.py ..."
  & $Python (Join-Path $Root "scripts\build_latex.py")
  Write-Host "Done. Open 06_dashboard\index.html to review."
  Write-Host "LaTeX ready at 07_latex\relatorio_tecnico.tex — upload to Overleaf (XeLaTeX)."
}
finally {
  Pop-Location
}
```

- [ ] **Step 2: Run full regeneration end-to-end**

```powershell
Set-Location "C:\Users\dvill\Projeto_Fabrica_Tramontina_22399036"
.\scripts\run_all.ps1
```

Expected: all three scripts complete, final messages printed.

- [ ] **Step 3: Commit**

```powershell
git add scripts/run_all.ps1
git commit -m "build: update run_all.ps1 to include build_latex.py as step 3"
```

---

## Task 10: Final Verification — All 14 Assignment Items

- [ ] **Step 1: Run full regeneration**

```powershell
.\scripts\run_all.ps1
```

- [ ] **Step 2: Check all 14 items against OBJETIVO.md**

Open `06_dashboard/index.html` in a browser and verify each item:

| Item | Check |
|------|-------|
| 1 – Members | Dashboard header shows 5 member names |
| 2 – Objectives | `entregaveis/objetivos.html` has 5 bullet objectives |
| 3 – Product + images | Dashboard product cards show images + technical drawing |
| 4 – BOM tree | Table 1 in calculos.html lists 7 components |
| 5 – Market segments | `entregaveis/mercado.html` shows 4 segments with justifications |
| 6 – Weekly goal | calculos.html shows 1,000 kits/week + premises table |
| 7 – Table 1 | calculos.html table has component / qty / unit / make-buy columns |
| 8 – Table 2 | calculos.html process section shows all 26 rows |
| 9 – Flowchart | `entregaveis/fluxograma.html` shows ASME shapes + 2 tracks |
| 10 – Table 3 | calculos.html equipment table shows 11 rows with official capacities |
| 11 – Calc selected equip | memoria.html shows Router CNC calculation with formula |
| 12 – Layout | `entregaveis/layout.html` shows equipment footprints + 9 zones + dimensions |
| 13 – Mapo | `entregaveis/mapofluxograma.html` shows all 26 process nodes on layout |
| 14 – Conclusions | `entregaveis/conclusoes.html` shows summary + bottleneck + improvements |

- [ ] **Step 3: Upload LaTeX to Overleaf**

1. Go to Overleaf and create a new project
2. Upload all files from `07_latex/` (including the `figuras/` subfolder)
3. Set compiler to **XeLaTeX** in project settings
4. Click Compile
5. Verify PDF generates with all 13 chapters and figures

- [ ] **Step 4: Fix any compilation issues**

Common Overleaf issues:
- `svg` package not found → add `\usepackage{svg}` is already there; ensure XeLaTeX is selected
- Missing `figuras/` folder → re-upload the figuras subfolder
- `abntex2` not found → it's in TeX Live on Overleaf; no action needed

- [ ] **Step 5: Final commit**

```powershell
git add -A
git commit -m "feat: all 14 assignment items complete — content, detailed diagrams, LaTeX report"
```

---

## Spec Coverage Check

| Spec requirement | Tasks |
|-----------------|-------|
| Root OBJETIVO.md | Task 1 |
| project_objectives in JSON | Task 2 |
| market_segments in JSON | Task 2 |
| conclusions in JSON | Task 2 |
| HTML pages for 3 new blocks | Task 3 |
| Dashboard cards for new pages | Task 3 |
| Excel sheets for new blocks | Task 4 |
| Flowchart ASME symbols, 2 tracks | Task 5 |
| Layout equipment footprints + zones + dims | Task 6 |
| Mapofluxograma all 26 processes | Task 7 |
| build_latex.py with abntex2 | Task 8 |
| run_all.ps1 updated | Task 9 |
| Final 14-item verification | Task 10 |
