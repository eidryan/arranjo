# Memoria de calculo transparente

Todas as contas abaixo foram geradas por `scripts/generate_outputs.py` a partir de `data/projeto.json`.

## Demanda

- Meta de produtos bons: 1000 kits/semana.
- Rendimento final assumido: 95.00%.
- Demanda bruta: ceil(1000 / 0.95) = 1053 kits/semana.
- Horas uteis: 5 dias * 1 turno * 7 h = 35.0 h/semana.
- Ritmo medio necessario: 1053 / 35.0 = 30.09 kits/h.

## Equipamento selecionado para memoria detalhada

- Equipamento: Router CNC para madeira - Maksiwa Store RTC.1313.
- Operacoes consideradas: 13 - Fresar sulco da tabua e usinar/furar cabos.
- Motivo da selecao: A tabua e os cabos exigem usinagem/fresagem com repetibilidade; a etapa tem tempo padrao estimado alto e tende a ser gargalo..
- Tempo padrao: 120 s/kit.
- Taxa nominal: 3600 / 120 = 30.00 kits/h.
- Taxa efetiva: 30.00 * 0.85 * 0.92 * 0.98 = 22.99 kits/h.
- Capacidade semanal por maquina: 22.99 * 35.0 = 804.68 kits/semana.
- Quantidade necessaria: ceil(1053 / 804.68) = 2 equipamento(s).
- Utilizacao estimada: 65.4%.

## Areas

- Area total proposta: 24 m * 16 m = 384.0 m2.
- Area estimada necessaria: 260.4 m2.
- Ocupacao: 67.8%; folga: 123.6 m2.
