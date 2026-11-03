# Decisões de arquitetura (ADR)

As ADRs 001 a 009 do projeto estão no documento ADR-LIS, linkado no projeto do Linear, e **todas têm status Proposta**. A Proposta v2 (03/11/2026) não as altera até ser aprovada.

Quando um item abaixo for decidido, ele vira uma ADR neste diretório, numerada a partir da primeira livre depois das já existentes, no formato `NNN-titulo-curto.md`.

## Decisões em aberto

| Tema | Proposta | Quando decidir |
| --- | --- | --- |
| Onde hospedar | Construir portátil (Docker e Terraform) e escolher o destino depois: nuvem da IAgentics, Azure do Grupo ou outra. | Até 18/01, quando o Grupo entrega subscrição, quotas e dono dos custos |
| Classificador | Disputa entre Jev e um Claude pequeno em amostra própria; o vencedor vira o padrão. | Antes do M2 (18/12); amostra própria antes de 20/11 |
| Trilha de cada fonte | Regra de quatro perguntas, registrada em `sources/catalog.yaml`. | Catálogo de fontes v1 (M0) |
| Redes sociais | Quais entram, em que fase e com qual fornecedor, depois do jurídico. | Posição do jurídico prevista para 04/12 |
| Níveis do MVP | N0 a N3 e N5 agora; N4 (cruzamento) depois do M3. | Revisar após o M3 (22/01) |
| Modelo por nível | Menor em N3 e mais forte em N5, a confirmar por custo e qualidade. | Junto com a disputa do classificador |
| Revisão humana | 100% em N4 e N5; amostra em N3. | Reduzir quando as métricas de fundamentação permitirem |
| Orquestrador | Dagster ou Prefect, ou algo mínimo (cron e fila) se o volume permitir. | Antes de ligar a coleta agendada (M1) |

## Modelo de ADR

```markdown
# NNN · Título

- Status: Proposta | Aceita | Substituída por NNN
- Data: AAAA-MM-DD
- Decisores:

## Contexto
## Decisão
## Alternativas consideradas
## Consequências
```
