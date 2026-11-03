# Dados

Referência do modelo de dados descrito na seção 3 do PDF de arquitetura. Os dois arquivos aqui são extraídos dos anexos A e B, sem mudança de conteúdo.

| Arquivo | Conteúdo |
| --- | --- |
| `schema.sql` | Schemas `core`, `analytics`, `gov` e `bi`; tabelas de `core` e `analytics` (fonte, execução de coleta, item bruto, taxonomia, versão de modelo, item, rótulo, ponto de série, sinal, insight e evidência) e a view `core.label_current`. |
| `raw_item.py` | Contrato `RawItem`: única fronteira entre a coleta e o resto do pipeline. |

## Regras do modelo (resumo)

- Chaves determinísticas: `item_id = sha256(source_id || url_canonica)`.
- Rótulos e insights só são acrescentados, nunca sobrescritos. Insights viram `obsoleto`, não são apagados.
- Cada rótulo e cada insight guardam a versão do modelo que os produziu (`core.model_version`).
- O autor nunca é gravado em claro: só `autor_hash` (HMAC-SHA256).
- Séries e sinais são recalculáveis a partir de `core`.

## Pontos a alinhar antes de virar migração

- O exemplo do catálogo de fontes usa `id` e `robots_ok`; a tabela `core.source` usa `source_id` e não tem coluna para `robots_ok`. Decidir se o catálogo mapeia `id` para `source_id` e se `robots_ok` entra na tabela.
- `gov.*`, `analytics.report` e as views `bi.*` estão só em resumo no PDF e ainda não têm DDL.
- A zona bruta tem retenção curta, com prazo a definir com o jurídico do Grupo.

O `schema.sql` foi executado em Postgres 16 sem erro, em um banco vazio.
