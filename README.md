# LIS · Inteligência de Comportamento Digital (Grupo Petrópolis)

Sistema de monitoramento de fontes públicas da web sobre o portfólio de bebidas do Grupo Petrópolis. A cada ciclo entrega análises de tendência (mínimas e máximas) e insights, e cada insight pode ser rastreado até o conteúdo que o originou.

Projeto da IAgentics para o LIS (Lab de Inovação e Sustentabilidade) do Grupo. Prazo final: 26/02/2027.

## Estado atual

O repositório começa pela documentação. A arquitetura, o modelo de dados e o motor de análise estão descritos na **Proposta v2 (03/11/2026)**, que ainda aguarda decisão e **não altera as ADRs 001 a 009** (todas com status Proposta). Não há código de produto aqui ainda.

Plano, marcos e tarefas ficam no Linear, que é a fonte da verdade do andamento:
[Grupo Petrópolis (LIS) · Inteligência de Comportamento Digital](https://linear.app/iagentics/project/grupo-petropolis-lis-inteligencia-de-comportamento-digital-54162d930a8a) (time IAG).

## Em uma página

- **Coleta em três trilhas** que entregam o mesmo contrato `RawItem`: scraper próprio em HTTP, scraper próprio com navegador (Playwright) e Apify para fontes com defesa contra robôs. A trilha de cada fonte é decidida por quatro perguntas e registrada em `sources/catalog.yaml`.
- **Dados** em quatro schemas no Postgres (`core`, `analytics`, `gov`, `bi`) mais uma zona bruta em armazenamento de objetos compatível com S3. Rótulos e insights só são acrescentados, nunca sobrescritos.
- **Análise em seis níveis** (N0 a N5): o código calcula todo número, o Jev (TypeSafe) rotula em volume e o Claude escreve a partir do N3. Toda frase cita evidências e validadores em código recusam número sem origem.
- **Portátil**: containers e Terraform, sem serviço proprietário de nuvem no caminho crítico. O destino de hospedagem continua em aberto.

## Estrutura do repositório

| Pasta | Conteúdo |
| --- | --- |
| `docs/` | Documentação. Comece por [`docs/README.md`](docs/README.md). |
| `docs/arquitetura/` | PDF da proposta (arquitetura, dados e motor de análise) e a fonte para reconstruí-lo. |
| `docs/dados/` | `schema.sql` (DDL de referência) e `raw_item.py` (contrato RawItem). |
| `docs/adr/` | Registro de decisões de arquitetura deste repositório. |
| `sources/` | Catálogo de fontes (`catalog.yaml`): trilha, cadência e status jurídico de cada uma. |
| `src/` | Código do pipeline (ainda vazio; layout proposto em [`src/README.md`](src/README.md)). |
| `evals/` | Conjunto de referência e avaliação de classificadores (ainda vazio). |
| `tests/` | HTML gravado dos scrapers e testes de contrato (ainda vazio). |
| `infra/` | Terraform, Dockerfiles e compose (ainda vazio). |

## Como trabalhamos

Segue a definição de pronto do projeto no Linear: testes passando em CI, logs e alertas da parte nova, IaC e documentação atualizadas, ADR revisada se a decisão mudou e custo da sprint registrado. Todo pull request, mesmo gerado por IA, passa por revisão cruzada.

## Nota sobre dados de terceiros

Preços e limites de fornecedores citados nos documentos vêm de páginas públicas e devem ser revalidados nos sites oficiais antes de entrarem no orçamento. Nada nesta documentação é parecer jurídico.
