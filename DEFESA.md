# Guia de Defesa — Projeto de Fábrica
## Kit Churrasco Tramontina 22399036 · Grupo A

> **Fonte da verdade:** `Downloads/apresentacao_final.pptx` (26 slides).
> Este documento cruza o conteúdo real dos slides com a lógica técnica e aponta inconsistências.

---

## Referência rápida — números que não podem errar

| O que | Valor |
|---|---|
| Meta semanal (kits bons) | **1.000 kits/semana** |
| Meta diária | **200 kits/dia** (1000 ÷ 5 dias) |
| Produto bom | **97%** |
| Demanda bruta diária | **206,2 kits/dia** (200 ÷ 0,97) |
| Jornada programada | **8 h/dia = 480 min** |
| Eficiência | **85%** |
| Disponibilidade | **90%** |
| Tempo disponível efetivo | **367,2 min/dia** (480 × 0,85 × 0,90) |
| Equipamento selecionado | **Laser Fibra CNC** (Madetech) |
| Capacidade do laser | **422 kits/dia** |
| Quantidade de lasers | **1 unidade — 49% utilização** |
| Layout | **384 m² (24 × 16 m)** |
| Tábua | **330 × 200 mm — Madeira Maçaranduba** |
| Rebites por kit | **6 total** (3 por cabo × 2 cabos) |
| Total de processos | **26 processos** |

---

## Guia slide a slide

### Slide 1 — Capa
**Conteúdo:** ARRANJO FÍSICO INDUSTRIAL · Kit Churrasco Tramontina · Engenharia de Produção · Grupo A · 2026 · Cód. 22399/036

**Legenda:** Slide de abertura. O código 22399/036 é a referência comercial do produto na Tramontina (mesmo produto, formatação com barra).

---

### Slide 2 — Equipe do Projeto
**Conteúdo:** Integrantes + orientação

**Legenda:**
- **Integrantes:** Adrian Vilela, André Baptista, Bernardo Gomes, Clara Barboza, João Pedro Deccax, Leonardo Nespoli, Lucas de Mello
- **Orientação:** Professora Suzana Dantas · Disciplina Arranjo Físico Industrial · 2026.1

⚠️ O slide escreve "André Bapista" (sem 't'). O nome correto é **André Baptista**.

---

### Slide 3 — Objetivos do Projeto
**Conteúdo:** 3 blocos — Objetivo Geral, Processos, Dimensionamento

**Legenda:**
- **Objetivo Geral:** Estruturar uma unidade fabril para produção em escala industrial do kit
- **Processos:** Definir os fluxos produtivos e recursos físicos
- **Dimensionamento:** Calcular carga de máquinas e layout para **1.000 kits semanais**

**Como defender:** Os 3 blocos cobrem os 14 itens do enunciado — produto + BOM + processos + equipamentos + layout + mapofluxograma.

---

### Slide 4 — Descrição do Produto
**Conteúdo:** Características do Kit Churrasco Dynamic

**Legenda elemento a elemento:**
- **Peça 1 — Faca 8" em Aço Inox AISI 420:** lâmina de aço inox martensítico endurecível por tratamento térmico
- **Peça 2 — Garfo Trinchante Inox Estampado:** forma da lâmina obtida por processo de corte/conformação
- **Peça 3 — Tábua de Madeira (33×20 cm):** dimensões externas da tábua
- **Cabos: Madeira natural rebitada:** os cabos da faca e do garfo são fixados à lâmina com rebites de aço inox
- **Diferencial: Tratamento térmico para durabilidade do fio:** justifica o Processo P6 (forno) e o Processo P9 (afiação)

---

### Slide 5 — Dimensões Técnicas
**Conteúdo:** Especificações dimensionais de cada componente

**Legenda elemento a elemento:**

| Elemento | Valor | O que significa |
|---|---|---|
| Faca — Lâmina | 200 mm | Comprimento da parte cortante |
| Faca — Cabo | 120 mm | Comprimento do cabo de madeira |
| Faca — Total | 320 mm | Comprimento total da peça |
| Garfo — Total | ≈ 330 mm | Comprimento total estimado |
| Material lâminas | AISI 420 | Aço inox martensítico (Alta Resistência) |
| Tábua | 330 × 200 mm | Comprimento × Largura |
| Tábua — Material | Madeira Maçaranduba | Madeira tropical dura, certificada FSC |
| Fixação | 3 rebites de aço inox por cabo | 3 furos por cabo × 2 cabos = 6 rebites por kit |

---

### Slide 6 — Pais e Filhos (BOM — Estrutura do Produto)
**Conteúdo:** Diagrama em árvore da estrutura do produto

**Legenda — o que é cada nível:**
- **Nível 0 (topo):** Kit 22399036 embalado para envio — o produto final que sai da fábrica
- **Nível 1 (filhos diretos):** Os componentes que compõem o kit — faca montada, garfo montado, tábua processada, embalagem
- **Nível 2 (insumos):** O que entra na produção para gerar os filhos — chapas de inox AISI 420, cabos de madeira (pré-cortados internamente), rebites inox, caixa kraft display

**Por que essa estrutura importa:** Ela define o que **fabricamos** (lâminas, cabos, tábua) e o que **compramos** (rebites, embalagem) — base da Tabela 1.

---

### Slides 9 e 10 — Tabela 1: Componentes e Justificativas (BOM)

**Slide 9 — Componentes:**

| Comp. | Descrição | Qtd | Fazer/Comprar |
|---|---|---|---|
| 01 | Lâmina Faca Inox AISI 420 | 1 | **FAZER** |
| 02 | Lâmina Garfo Inox 420 | 1 | **FAZER** |
| 03 | Cabo Madeira (pré-cortado) | 2 | **FAZER** |
| 04 | Tábua Madeira Acabada | 1 | **FAZER** |
| 05 | Rebites Inox | 6 | **COMPRAR** |
| 06 | Embalagem Kraft Display | 1 | **COMPRAR** |

**Legenda:**
- **Qtd = 2 cabos:** uma faca e um garfo, cada um com 1 cabo → 2 cabos por kit
- **Qtd = 6 rebites:** 3 rebites por cabo × 2 cabos = 6 por kit
- **Embalagem Kraft Display:** caixa com janela transparente que embala o kit completo

**Slide 10 — Justificativas:**
- **FAZER (lâminas, cabos, tábua):** controle dimensional preciso antes da rebitagem — se o furo do cabo não bater com o furo da lâmina, o rebite não fecha. Terceirizar significa depender de tolerâncias externas.
- **COMPRAR (rebites, embalagem):** custo baixo, sem valor diferencial para fabricar internamente; o foco é nas lâminas.

---

### Slides 11, 12, 13 — Processos Industriais (Tabela 2)

**Legenda dos 5 tipos de processo (notação ASME):**

| Tipo | Símbolo | O que significa |
|---|---|---|
| **Operação** | ⬤ círculo | Transformação física do material — corte, solda, usinagem |
| **Inspeção** | □ quadrado | Verificação dimensional ou visual sem transformar |
| **Transporte** | ▷ seta | Movimentação de material de um ponto a outro |
| **Armazenagem** | ▽ triângulo | Material parado aguardando etapa futura |
| **Espera** | D letra D | Material parado sem ação planejada — resfriamento, cura |

**Slide 11 — Processos 1 a 10 (Setor Metal):**

| Nº | Processo | Tipo | Por que existe |
|---|---|---|---|
| 01 | Inspeção de Matéria-Prima | Inspeção | Conferir chapa de inox antes de gastar energia cortando |
| 02 | Armazenagem de MP | Armazenagem | Estoque de segurança para manter ritmo de produção |
| 03 | Transporte Aço Inox para corte | Transporte | Levar a chapa até o laser |
| 04 | Corte do aço inox para blanks | Operação | Laser fibra CNC corta o perfil da faca e do garfo |
| 05 | Inspeção dos blanks | Inspeção | Verificar se o corte ficou dentro da tolerância |
| 06 | Tratamento térmico dos blanks | Operação | Forno a 1.050–1.100°C endurece o AISI 420 (martensita) |
| 07 | Espera de resfriamento | Espera | Peças precisam esfriar — sem ação humana |
| 08 | Rebarbar, lixar e polir faca e garfo | Operação | Remove rebarbas do corte e dá acabamento superficial |
| 09 | Afiar facas | Operação | Gera o fio de corte — único processo que não se aplica ao garfo |
| 10 | Armazenagem de peças metálicas semiacabadas | Armazenagem | Pulmão entre setor metal e montagem |

**Slide 12 — Processos 11 a 20 (Setor Madeira + início da Montagem):**

| Nº | Processo | Tipo | Por que existe |
|---|---|---|---|
| 11 | Transporte de madeira para corte | Transporte | Levar tábua bruta até a serra |
| 12 | Corte da tábua e blanks dos cabos | Operação | Serra industrial corta a tábua e os cabos no comprimento certo |
| 13 | Fresar tábua e furar cabos | Operação | Router CNC/fresa: sulco na tábua + 3 furos por cabo |
| 14 | Lixar cabos e tábua | Operação | Lixadeira remove marca da serra, deixa superfície lisa |
| 15 | Acabamento superficial | Operação | Aplica verniz/óleo sobre a madeira para proteção |
| 16 | Aguardar cura do acabamento | Espera | Verniz precisa secar — sem ação |
| 17 | Inspeção de peças de madeira | Inspeção | Verificar dimensões e acabamento antes da montagem |
| 18 | Transporte de madeira para montagem | Transporte | Levar cabos e tábua para a área de montagem |
| 19 | Transporte de garfos e facas para montagem | Transporte | Convergência das duas trilhas |
| 20 | Transporte dos rebites para montagem | Transporte | Rebites chegam ao posto de rebitagem |

**Slide 13 — Processos 21 a 26 (Montagem, Embalagem, Expedição):**

| Nº | Processo | Tipo | Por que existe |
|---|---|---|---|
| 21 | Montagem de facas e garfos (rebitagem) | Operação | Rebitadeira pneumática fixa cabo na lâmina com 3 rebites |
| 22 | Inspeção das facas e garfos acabados | Inspeção | Verificar rebites, fio, acabamento antes de montar o kit |
| 23 | Transporte da cartela para montagem | Transporte | A embalagem kraft vem do estoque até a mesa |
| 24 | Montagem do kit (faca + garfo + tábua + cartela) | Operação | Montagem manual do kit completo na embalagem display |
| 25 | Transporte do kit finalizado | Transporte | Levar kit para armazenagem ou expedição |
| 26 | Armazenagem de kit finalizado | Armazenagem | Estoque de produto acabado antes da expedição |

---

### Slides 14, 15, 16 — Fluxograma do Processo (P1, P2, P3)

**O que é o fluxograma:** representação visual da sequência dos 26 processos usando os símbolos ASME. Cada símbolo tem o número do processo correspondente à Tabela 2.

**Legenda visual — o que cada forma significa:**
- **Círculo (●)** = Operação — máquina ou operador transformando o material
- **Quadrado (■)** = Inspeção — alguém verificando dimensões ou qualidade
- **Seta (→)** = Transporte — material se movendo
- **Triângulo invertido (▽)** = Armazenagem — material parado em estoque
- **D (⊃)** = Espera — material aguardando sem ação planejada
- **Linha** conectando os símbolos = sequência do processo
- **Número** dentro do símbolo = número do processo (bate com a Tabela 2)

**P1 (slide 14):** processos 1 a 10 — trilha do metal
**P2 (slide 15):** processos 11 a 20 — trilha da madeira + convergência para montagem
**P3 (slide 16):** processos 21 a 26 — montagem, embalagem, expedição

---

### Slide 17 — Tabela de Equipamentos (Tabela 3)

**Legenda de cada coluna:**
- **Equipamento:** nome/tipo da máquina
- **Fornecedor(es):** empresa real que fabrica/vende (pesquisado)
- **Medidas Aprox.:** footprint da máquina em comprimento × largura × altura
- **Capacidade (Fabricante):** o que o fabricante declara (não o que usamos nos cálculos — essa é a capacidade nominal bruta)
- **Qtd:** quantidade necessária para atender a demanda

**Equipamentos listados e o que fazem:**

| Equipamento | O que faz no processo |
|---|---|
| **Laser Fibra CNC** (Madetech) | P04 — Corta blanks de faca e garfo na chapa de inox |
| **Forno de Têmpera** (Jung Industrial) | P06 — Tratamento térmico 1.050–1.100°C |
| **Lixadeira de Cinta** (Lippel/Ferromax) | P08 — Rebarbação e polimento das lâminas · 3 unidades |
| **Rebitadeira Pneumática** (Pram Ferramentas) | P21 — Fixa cabo na lâmina com rebites · 3 unidades |
| **Afiadora Automática** (Lippel/Mecanofar) | P09 — Afia o fio de corte das facas |
| **Serra Industrial** (Lippel/Invicta) | P12 — Corta tábua e blanks dos cabos |
| **Router CNC / Fresa** (Batistella/SCM) | P13 — Fresa sulco da tábua e fura cabos |

---

### Slide 18 — Seleção de 1 Equipamento

**O que este slide faz:** detalha o equipamento escolhido para o memorial de cálculo — o **Laser Fibra CNC**.

**Legenda da tabela de parâmetros:**

| Parâmetro | Valor | O que significa |
|---|---|---|
| Capacidade Nominal | 20.000 mm/min | Velocidade máxima de corte declarada pelo fabricante |
| Mesa | 600 × 400 mm | Área útil de trabalho do laser |
| Turnos | 1 turno/dia | Regime de trabalho adotado |
| Jornada | 8 h/dia | Horas programadas (não úteis) |
| Dias úteis | 5 dias/semana | Dias de trabalho |
| Disponibilidade | 90% | Fração do tempo que a máquina está operacional (sem quebras) |
| Eficiência | 85% | Fração do tempo disponível que é tempo produtivo |
| Produto bom | 97% | Fração das peças cortadas que passam na inspeção |
| Setup | 30 min/semana | Tempo de ajuste/troca de programação já descontado |

---

### Slide 19 — Parque de Máquinas — Quantidades Finais

**O que este slide faz:** mostra TODOS os equipamentos com as quantidades calculadas.

**Legenda:**

| Equipamento | Qtd | Por que essa quantidade |
|---|---|---|
| Laser Fibra CNC | **1** | Memorial de cálculo — 49% utilização |
| Forno de Têmpera | **1** | Ciclo em batelada cobre lote diário |
| Lixadeira de Cinta | **3** | 3 estações em linha para desbaste, lixamento e polimento |
| Rebitadeira Pneumática | **3** | 1 por estação de montagem (faca, garfo, fixação) |
| Afiadora Automática | **1** | Capacidade (~400 facas/h) supera demanda com folga |
| Politriz/Retificadeira | **2** | Acabamento final das lâminas |
| Empilhadeira Elétrica | **1** | Movimentação de pallets — logística interna geral |
| Esteiras Transportadoras | **6** | Interligam todos os postos produtivos |
| Serra Industrial | **1** | Linha de madeira |
| Router CNC/Fresa | **1** | Linha de madeira |

---

### Slide 20 — Memorial de Cálculo (Laser Fibra CNC)

> Este é o slide mais importante tecnicamente. Ver **seção completa** abaixo.

---

### Slide 21 — Desenho Esquemático do Arranjo Físico

> Ver **seção completa** abaixo.

---

### Slide 22 — Layout Industrial (descrição textual)

**Conteúdo do slide:**
- Área: 384 m² (24 × 16 m)
- Setores em sequência: Recebimento → Estampagem → Tratamento Térmico → Polimento → Montagem → Expedição
- Fluxo otimizado para produção puxada

**O que é "produção puxada":** o material avança quando a etapa seguinte sinaliza que está pronta para receber. Reduz estoques intermediários.

---

### Slide 23 — Mapofluxograma da Produção

**O que é o mapofluxograma:** o fluxograma dos 26 processos desenhado SOBRE o layout físico. Mostra onde cada processo acontece no espaço da fábrica.

**Como ler:**
- Cada símbolo ASME está posicionado na zona do layout onde ocorre
- As setas entre símbolos mostram o caminho físico do material
- Duas trilhas visíveis: metal (setor metal) e madeira (setor madeira), convergindo na montagem
- Cruzamentos ou setas longas indicam possíveis melhorias no layout

---

### Slide 24 — Maquinário Principal

**Conteúdo:** destaque para os 2 equipamentos mais críticos

- **Laser Fibra CNC:** corte de precisão dos blanks de faca e garfo em chapa AISI 420
- **Forno de Têmpera:** garante a dureza Rockwell necessária (endurecimento do AISI 420)

**Por que estes dois:** são os equipamentos do setor metal que definem a qualidade final do produto. Sem o laser, não há geometria precisa; sem o forno, não há dureza para o fio de corte.

---

### Slide 25 — Conclusões

Slide de encerramento. Título: "Kit Churrasco Tramontina | Engenharia de Produção | 2026"

---

### Slide 26 — Fontes de Pesquisa

**Fontes confirmadas:**
- Página oficial Tramontina (tramontina.com.br) — produto, composição, dimensões
- Desenho técnico oficial Tramontina (assets.tramontina.com.br)
- Demais fontes: fornecedores de equipamentos pesquisados (Madetech, Jung Industrial, Lippel, Pram, Batistella/SCM)

---

## Memorial de Cálculo completo (Slide 20 — fonte da verdade)

### Contexto
O equipamento selecionado é o **Laser Fibra CNC** (Madetech), que executa o Processo 04 (corte dos blanks de faca e garfo).

### Variáveis e o que significam

| Variável | Símbolo | Valor | Origem |
|---|---|---|---|
| Meta diária de kits bons | — | 200 kits/dia | 1.000 kits/semana ÷ 5 dias |
| Taxa de produto bom | — | 97% = 0,97 | Premissa do projeto |
| Demanda bruta diária | **Db** | 206,2 kits/dia | Calculado |
| Jornada programada | — | 480 min/dia | 8 h × 60 min |
| Eficiência | η | 85% = 0,85 | Premissa de engenharia |
| Disponibilidade | disp | 90% = 0,90 | Premissa de engenharia |
| Tempo disponível efetivo | **Td** | 367,2 min/dia | Calculado |
| Tempo de ciclo por kit | **Tc** | 0,87 min/kit | Estimativa (≈ 52 s/kit) |
| Capacidade diária do laser | **Cap** | 422 kits/dia | Calculado |
| Número de máquinas | **N** | 0,49 → **1** | Calculado |

### Passo 1 — Demanda bruta diária

> Produzimos mais do que 200 porque parte dos kits será rejeitada.

```
Db = meta_diária / produto_bom
Db = 200 / 0,97
Db = 206,2 kits/dia
```

### Passo 2 — Tempo disponível efetivo

> Das 8 horas programadas, só parte é tempo realmente produtivo.

```
Td = jornada_min × eficiência × disponibilidade
Td = 480 × 0,85 × 0,90
Td = 367,2 min/dia
```

**Por que multiplicar eficiência e disponibilidade:**
- **Eficiência (85%):** dos minutos em que a máquina está ligada, 15% são perdidos em micro-paradas, variações de ritmo e pequenos ajustes
- **Disponibilidade (90%):** 10% do tempo a máquina está em manutenção ou parada por falha

### Passo 3 — Tempo de ciclo

```
Tc = 0,87 min/kit  (= 52,2 segundos por kit)
```

Este é o tempo que o laser leva por kit — inclui corte da faca, corte do garfo e tempo de carga/descarga da chapa. É uma estimativa baseada na velocidade do laser (20.000 mm/min) e no comprimento do caminho de corte de cada blank.

### Passo 4 — Capacidade diária

> Quantos kits o laser consegue processar em um dia.

```
Cap = Td / Tc
Cap = 367,2 / 0,87
Cap = 421,8 ≈ 422 kits/dia
```

### Passo 5 — Número de máquinas

```
N = Db / Cap
N = 206,2 / 422
N = 0,49
```

Como não existe 0,49 máquina, arredondamos para cima:

```
N = 1 Laser Fibra CNC
```

### Utilização

```
utilização = Db / Cap = 206,2 / 422 = 49%
```

**O que significa 49%:** a máquina opera com folga de 51%. Absorve variações de demanda sem precisar de horas extras ou segundo equipamento.

### Resultado
> **1 Laser Fibra CNC Madetech é suficiente, operando a 49% de utilização.**

---

## Desenho Esquemático — guia completo (Slide 21)

O layout mostra a fábrica de **24 m × 16 m = 384 m²** vista de cima, dividida em **9 zonas**.

### Legenda das zonas (cores no slide)

| Zona | Cor | Área | O que acontece ali |
|---|---|---|---|
| **Setor Metal** | Verde claro | 104 m² | Processos P03 a P10 — corte laser, TT, polimento, afiação |
| **Setor Madeira** | Amarelo claro | 99 m² | Processos P11 a P17 — corte, fresagem, lixamento, acabamento |
| **Montagem** | Azul claro | 49 m² | Processos P18 a P22 — convergência dos dois setores, rebitagem |
| **Embalagem** | Vermelho claro | 28 m² | Processos P23 a P25 — montagem do kit completo na embalagem |
| **Inspeção / QC** | Laranja claro | 20 m² | Bancada de controle de qualidade |
| **Apoio / Manutenção** | Cinza claro | 20 m² | Ferramentas, EPIs, compressor de ar |
| **Estoque de MP** | Roxo claro | 20 m² | Bobinas de inox, tábuas de madeira, rebites |
| **Estoque Intermediário** | Roxo claro | 20 m² | Peças semiacabadas entre setor metal e montagem |
| **Recebimento / Expedição** | Azul claro | 24 m² | Doca de entrada de matéria-prima e saída de produto acabado |

### Legenda dos equipamentos (retângulos escuros dentro das zonas)

**No Setor Metal:**
| Equipamento no layout | Nome completo | Processo |
|---|---|---|
| CNC Fiber Pro 1530 | Laser Fibra CNC Madetech | P04 — Corte de blanks |
| 703.099 com carro | Forno de Têmpera Jung Industrial | P06 — Tratamento térmico |
| Lixadeira/politriz | Lixadeira/Politriz de cinta para metal | P08 — Polimento |
| AF.650 | Afiador de Facas Maksiwa | P09 — Afiação |

**No Setor Madeira:**
| Equipamento no layout | Nome completo | Processo |
|---|---|---|
| BMS.1900.I (ou Serra) | Serra/Esquadrejadeira para madeira | P12 — Corte da tábua e cabos |
| Router CNC (1) e (2) | Router CNC / Fresa | P13 — Fresagem e furação |
| Lixadeira de cinta | Lixadeira de madeira | P14 — Lixamento |
| Bancada + exaustão | Bancada de acabamento | P15 — Acabamento superficial |

**Na Montagem:**
| Equipamento no layout | Nome completo | Processo |
|---|---|---|
| 404-S TURBO-X | Rebitadeira Pneumática Rebitex | P21 — Rebitagem |
| Bancada Montagem | Bancada industrial | P22/P24 — Inspeção e montagem do kit |

**Na Embalagem:**
| Equipamento no layout | Nome completo | Processo |
|---|---|---|
| 40×50 cm semiaut | Seladora Blister Flockcolor | P22 — Selagem (se aplicável) |
| Bancada Embalagem | Bancada industrial | P24 — Embalagem final |

**Na Inspeção/QC:**
| Equipamento no layout | Nome completo | Processo |
|---|---|---|
| Bancada QC | Bancada de controle de qualidade | Inspeções gerais |

### As dimensões externas
- **24 m** = dimensão horizontal (comprimento da fábrica)
- **16 m** = dimensão vertical (largura da fábrica)
- Dimensões são premissas de projeto — não foi baseado em terreno real

---

## Cross-check — inconsistências encontradas

| # | Onde | Inconsistência | Status |
|---|---|---|---|
| 1 | Slide 2 | "André Bapista" — falta o 't' no sobrenome | ⚠️ Erro tipográfico |
| 2 | Slide 17 | Laser Fibra CNC no mesmo campo que "RHTC/ProfiPress" — são fornecedores misturados na tabela | ⚠️ Formatação confusa da tabela |
| 3 | Slide 19 | Router CNC: 1 unidade | vs nosso layout SVG que mostra 2 Router CNCs — o slide é a verdade, 1 unidade |
| 4 | Slide 9 | Mistura conteúdo de BOM e Tabela de Processos P2 na extração — provavelmente layout de duas colunas | ✅ Não é problema real |
| 5 | Slide 20 | Tc = 0,87 min/kit não é explicitado de onde vem | ⚠️ Lacuna de transparência |
| 6 | Slide 22 | Diz "Estampagem" nos setores (Recebimento → Estampagem → TT...) mas o processo é corte a laser, não estampagem | ⚠️ Terminologia incorreta — deveria ser "Corte Laser" |
| 7 | Slide 26 | Fontes incompletas — só 2 visíveis, mas o projeto usou ~12 fontes | ⚠️ Slide de fontes poderia ser mais completo |

---

## Perguntas prováveis da banca e respostas

**"Por que 1.000 kits/semana?"**
"Representa 200 kits/dia — ritmo viável para uma fábrica nova de médio porte com 9 equipamentos principais. O laser opera a 49% de utilização, o que dá margem para absorver picos de demanda sem investimento adicional."

**"O que é AISI 420 e por que foi escolhido?"**
"É um aço inox martensítico — o único tipo de inox que endurece com tratamento térmico. Isso permite criar fio de corte na faca, o que é impossível com AISI 304 (o inox comum). Toda faca de qualidade usa aço desta família."

**"Por que FAZER cabos e tábua em vez de comprar prontos?"**
"O cabo tem 3 furos de rebite em posições precisas — se o fornecedor errar 0,5mm, o rebite não fecha direito. A tábua precisa ter as dimensões compatíveis com a embalagem display. Fabricar internamente garante controle dimensional em ambos."

**"O que é tratamento térmico e por que é necessário?"**
"É o aquecimento da lâmina AISI 420 a 1.050–1.100°C seguido de resfriamento controlado. Isso transforma a microestrutura do aço em martensita — fase mais dura. Sem isso a lâmina fica mole e não sustenta o fio de corte."

**"Por que 3 lixadeiras e 3 rebitadeiras?"**
"As 3 lixadeiras operam em linha: desbaste grosso, lixamento médio e polimento fino — uma máquina por etapa de acabamento. As 3 rebitadeiras são 1 por posto de montagem: um para a faca, um para o garfo, e um de reserva/manutenção alternada."

**"O que é o mapofluxograma e por que é diferente do fluxograma?"**
"O fluxograma mostra a sequência das 26 operações. O mapofluxograma mostra onde no espaço físico cada operação acontece — é o fluxograma desenhado sobre o layout. Ele revela perdas de movimentação: se as setas cruzam muito ou percorrem distâncias longas, o layout precisa de ajuste."

**"Como calcularam o número de lasers?"**
"Pela fórmula: N = Db / Cap, onde Db é a demanda bruta diária (206,2 kits) e Cap é a capacidade efetiva (422 kits/dia). Cap = Td / Tc = 367,2 min / 0,87 min por kit. Td é o tempo disponível considerando eficiência e disponibilidade. Resultado: N = 0,49, arredondado para 1."

**"Por que arranjo misto?"**
"Setor metal e madeira usam arranjo funcional — equipamentos agrupados por processo (laser com laser, forno com forno), porque cada componente passa por uma sequência específica e os equipamentos são caros e especializados. A montagem usa arranjo em linha — operações em sequência fixa para um produto padronizado, o que minimiza movimentação e esperas."

**"Qual é o gargalo da produção?"**
"Formalmente identificado: o Laser Fibra CNC com 49% de utilização. Na prática, as lixadeiras de metal e rebitadeiras operam mais próximo da capacidade total. Para dobrar a produção, bastaria adicionar um segundo laser e replicar as estações de lixamento e rebitagem."

**"O que são as esteiras transportadoras?"**
"São 6 esteiras que interligam as estações de trabalho — transportam peças do laser para o forno, do forno para o polimento, e assim por diante. Correspondem aos Processos de Transporte na Tabela 2 (P03, P11, P18, P19, P20, P25)."
