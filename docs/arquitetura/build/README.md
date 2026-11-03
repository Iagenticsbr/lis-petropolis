# Como reconstruir o PDF

O PDF `../LIS-arquitetura-dados-e-motor-de-analise.pdf` é gerado a partir de HTML com Chromium (Playwright). O build faz duas passadas: a primeira descobre em que página cai cada título, a segunda preenche o sumário com os números certos. No fim, carimba o rodapé ("LIS · Grupo Petrópolis · IAgentics", página N / total) e grava metadados.

## Requisitos

- Python 3.10 ou superior com `playwright`, `pikepdf`, `reportlab` e `fonttools`
- Chromium instalado para o Playwright (`playwright install chromium`)
- Node e npm, só para baixar as fontes

## Passos

```bash
# 1. fontes (Bricolage Grotesque, Source Sans 3, JetBrains Mono)
cd docs/arquitetura/build/fonts && npm ci && cd ..

# 2. PDF, gravado em docs/arquitetura/
python build.py

# opcional: gravar em outra pasta
OUT_DIR=/caminho/qualquer python build.py
```

O build termina com `pass2 páginas: 27 | deriva do sumário: {}`. Se a deriva do sumário não vier vazia, o sumário está apontando para a página errada: rode de novo.

## Arquivos

| Arquivo | Papel |
| --- | --- |
| `p0_head.html` | CSS e cabeçalho (inclui o marcador das fontes) |
| `p1_a.html` | Capa, sumário e seções 1 e 2 |
| `p2_b.html` | Seção 3 (modelo de dados) |
| `p3_c.html` | Seção 4 (motor de análise) |
| `p4_d.html` | Seção 5 e anexos A a D |
| `figuras/fig1.svg` a `fig3.svg` | Diagramas das figuras 1 a 3 |
| `figs.py` | Gera as figuras 4 a 7 |
| `build.py` | Monta, renderiza, numera o sumário, carimba rodapé e metadados |
| `fonts/package.json` | Dependências das fontes (`node_modules` não vai para o git) |

Arquivos intermediários (`build.html`, `pass1.pdf`, `pass2.pdf`, `pages.json`, `_*.ttf`) são ignorados pelo git.
