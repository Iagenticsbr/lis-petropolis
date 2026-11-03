# src

Código do pipeline. Ainda vazio: a arquitetura é uma proposta (ver `docs/arquitetura/`).

Layout proposto na seção 2.5 do PDF, para quando a implementação começar:

```text
src/lis/
├─ contracts/     # RawItem, Item, Label (pydantic)
├─ collectors/
│  ├─ own/        # um módulo por fonte
│  └─ apify/      # um adaptador por actor
├─ normalize/     # idioma, dedupe, autor em hash
├─ classify/      # Classifier + adaptadores jev e claude
├─ aggregate/     # séries, picos e vales, exemplos
├─ synthesize/    # prompts, validadores, níveis N3 a N5
├─ deliver/       # relatório e views SQL
└─ pipeline/      # orquestração (Dagster ou Prefect)
```

Nenhum módulo conhece a nuvem: o que muda por ambiente vem de variáveis e do Terraform.
