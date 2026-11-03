# Documentação do LIS

| Documento | O que é | Status |
| --- | --- | --- |
| [`arquitetura/LIS-arquitetura-dados-e-motor-de-analise.pdf`](arquitetura/LIS-arquitetura-dados-e-motor-de-analise.pdf) | Arquitetura de software, modelo de dados e motor de análise por níveis (N0 a N5). 27 páginas, com diagramas, DDL, contrato RawItem e glossário. | Proposta v2, de 03/11/2026, para decisão |
| [`dados/schema.sql`](dados/schema.sql) | DDL de referência (Postgres), extraída do Anexo A do PDF. | Proposta; validada em Postgres 16 |
| [`dados/raw_item.py`](dados/raw_item.py) | Contrato `RawItem` (pydantic), extraído do Anexo B do PDF. | Proposta |
| [`adr/`](adr/README.md) | Decisões em aberto que viram ADRs quando forem decididas. | A abrir |

## Outras referências do projeto

Estes documentos ficam fora do repositório, linkados no projeto do Linear: ENG-LIS (Documento de Engenharia), PDR-LIS (Preliminary Design Review), ADR-LIS (ADRs 001 a 009) e o plano de sprints revisado em 13/10/2026.

## Regras para os documentos

- O PDF é gerado a partir de `arquitetura/build/`. Para mudar o texto, edite o HTML de lá e reconstrua; não edite o PDF.
- Mudou o PDF? Atualize também `dados/schema.sql` e `dados/raw_item.py` se o Anexo A ou B mudou.
- Documento novo entra na tabela acima, com versão, data e status.
