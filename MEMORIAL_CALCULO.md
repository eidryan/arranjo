# Memorial de Cálculo — Projeto de Fábrica
## Kit Churrasco Tramontina 22399036

---

## Bloco 1 — Demanda bruta semanal

### O problema
A meta é **1.000 kits bons por semana**. Mas durante a produção, nem tudo que entra sai como produto bom — há rejeitos, retrabalhos, perdas. Então precisamos produzir **mais do que 1.000** para garantir que 1.000 saiam aprovados.

### Fórmula
```
demanda_bruta = TETO( meta_boa / rendimento_final )
```

### Entradas
| Variável | Valor | Fonte |
|---|---|---|
| Meta de kits bons/semana | 1.000 | Premissa do projeto |
| Rendimento final | 95% = 0,95 | Premissa de engenharia |

### Cálculo
```
demanda_bruta = TETO( 1.000 / 0,95 )
demanda_bruta = TETO( 1.052,63 )
demanda_bruta = 1.053 kits/semana
```

**O que significa:** De cada 1.053 kits que entram no processo, 5% (≈53) serão descartados ou retrabalhados. Os 1.000 restantes são os "kits bons" que chegam ao cliente.

---

## Bloco 2 — Horas úteis e ritmo médio

### Regime de trabalho
| Parâmetro | Valor |
|---|---|
| Dias úteis/semana | 5 dias |
| Turnos/dia | 1 turno |
| Horas programadas/turno | 8 h |
| Horas úteis/turno | **7 h** |
| Horas úteis/semana | **35 h** |

**Por que 7h e não 8h:** 1 hora por turno é descontada para pausas obrigatórias, pequenas manutenções e setup. É premissa padrão de engenharia de produção.

### Ritmo médio necessário
```
ritmo = demanda_bruta / horas_úteis_semana
ritmo = 1.053 / 35
ritmo = 30,09 kits/hora
```

**O que significa:** Em média, a fábrica precisa produzir um kit a cada ~2 minutos para fechar a meta semanal.

---

## Bloco 3 — A fórmula geral de dimensionamento de equipamentos

Esta é a fórmula central de todo o projeto. Ela aparece em cada linha da Tabela 3.

### Fórmula
```
Q = TETO( demanda_bruta / (taxa_nominal × h_úteis × η × conf × rend_processo) )
```

### Cada fator explicado

| Fator | Símbolo | Valor usado | Significado |
|---|---|---|---|
| Demanda bruta | — | 1.053 kits/sem | Produção total necessária |
| Taxa nominal | — | varia por equip. | Capacidade declarada pelo fabricante em condições ideais |
| Horas úteis/semana | h_úteis | 35 h | Tempo real disponível |
| Eficiência geral | η | 85% | Redução por micro-paradas, esperas, variações de ritmo |
| Confiabilidade | conf | 92% | Fração do tempo que o equipamento está disponível (sem quebras) |
| Rendimento do processo | rend | 98% | Fração de peças boas que saem deste processo específico |

### Taxa efetiva

Antes de calcular Q, calculamos a taxa efetiva — o que o equipamento realmente entrega considerando as perdas:

```
taxa_efetiva = taxa_nominal × η × conf × rend_processo
taxa_efetiva = taxa_nominal × 0,85 × 0,92 × 0,98
taxa_efetiva = taxa_nominal × 0,7663
```

**Portanto:** qualquer equipamento entrega ~76,6% da sua capacidade nominal declarada.

### Capacidade semanal por unidade
```
capacidade_semana = taxa_efetiva × horas_úteis_semana
capacidade_semana = taxa_efetiva × 35
```

### Quantidade necessária
```
Q = TETO( 1.053 / capacidade_semana )
```

A função TETO arredonda para cima — não existe meio equipamento.

### Utilização
```
utilização = 1.053 / (Q × capacidade_semana)
```

Utilização abaixo de 100% indica folga de capacidade. Acima de ~85% é preocupante.

---

## Bloco 4 — Como calcular a taxa nominal a partir do tempo-padrão

Para a maioria dos equipamentos, a capacidade do fabricante é dada em unidades/hora ou em tempo por peça.

### Quando o fabricante informa tempo por peça
```
taxa_nominal = 3.600 / tempo_padrão_segundos
```

Exemplo — Laser Fibra CNC (tempo estimado: 45 s/kit):
```
taxa_nominal = 3.600 / 45 = 80 kits/hora
```

### Quando o fabricante informa ciclos/min (ex: rebitadeira)
A Rebitex 404-S informa 60 ciclos/min, mas o **tempo-padrão real** inclui o posicionamento dos 4 rebites e o manuseio das peças — estimado em 90 s/kit:
```
taxa_nominal = 3.600 / 90 = 40 kits/hora
```
A capacidade bruta da rebitadeira (60 ciclos/min = 3.600 rebites/hora) é muito maior, mas cada kit usa 4 rebites e exige manuseio manual. O gargalo é o operador, não a máquina.

---

## Bloco 5 — Equipamento selecionado: Laser Fibra CNC Madetech

Este é o equipamento detalhado no memorial de cálculo da apresentação.

### Por que o Laser Fibra
- É o equipamento que **corta os blanks** da faca e do garfo na chapa de aço inox (Processo P4)
- Para AISI 420 em 2 mm de espessura, corte a laser é o método industrial padrão
- Fornecedor real cotado: **Madetech — CNC Fiber Pro 1530** (São Paulo)
- Capacidade declarada: laser 1.500 W, mesa 3.000 × 1.500 mm, velocidade 20.000 mm/min, corte até 2 mm em inox

### Memória completa

**Entradas:**
| Variável | Valor | Fonte |
|---|---|---|
| Tempo-padrão | 45 s/kit | Estimativa: cortar blanks de faca e garfo em chapa aninhada |
| Taxa nominal | 80 kits/h | 3.600 / 45 |
| Eficiência | 85% | Premissa de engenharia |
| Confiabilidade | 92% | Premissa de engenharia |
| Rendimento do processo | 98% | Premissa de engenharia |
| Horas úteis/semana | 35 h | 5 dias × 1 turno × 7 h |
| Demanda bruta | 1.053 kits/sem | Bloco 1 |

**Cálculo passo a passo:**
```
taxa_efetiva = 80 × 0,85 × 0,92 × 0,98
taxa_efetiva = 80 × 0,7663
taxa_efetiva = 61,3 kits/hora

capacidade_semana = 61,3 × 35
capacidade_semana = 2.145,8 kits/semana

Q = TETO( 1.053 / 2.145,8 )
Q = TETO( 0,49 )
Q = 1 unidade

utilização = 1.053 / (1 × 2.145,8)
utilização = 49%
```

**Resultado:** 1 Laser Fibra CNC Madetech CNC Fiber Pro 1530 opera a 49% de utilização — tem folga de capacidade para absorver variações de demanda.

---

## Bloco 6 — Cálculo completo de todos os equipamentos

| # | Equipamento | Tempo-padrão (s/kit) | Taxa nominal (kits/h) | Taxa efetiva (kits/h) | Cap./sem. (kits) | Q | Utilização |
|---|---|---|---|---|---|---|---|
| 1 | Laser fibra CNC | 45 s | 80,0 | 61,3 | 2.146 | **1** | 49% |
| 2 | Forno TT (batelada) | — | 150,0¹ | 115,0 | 4.023 | **1** | 26% |
| 3 | Politriz/lixadeira metal | 90 s | 40,0 | 30,7 | 1.073 | **1** | **98%** |
| 4 | Afiador de facas | 30 s | 120,0 | 92,0 | 3.219 | **1** | 33% |
| 5 | Esquadrejadeira madeira | 45 s | 80,0 | 61,3 | 2.146 | **1** | 49% |
| 6 | Router CNC madeira | 120 s | 30,0 | 23,0 | 805 | **2** | 65% |
| 7 | Lixadeira de madeira | 90 s | 40,0 | 30,7 | 1.073 | **1** | **98%** |
| 8 | Bancada acabamento | 60 s | 60,0 | 46,0 | 1.609 | **1** | 65% |
| 9 | Rebitadeira pneumática | 90 s | 40,0 | 30,7 | 1.073 | **1** | **98%** |
| 10 | Bancada montagem/inspeção | 60 s | 60,0 | 46,0 | 1.609 | **1** | 65% |
| 11 | Seladora blister | 15 s² | 240,0 | 183,9 | 6.437 | **1** | 16% |

¹ Forno TT: estimativa por batelada — 600 peças metálicas em 2 horas = 300 peças/h = 150 kits/h (2 peças metálicas/kit)

² Seladora: 4 prensadas/min (dado do fabricante Flockcolor) = 240 prensadas/h. Assumindo 1 kit por prensada → 15 s/kit

---

## Bloco 7 — Por que o Router CNC precisa de 2 unidades

É o único equipamento que precisou de mais de 1 unidade. Vejamos:

```
taxa_efetiva_router = 30 × 0,85 × 0,92 × 0,98 = 23,0 kits/h
capacidade_1_router = 23,0 × 35 = 804,7 kits/semana

Q = TETO( 1.053 / 804,7 ) = TETO( 1,31 ) = 2 unidades
```

Com 1 unidade a capacidade seria de 804,7 kits/semana — insuficiente para 1.053. Com 2 unidades:

```
utilização_2_routers = 1.053 / (2 × 804,7) = 1.053 / 1.609,4 = 65%
```

**O tempo-padrão de 120 s/kit** (fresar sulco da tábua + usinar e furar os 4 cabos) é o mais longo do projeto. Por isso o router é identificado como o **gargalo** do projeto — o equipamento que limita a capacidade da fábrica.

### Para dobrar a capacidade futura
Sem alterar o prédio: adicionar um 3º Router CNC ou um 2º turno.

---

## Bloco 8 — Cálculo da área do layout

### Área dos equipamentos
Cada equipamento ocupa: footprint (comprimento × largura) × fator de área de serviço

O fator de serviço inclui espaço para operação, manutenção e circulação ao redor do equipamento. Valor padrão: 2,0 (exceto Router CNC: 2,2 e Afiador: 5,0 por ser pequeno mas precisar de espaço de operação)

```
área_equipamento = footprint_m² × fator_serviço × quantidade
```

Exemplo — Router CNC:
```
footprint = 1,7 × 2,0 = 3,4 m²
área_planejada = 3,4 × 2,2 × 2 unidades = 14,96 m²
```

**Total área equipamentos: 90,3 m²**

### Áreas fixas
| Área | m² | Base |
|---|---|---|
| Estoque MP e embalagens | 30,0 | 5 dias de material, porta-paletes e corredores |
| Estoque intermediário | 12,0 | Pulmão entre setores |
| Estoque produto acabado | 12,0 | 3 dias × volume da embalagem |
| Inspeção e controle | 12,0 | Bancada, instrumentos, retenção |
| Recebimento e expedição | 24,0 | Doca, conferência |
| Apoio (manutenção, EPI, compressor) | 20,0 | Operação mínima |
| **Total fixo** | **110,0 m²** | |

### Circulação
```
área_circulação = 30% × (área_equipamentos + área_fixa)
área_circulação = 0,30 × (90,3 + 110,0)
área_circulação = 0,30 × 200,3
área_circulação = 60,1 m²
```

### Área total requerida
```
área_requerida = 90,3 + 110,0 + 60,1 = 260,4 m²
```

### Área proposta
```
área_proposta = 24 m × 16 m = 384 m²
folga = 384 - 260,4 = 123,6 m²
ocupação = 260,4 / 384 = 67,8%
```

A folga de **32,2%** permite expansão futura sem reforma estrutural — dobrar o Router CNC (3ª unidade) e adicionar equipamentos menores caberia dentro da área existente.

---

## Bloco 9 — O que cada premissa significa e como defender

### Eficiência de 85%
Significa que, do tempo disponível, 85% é tempo produtivo. Os 15% restantes são micro-paradas, variações de ritmo, setup de pequenos ajustes.
**Referência:** Valor típico citado na literatura de Engenharia de Produção (Slack et al.) para operações industriais de médio porte.

### Confiabilidade de 92%
Significa que o equipamento fica disponível 92% do tempo programado — 8% está em manutenção preventiva ou corretiva.
**Referência:** Premissa conservadora. Equipamentos novos tendem a ter confiabilidade maior. É favorável ao projeto (dimensiona por excesso de segurança).

### Rendimento de processo de 98%
Significa que 98% das peças que entram num processo saem aprovadas. 2% são descartadas ou retrabalhadas naquele processo específico.
**Nota:** O rendimento final de 95% é o produto de múltiplos processos, cada um com 98%. Com 26 processos: 0,98²⁶ ≈ 0,59 seria muito baixo — na prática, só os processos críticos (TT, afiação, polimento) têm rejeito real. Os demais são 100%. O valor de 95% no final é uma premissa conservadora agregada.

### Como responder se questionarem as premissas
"As premissas de eficiência, confiabilidade e rendimento são valores típicos de referência para projetos básicos de fábrica. A conclusão 1 do projeto aponta explicitamente que o próximo passo é um estudo de tempos real para substituir as estimativas por valores medidos."

---

## Resumo rápido para a apresentação oral

1. **Meta:** 1.000 kits bons/semana
2. **Bruto necessário:** 1.053 (por causa do rendimento de 95%)
3. **Regime:** 5 dias × 1 turno × 7h úteis = 35h/semana → ritmo de ~30 kits/hora
4. **Fórmula:** Q = TETO( 1053 / (taxa × 35 × 0,85 × 0,92 × 0,98) )
5. **Equipamento selecionado:** Laser Fibra CNC — 1 unidade, 49% de utilização
6. **Único com 2 unidades:** Router CNC (gargalo, 120 s/kit)
7. **Gargalos reais:** politriz de metal, lixadeira de madeira e rebitadeira a 98%
8. **Layout:** 384 m² para uma necessidade de 260 m² — 67,8% de ocupação
