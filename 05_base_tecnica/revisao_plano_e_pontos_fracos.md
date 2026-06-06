# Revisão do Plano e Pontos Fracos

## Diretriz Nova

Todas as contas do projeto devem ser executadas por código e documentadas de forma transparente. O Excel pode mostrar os resultados, mas a origem das contas deve ficar em `scripts/generate_outputs.py` e na base `data/projeto.json`.

Para cada cálculo, o projeto deve deixar claro:

- dado de entrada;
- fonte ou premissa;
- fórmula usada;
- resultado;
- unidade;
- observação sobre incerteza.

## Pontos Fracos do Plano Anterior

1. Premissas ainda estavam genéricas.
   - Risco: parecer que a meta semanal, eficiência e tempos foram escolhidos sem critério.
   - Correção: registrar cada premissa em matriz de dados e separar o que é fonte oficial do que é estimativa de engenharia.

2. Capacidade de equipamentos podia virar chute.
   - Risco: misturar capacidade oficial do fabricante com produtividade estimada por peça.
   - Correção: na Tabela 3, registrar a capacidade informada pelo fabricante; no cálculo, registrar quando a produtividade por kit é estimada por tempo padrão.

3. Layout podia ser desenhado antes da capacidade.
   - Risco: layout bonito, mas desconectado do número de máquinas.
   - Correção: calcular quantidade de máquinas antes de fechar áreas e mapofluxograma.

4. Fluxograma e Tabela 2 poderiam divergir.
   - Risco: numeração diferente entre tabela, fluxograma e mapofluxograma.
   - Correção: gerar diagramas a partir da mesma lista de processos em JSON.

5. O dashboard poderia competir com a entrega formal.
   - Risco: gastar tempo em HTML e negligenciar PDF/XLSX/draw.io.
   - Correção: dashboard será apoio e revisão; entrega formal continua sendo PDF final, XLSX e draw.io. A montagem em slides/PPTX fica como última etapa, depois que a base técnica estiver fechada.

6. Pesquisa de mercado e tecnologia podia ficar superficial.
   - Risco: cálculos sem base técnica para processos de cutelaria, madeira e embalagem.
   - Correção: pesquisar produto, materiais, processo, equipamentos, capacidades e dimensões antes de consolidar a apresentação.

## Estratégia Corrigida

1. Usar os slides da aula como método:
   Produto -> árvore pai-filho -> materiais -> fazer/comprar -> processos -> fluxograma -> layout -> mapofluxograma -> tipo de arranjo.

2. Usar a matriz de pesquisa como base técnica:
   - Tramontina para produto, embalagem e desenho técnico.
   - Aperam/Rolmetais para aço inox 420.
   - fontes técnicas de madeira para densidade/trabalhabilidade da Maçaramduba.
   - fabricantes de máquinas para dimensões/capacidades.

3. Usar código para contas:
   - demanda bruta;
   - quantidade semanal por componente;
   - capacidade por processo;
   - quantidade de máquinas;
   - cálculo detalhado do equipamento selecionado;
   - estimativa de área.

4. Gerar saídas editáveis:
   - `02_calculos/demonstrativo_calculos.xlsx`;
   - `03_diagramas/fluxograma_processo.drawio`;
   - `03_diagramas/layout_esquematico.drawio`;
   - `03_diagramas/mapofluxograma.drawio`;
   - `06_dashboard/index.html`.

## Decisão de Escopo

O projeto será tratado como proposta básica de fábrica para um único produto: Kit para Churrasco Tramontina 3 peças, referência 22399036. A fábrica proposta integra processos metálicos, madeira, montagem e embalagem. O arranjo físico esperado tende a ser misto: setores funcionais para metal e madeira, com fluxo final em linha/célula de montagem e embalagem.
