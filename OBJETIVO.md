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
