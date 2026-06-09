# Design: polish_presentation.py

**Data:** 2026-06-09  
**Objetivo:** Polir o PPTX do grupo usando-o como base, inserindo os renders faltantes e corrigindo os dados que divergem do que foi decidido.

---

## Entradas / Saídas

| Item | Caminho |
|---|---|
| Base | `C:\Users\dvill\Downloads\Projeto de Fábrica - Kit Churrasco Tramontina (1).pptx` |
| Renders SVG | `06_dashboard/renders/*.svg` |
| Saída | `01_apresentacao/apresentacao_final.pptx` |

---

## Decisões técnicas fixadas

- Meta: **1.000 kits/semana** (não 2.000)
- Layout: **384 m² — 24 × 16 m** (não 800 m²)
- Equipamento destaque: **Laser Fibra CNC** (não Prensa Excêntrica)
- Tábua e cabos: **FAZER** internamente
- Tábua: **340 × 190 × 15 mm**, madeira **Maçaranduba**
- Integrantes confirmados: Adrian Vilela, André Baptista, Bernardo Gomes, Clara Barboza, João Pedro Deccax, Leonardo Nespoli, Lucas de Mello

---

## Operações do script (em ordem)

### 1. Renders SVG → PNG via Playwright

Reusar `_svg_to_png()` de `build_presentation.py`.

| SVG | PNG(s) gerados |
|---|---|
| `fluxograma_render.svg` | `fluxo_top.png` (0–58% da altura) e `fluxo_bot.png` (42–100%) |
| `layout_render.svg` | `layout.png` |
| `mapofluxograma_render.svg` | `mapo.png` |

Sobreposição de 16% no fluxograma garante que nenhum processo é cortado na divisão.

### 2. Inserção de slides de diagrama

Slide inserido após o atual **slide 11** ("PAIS E FILHOS"), deslocando os demais:

| Novo slide | Conteúdo | Título |
|---|---|---|
| 12 | `fluxo_top.png` | Fluxograma do Processo (1/2) |
| 13 | `fluxo_bot.png` | Fluxograma do Processo (2/2) |

Após inserção, os slides de layout e mapofluxograma passam a ser slides **17** e **18**.

- Slide 17 (era 15 — arranjo físico em branco): inserir `layout.png`
- Slide 18 (era 16 — mapofluxograma em branco): inserir `mapo.png`

Imagens ocupam a área útil do slide abaixo do título existente. Não substituir o slide inteiro — só adicionar a imagem.

### 3. Correções de texto

Varrer todos os `TextFrame` do arquivo e aplicar substituições exatas:

| Encontrar | Substituir |
|---|---|
| `5.000 kits semanais` | `1.000 kits semanais` |
| `2.000 kits por semana` | `1.000 kits por semana` |
| `2.000` (em contexto de kits/meta) | `1.000` |
| `400 kits` (diário) | `200 kits` |
| `50 kits / hora` | `30 kits / hora` |
| `60,7 kits / hora` | `30,9 kits / hora` |
| `800m²` / `800 m²` | `384 m²` |
| `40m x 20m` / `40 × 20` | `24 × 16 m` |
| `Eucalipto/Pinus` | `Maçaranduba` |
| `Madeira Certificada` | `Madeira Maçaranduba` |
| `350 x 220 x 18` | `340 x 190 x 15` |
| `Prensa Excêntrica` (slide de seleção) | `Laser Fibra CNC` |
| `Harlo do Brasil` (no slide de seleção) | `Madetech (SP)` |
| `60 golpes/min` (no slide de seleção) | `20.000 mm/min` |

Substituição **case-insensitive, só texto — não tocar em formas, cores ou posições**.

O slide de cálculo detalhado (atual slide 20) tem os números da prensa escritos em caixas de texto livres. Substituições acima cobrem os valores numéricos. Se a fórmula narrativa não for coberta por substituição simples, deixar uma nota `# TODO` no código para ajuste manual posterior.

### 4. Padronização de fontes

Varrer todos os `TextFrame` e aplicar regras mínimas — não destrutivas:

- Qualquer `run.font.size` menor que `Pt(9)` → elevar para `Pt(9)` (tabelas)
- Corpo de texto livre (fora de tabelas) menor que `Pt(12)` → elevar para `Pt(12)`
- Não reduzir nenhum tamanho que já esteja correto
- Não alterar bold, cor, nem alinhamento

### 5. Saída

Salvar em `01_apresentacao/apresentacao_final.pptx`.  
Não sobrescrever o arquivo original.  
Adicionar ao `run_all.ps1` como passo `[5/5]`.

---

## O que o script NÃO faz

- Não altera layout visual (cores de fundo, posições, formas)
- Não reescreve parágrafos inteiros — só substituições pontuais
- Não mexe em slides que já estão corretos
- Não gera novo conteúdo além dos renders já existentes

---

## Arquivos afetados

| Arquivo | Ação |
|---|---|
| `scripts/polish_presentation.py` | Criar |
| `scripts/run_all.ps1` | Adicionar passo 5/5 |
| `01_apresentacao/apresentacao_final.pptx` | Criar (gerado) |
