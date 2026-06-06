# Projeto de fabrica - Tramontina 22399036

Pacote base para a Atividade 2, usando o produto:
Kit para Churrasco Tramontina com Laminas em Aco Inox e Cabos em Madeira Natural 3 Pecas.

## Regra central do pacote

Todas as contas foram feitas em codigo e podem ser auditadas.

- Entradas, fontes e premissas: `data/projeto.json`
- Script de calculo e geracao dos artefatos: `scripts/generate_outputs.py`
- Builder do demonstrativo em Excel: `scripts/build_workbook.mjs`
- Resultados calculados: `data/resultados_calculo.json`
- Demonstrativo editavel: `02_calculos/demonstrativo_calculos.xlsx`
- Memoria em texto: `02_calculos/memoria_calculo_transparente.md`

## Artefatos principais

- `01_apresentacao/roteiro_slides.md`: roteiro para montar a apresentacao de 20 minutos. O PPTX fica por ultimo, depois que todos os dados, calculos e diagramas estiverem fechados.
- `02_calculos/demonstrativo_calculos.xlsx`: premissas, BOM, processos, equipamentos, capacidades, materiais e layout.
- `03_diagramas/fluxograma_processo.drawio`: fluxograma editavel.
- `03_diagramas/layout_esquematico.drawio`: layout editavel.
- `03_diagramas/mapofluxograma.drawio`: mapofluxograma editavel.
- `05_base_tecnica/revisao_plano_e_pontos_fracos.md`: revisao critica do plano.
- `05_base_tecnica/fontes_pesquisa_e_premissas.md`: fontes e premissas usadas.
- `06_dashboard/index.html`: central HTML com frentes visuais, renderizacoes, links e dashboard.
- `06_dashboard/renders/*.svg`: renderizacoes visuais do fluxograma, layout e mapofluxograma.

## Resultado numerico atual

- Meta: 1.000 kits bons por semana.
- Rendimento final assumido: 95%.
- Demanda bruta calculada: 1.053 kits por semana.
- Jornada util: 35 h/semana.
- Ritmo medio requerido: 30,09 kits/h.
- Equipamento detalhado: Router CNC Maksiwa Store RTC.1313.
- Quantidade calculada para o router: 2 unidades.
- Area total proposta: 384 m2.
- Area requerida estimada: aproximadamente 260,4 m2.

## Integrantes registrados

- Bernardo Gomes
- Lucas de Mello
- Clara Hermsdorff
- João Deccax
- André Baptista

Pendente: a captura mostra um integrante como "You"; falta substituir pelo nome real antes da entrega final.

## Como regenerar

Execute:

```powershell
.\scripts\run_all.ps1
```

O comando recalcula tudo a partir de `data/projeto.json` e sobrescreve os artefatos derivados.

## Limites assumidos

As fontes de fabricante foram usadas quando estavam disponiveis. Onde a fonte nao informava capacidade real por kit, o pacote marca como premissa e aplica a mesma politica de eficiencia, confiabilidade e rendimento para manter consistencia.
