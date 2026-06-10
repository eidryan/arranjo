# Guia de Defesa — Projeto de Fábrica
## Kit para Churrasco Tramontina 22399036 · Grupo A

---

## Como ler este documento

Cada seção cobre um dos 14 itens obrigatórios da atividade. Para cada um:
- **O que foi feito** — o conteúdo e a lógica
- **Por que fizemos assim** — raciocínio técnico
- **Lacunas e como responder** — o que é fraco e o argumento de defesa

---

## 1. Integrantes

**Grupo A:** Adrian Vilela, André Baptista, Bernardo Gomes, Clara Barboza, João Pedro Deccax, Leonardo Nespoli, Lucas de Mello

**Orientação:** Professora Suzana Dantas — Disciplina Arranjo Físico Industrial 2026.1

---

## 2. Objetivos do projeto

Cinco objetivos formais:

1. Desenvolver proposta de fábrica para o kit com meta de 1.000 kits bons/semana
2. Dimensionar processos, equipamentos e layout em fluxo contínuo
3. Calcular quantidades de equipamentos com tempos-padrão, eficiência, confiabilidade e rendimento explicitados
4. Selecionar segmentos de mercado e justificar a meta
5. Gerar documentação técnica auditável com fontes identificadas

**Por que esses objetivos:** Cobrem exatamente os 14 itens obrigatórios do enunciado. O objetivo 5 é o diferencial — toda conta é gerada por código com fonte declarada, não foi digitada manualmente.

---

## 3. Produto

**Kit SKU 22399036** — Kit para Churrasco Tramontina com Lâminas em Aço Inox e Cabos em Madeira Natural 3 Peças

### Composição
| Componente | SKU filho | Material principal |
|---|---|---|
| Faca Chef 8" | 22315008 | Lâmina AISI 420, cabo madeira natural |
| Garfo Trinchante | 22330000 | Lâmina AISI 420, cabo madeira natural |
| Tábua Retangular | 13102152 | Madeira Maçaranduba com acabamento natural |

### Dados técnicos (fonte: página oficial Tramontina)
- Embalagem: 38,9 × 4,0 × 21,6 cm · 1,23 kg
- Certificação FSC C125626 (madeira de manejo sustentável)
- Garantia: 5 anos

### Material das lâminas — AISI 420
O aço escolhido é o **AISI 420 martensitico** (Aperam 420D). A escolha importa porque:
- É endurecível por tratamento térmico — justifica o processo P6 (forno)
- Dureza final controlada para fio de corte — justifica o processo P9 (afiação)
- Alternativa ao AISI 304 (que não endurece) — usado em facas de qualidade

**Lacuna:** As dimensões exatas da lâmina (espessura 2 mm, comprimento 317 mm) são estimativas a partir do desenho técnico oficial. Não foram confirmadas por desmontagem do produto.

**Como responder:** "Usamos o desenho técnico oficial da Tramontina disponível no site como base. A espessura de 2 mm é compatível com a especificação do laser fibra (corte até 2 mm em inox) e com padrões industriais de facas desse segmento."

---

## 4. Estrutura pai-filho (BOM — Tabela 1)

### Decisão FAZER vs COMPRAR

⚠️ **INCONSISTÊNCIA PENDENTE NO SLIDE:** A Tabela 1 do PPTX atual ainda mostra cabo de madeira e tábua como COMPRAR (versão do grupo). A decisão técnica é FAZER. Isso precisa ser corrigido antes da apresentação.

**Decisão técnica adotada neste projeto:**

| Componente | Qtd | Un | Decisão | Justificativa |
|---|---|---|---|---|
| Faca chef (lâmina + cabo + rebites) | 1 | un | **FAZER** | Controle de qualidade do fio e acabamento |
| Garfo trinchante (lâmina + cabo + rebites) | 1 | un | **FAZER** | Controle de qualidade do acabamento |
| Tábua retangular maçaranduba | 1 | un | **FAZER** | Peça principal do kit, diferencial de qualidade |
| Cartela/cinta impressa | 1 | un | COMPRAR | Item gráfico padronizado |
| Blister/suporte plástico | 1 | un | COMPRAR | Fornecedor especializado em injeção |
| Etiqueta/código de barras | 1 | conj | COMPRAR | Requisito de rastreabilidade |
| Caixa de transporte | 1 | un | COMPRAR | Requisito do enunciado |

**Por que FAZER tábua e cabos:** Se compramos prontos, eliminamos 7 processos de madeira (P11–P17), o Router CNC, a esquadrejadeira e a lixadeira. O projeto perde substância técnica e o arranjo físico fica trivial. Para um projeto de fábrica acadêmico, é mais correto modelar a produção completa.

**Como responder se questionarem:** "Tramontina é fabricante verticalizado — a madeira é processada internamente para garantir encaixe preciso do cabo no anel de rebitagem e acabamento uniforme. Terceirizar o cabo implicaria perder controle dimensional nos 3 furos de rebite."

---

## 5. Segmentos de mercado

Quatro segmentos:
1. **Varejo doméstico** — supermercados e lojas de utilidades, demanda regular
2. **Kits presente sazonal** — Dia dos Pais, Natal, Namorados; pico de demanda
3. **E-commerce e marketplaces** — Mercado Livre, Amazon, site Tramontina; embalagem compacta favorece frete
4. **Brindes corporativos / ESG** — FSC C125626 como diferencial sustentável

**Por que 4 segmentos:** O enunciado pede segmentos e justificativa. O quarto segmento (brindes/ESG) diferencia o trabalho pois usa a certificação FSC como argumento técnico.

---

## 6. Meta semanal de produção

### Números finais
| Parâmetro | Valor | Fonte |
|---|---|---|
| Meta de kits bons | **1.000 kits/semana** | Premissa do projeto |
| Rendimento final | 95% | Premissa de engenharia |
| Demanda bruta necessária | **1.053 kits/semana** | Calculado: 1000 / 0,95 |
| Dias úteis | 5 dias/semana | Premissa |
| Turnos | 1 turno/dia | Premissa |
| Horas úteis/turno | 7 h (de 8 programadas) | Premissa (1h pausas/manutenção) |
| Horas úteis/semana | **35 h** | Calculado |
| Ritmo médio necessário | **~30 kits/h** | Calculado |

### Fórmula da demanda bruta
```
demanda_bruta = ARREDONDAR.PARA.CIMA(meta_boa / rendimento_final)
demanda_bruta = ARREDONDAR.PARA.CIMA(1000 / 0,95) = 1.053 kits/semana
```

⚠️ **Lacuna crítica:** A justificativa para 1.000 kits/semana não está formalmente documentada. É uma premissa do projeto.

**Como responder:** "A meta de 1.000 kits/semana foi definida como ponto de partida viável para uma fábrica de médio porte. Representa ~50.000 kits/ano, compatível com a presença da Tramontina em redes nacionais de varejo. O modelo é facilmente escalável — para 2.000 kits, dobramos as quantidades de equipamentos mantendo o mesmo layout com a folga de 32% existente."

---

## 7. Tabela 1 — Componentes (ver seção 4 acima)

---

## 8. Tabela 2 — Processos (26 processos)

### Distribuição por tipo
| Tipo | Qtd | Processos |
|---|---|---|
| Operação | 12 | P4, P6, P8, P9, P12, P13, P14, P15, P19, P21, P22, P24 |
| Inspeção | 5 | P1, P5, P17, P20, P23 |
| Transporte | 4 | P3, P11, P18, P26 |
| Armazenagem | 3 | P2, P10, P25 |
| Espera | 2 | P7, P16 |

### Lógica do fluxo
O processo segue **duas trilhas paralelas** que convergem na montagem:
- **Trilha metal (P1–P10):** recebimento → corte laser → inspeção → tratamento térmico → resfriamento → polimento → afiação → estoque intermediário
- **Trilha madeira (P11–P17):** transporte da madeira → corte → fresagem CNC → lixamento → acabamento → cura → inspeção
- **Montagem e embalagem (P18–P26):** convergência das trilhas → rebitagem → inspeção → kit → blister → inspeção → caixa → estoque PA → expedição

### Por que 26 processos
Cada processo tem identidade única: tipo diferente OU recurso diferente OU produto diferente entrando/saindo. P7 (resfriamento) e P16 (cura) são esperas porque o produto está parado aguardando transformação física sem ação humana direta.

⚠️ **Lacuna:** Os tempos-padrão são todos **estimativas de engenharia**, não medições reais (cronoanálise). Isso é normal para projeto básico de fábrica mas é vulnerabilidade técnica.

**Como responder:** "Os tempos-padrão foram estimados com base nas capacidades declaradas pelos fabricantes e em benchmarks de operações similares. A conclusão 1 do projeto já aponta explicitamente que o próximo passo seria um estudo de tempos real (cronoanálise) para substituir as estimativas."

---

## 9. Fluxograma do processo

O fluxograma usa a **notação ASME** com os 5 símbolos padrão:
- ⬤ Operação (círculo)
- ▷ Transporte (seta/triângulo)
- □ Inspeção (quadrado)
- ▽ Armazenagem (triângulo invertido)
- D Espera (D maiúsculo)

Duas trilhas paralelas (metal e madeira) convergem na montagem. Os números dos processos correspondem exatamente à Tabela 2 — isso é fundamental.

**Por que é importante a correspondência:** O enunciado pede fluxograma "utilizando os ícones representativos e a numeração correspondente à Tabela 2". Se o número no fluxograma não bater com a tabela, é erro.

---

## 10. Tabela 3 — Equipamentos

### Parque de máquinas (11 equipamentos)
| # | Equipamento | Fornecedor/Modelo | Taxa efetiva | Qtd | Utilização |
|---|---|---|---|---|---|
| 1 | Corte laser fibra CNC | Madetech / CNC Fiber Pro 1530 | 61,3 kits/h | 1 | 49% |
| 2 | Forno de tratamento térmico | Cecomatec / 703.099 com carro | 115,0 kits/h | 1 | 26% |
| 3 | Lixadeira/politriz de metal | A cotar | 30,7 kits/h | 1 | **98%** |
| 4 | Afiador de facas | Maksiwa / AF.650 | 91,9 kits/h | 1 | 33% |
| 5 | Esquadrejadeira para madeira | Maksiwa / BMS.1900.I | 61,3 kits/h | 1 | 49% |
| 6 | Router CNC para madeira | Maksiwa Store / RTC.1313 | 23,0 kits/h | 2 | 65% |
| 7 | Lixadeira de madeira | A cotar | 30,7 kits/h | 1 | **98%** |
| 8 | Bancada de acabamento madeira | Montagem interna | 46,0 kits/h | 1 | 65% |
| 9 | Rebitadeira pneumática | Rebitex / 404-S TURBO-X | 30,7 kits/h | 1 | **98%** |
| 10 | Bancada de montagem/inspeção | Montagem interna | 46,0 kits/h | 1 | 65% |
| 11 | Seladora blister carrossel | Flockcolor / 40×50 cm | 183,9 kits/h | 1 | 16% |

### Fórmula para quantidade de equipamentos
```
Q = TETO( demanda_bruta / (taxa_nominal × h_úteis/semana × eficiência × confiabilidade × rendimento_processo) )
```

Onde:
- Eficiência geral: 85%
- Confiabilidade: 92%
- Rendimento do processo: 98%

⚠️ **Lacuna:** Politriz de metal, lixadeira de madeira e rebitadeira estão a **98% de utilização** — tecnicamente são os gargalos reais, não o Router CNC. A escolha do Router CNC como equipamento da memória de cálculo foi estratégica (mais capital intensivo e interessante tecnicamente).

**Como responder se perguntarem sobre os 98%:** "A politriz e a lixadeira industrial têm capacidade facilmente ampliável — adicionar um segundo turno ou um segundo equipamento de baixo custo resolve. O Router CNC foi selecionado para a memória de cálculo por ser o equipamento de maior valor de capital e mais crítico para a qualidade dimensional."

---

## 11. Memória de cálculo — Equipamento selecionado: Laser Fibra CNC

### Por que o Laser Fibra e não a Prensa Excêntrica (versão do grupo)

O grupo originalmente selecionou a Prensa Excêntrica 60 tf. Mudamos para o Laser Fibra CNC pelos seguintes motivos técnicos:

| Critério | Prensa Excêntrica | Laser Fibra CNC |
|---|---|---|
| Processo correto para AISI 420 | Estampagem — forma, não corta perfil | **Corte — perfil preciso da lâmina** |
| Qualidade do corte | Rebarbas, exige desbaste posterior | **Borda limpa, tolerância ±0,05 mm** |
| Fornecedor cotado | Harlo do Brasil (SP) | **Madetech (SP) — com specs reais** |
| Resultado do cálculo | 1 unidade, ~2% utilização | **1 unidade, 49% utilização** |
| Coerência com P4 da Tabela 2 | "Corte de blanks" — laser é correto | ✅ |

### Cálculo
```
Tempo-padrão: 45 s/kit (cortar blanks de faca e garfo em chapa aninhada)
Taxa nominal: 3600 / 45 = 80 kits/h

Taxa efetiva = 80 × 0,85 × 0,92 × 0,98 = 61,3 kits/h
Capacidade/semana = 61,3 × 35 = 2.145 kits/semana

N = TETO(1053 / 2145) = TETO(0,49) = 1 unidade
Utilização = 1053 / 2145 = 49%
```

⚠️ **Lacuna:** O tempo de 45 s/kit é estimativa. Com laser fibra a 20.000 mm/min e blank de ~200 mm de comprimento, o corte do perfil de uma faca leva ~30–60 s dependendo da complexidade. 45 s é defensável.

---

## 12. Layout esquemático

### Dimensões e ocupação
- Área total: **384 m² (24 × 16 m)** — premissa do projeto
- Área requerida calculada: 260,4 m²
- Ocupação: 67,8%
- Folga: 32,2% (~123,6 m²) — permite expansão futura

### Setores
| Setor | Área | Conteúdo |
|---|---|---|
| Recebimento/Expedição | 24,0 m² | Doca, conferência, separação |
| Setor Metal | ~60 m² | Laser, forno TT, politriz, afiador |
| Setor Madeira | ~50 m² | Esquadrejadeira, 2× Router CNC, lixadeira, bancada |
| Montagem/Embalagem | ~30 m² | Rebitadeira, bancadas, seladora |
| Estoques (MP, intermediário, PA) | 54,0 m² | Porta-paletes, FIFO |
| Inspeção e controle | 12,0 m² | Bancada, instrumentos |
| Apoio (manutenção, EPI, compressor) | 20,0 m² | Serviços |

### Tipo de arranjo
**Arranjo misto:** funcional para metal e madeira (equipamentos agrupados por processo), célula/linha para montagem e embalagem (fluxo unitário contínuo). Justificativa: volumes médios com variedade de componentes favorecem funcional nos setores; o kit é padronizado logo depois, favorecendo linha na montagem.

⚠️ **Lacuna:** As dimensões 24×16 m foram escolhidas como premissa, não derivadas de um estudo de terreno real. A área de 384 m² acomoda todos os equipamentos com margem de 32%.

---

## 13. Mapofluxograma

O mapofluxograma **sobrepõe o fluxograma ao layout** — mostra por onde o material caminha fisicamente.

Aspectos técnicos a dominar:
- Cada processo tem uma posição aproximada no mapa correspondente ao setor do layout
- As setas mostram a sequência física do fluxo
- Cruzamentos de seta indicam onde há potencial de conflito de movimentação — área para melhoria

**Como ler:** "Começando no Recebimento (P1–P2), a matéria-prima metálica vai para o Setor Metal (P3–P10) e a madeira para o Setor Madeira (P11–P17). Ambos convergem para a Montagem (P18–P26) e saem pela Expedição."

---

## 14. Conclusões

### Resumo do projeto
Fábrica de 384 m² capaz de produzir 1.000 kits bons/semana em 1 turno de 7 h úteis. Demanda bruta de 1.053 kits/semana com rendimento final de 95%.

### Gargalo identificado
**Router CNC Maksiwa RTC.1313** — 2 unidades a 65% de utilização. É a etapa mais lenta do setor madeira (tempo-padrão de 120 s/kit para fresar sulco da tábua e usinar/furar cabos). Para dobrar a capacidade: terceiro turno ou terceira unidade do router.

### 6 oportunidades de melhoria (obrigatório no enunciado)
1. Estudo de tempos real (cronoanálise) para substituir estimativas
2. Cotar equipamentos em pelo menos 2 fornecedores alternativos
3. Piloto de 1 semana para validar rendimento de 95% e premissas de eficiência
4. Controle Estatístico de Processo (CEP) no TT e afiação
5. Modelar cenários de demanda ±30%
6. Análise de custo de implantação e payback

---

## Resumo das inconsistências a resolver antes da apresentação

| # | Problema | Impacto | Ação necessária |
|---|---|---|---|
| 1 | Tabela 1 no slide: cabo e tábua aparecem como COMPRAR | Alto — contradiz todos os processos de madeira | Corrigir no PPTX para FAZER |
| 2 | Meta de 1.000 kits sem justificativa formal | Médio — pergunta provável da professora | Preparar argumento verbal (ver seção 6) |
| 3 | Tempos-padrão são estimativas | Médio — vulnerabilidade técnica | Já coberto nas conclusões — citar |
| 4 | Politriz/lixadeira/rebitadeira a 98% | Médio — parecem ser os gargalos reais | Explicar que são fáceis de ampliar |
| 5 | Número de rebites: 4 (nosso) vs 3 por cabo (produto real) | Baixo | Verificar no produto físico se possível |

---

## Perguntas prováveis da banca e respostas sugeridas

**"Por que 1.000 kits/semana?"**
"Representa ~50.000 kits/ano. Para uma fábrica nova do porte proposto (384 m²), é uma meta conservadora e alcançável. O modelo foi construído para ser facilmente escalável."

**"De onde vieram os tempos-padrão?"**
"São estimativas baseadas nas capacidades declaradas pelos fabricantes dos equipamentos e em benchmarks de operações similares. A limitação está documentada nas conclusões como primeiro ponto de melhoria — cronoanálise real seria o próximo passo."

**"Por que laser e não prensa para cortar o aço?"**
"O AISI 420 em espessura de 2 mm é cortado com laser fibra na indústria de cutelaria. A prensa excêntrica faz estampagem (deformação), não corte de perfil — o que exigiria um molde/punção específico para cada geometria de lâmina. Laser corta qualquer perfil programado com tolerância de ±0,05 mm."

**"O que é o mapofluxograma e por que é diferente do fluxograma?"**
"O fluxograma mostra a *sequência* das operações. O mapofluxograma mostra *onde no espaço físico* cada operação acontece. Ele combina os dois: o fluxo de processo sobreposto ao layout. É a ferramenta que revela perdas de movimentação — se as setas cruzam muito ou percorrem longas distâncias, o layout precisa de ajuste."

**"Por que arranjo misto?"**
"Os setores de metal e madeira têm vários equipamentos especializados processando os mesmos componentes — isso favorece o arranjo funcional (por processo). A montagem e embalagem são operações em sequência fixa com produto padronizado — isso favorece a linha ou célula. O misto captura os benefícios dos dois."

**"A área de 384 m² é suficiente?"**
"Sim. A área requerida calculada é 260,4 m², com 67,8% de ocupação. Os 32,2% restantes (~123 m²) cobrem corredores de segurança e permitem expansão futura sem reforma estrutural."

---

## Fontes principais

| Fonte | Uso |
|---|---|
| Página oficial Tramontina (22399036) | Produto, composição, dimensões, certificação FSC |
| Aperam 420D (aperam.com) | Material AISI 420 para lâminas |
| Rolmetais — AISI 420 | Densidade e tratamento térmico |
| Madetech — CNC Fiber Pro 1530 | Laser fibra: mesa, velocidade, espessura |
| Cecomatec — Forno 703.099 | TT: câmara, temperatura |
| Maksiwa Store — RTC.1313 | Router CNC: área útil, velocidade, spindle |
| Maksiwa — BMS.1900.I | Esquadrejadeira |
| Maksiwa — AF.650 | Afiador de facas |
| Rebitex — 404-S TURBO-X | Rebitadeira: ciclos/min, força |
| Flockcolor — Seladora Blister | Produtividade: 4 prensadas/min |
| Slides e guias da disciplina | Método: produto→BOM→Tabela 2→fluxograma→layout→mapo |
