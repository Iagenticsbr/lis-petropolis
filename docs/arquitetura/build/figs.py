"""Figuras 4 a 7 do documento LIS (SVG inline, mesmas classes de estilo das figuras 1 a 3)."""
from html import escape as esc


def marker(mid):
    return (f'<defs><marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
            f'markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="currentColor"/>'
            f'</marker></defs>')


def svg(cls, vb, label, mid, body):
    w, h = vb
    return (f'<svg class="{cls}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">'
            f'{marker(mid)}{body}</svg>')


def T(x, y, s, cls=""):
    return f'<text class="{cls}" x="{x}" y="{y}">{esc(s)}</text>'


def edge(d, mid, cls="edge"):
    return f'<path class="{cls}" d="{d}" marker-end="url(#{mid})"/>'


def tbox(x, y, w, h, cls, title, lines, step=13.5, first=33):
    """Caixa de tabela: título em negrito e campos em mono."""
    out = [f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="6"/>',
           T(x + 10, y + 18, title, "s")]
    for i, ln in enumerate(lines):
        out.append(T(x + 10, round(y + first + i * step, 1), ln, "m s"))
    return "".join(out)


# ---------------------------------------------------------------- Figura 4: ERD
def fig4():
    mid = "a4"
    W, H = 1100, 556
    colw, gap = 190, 32.5
    X = [10 + i * (colw + gap) for i in range(5)]
    b = []

    # rótulos das faixas
    b.append(T(10, 14, "COLETA E DADO", "t2 m s"))
    b.append(T(10, 178, "ANÁLISE", "t2 m s"))
    b.append(T(10, 332, "REFERÊNCIA (FK) E EVIDÊNCIA", "t2 m s"))
    b.append(T(10, 468, "GOVERNANÇA", "t2 m s"))

    # ---- linha 1: coleta e dado
    y1, h1 = 22, 118
    boxes1 = [
        ("core.source", ["source_id  PK", "nome, trilha", "cadencia", "status_juridico, ativo"]),
        ("core.collector_run", ["run_id  PK", "source_id  FK", "iniciado_em, concluido_em", "status", "itens_coletados, erros"]),
        ("core.raw_item", ["raw_id  PK", "run_id  FK", "uri_objeto", "hash_payload", "coletado_em"]),
        ("core.item", ["item_id  PK", "source_id, raw_id  FK", "publicado_em, idioma", "texto, texto_hash", "autor_hash, dedupe_grupo", "metricas"]),
        ("core.label", ["label_id  PK", "item_id  FK", "pergunta, resposta", "prob, confianca", "origem, criado_em", "modelo_id  FK"]),
    ]
    for i, (t, ls) in enumerate(boxes1):
        b.append(tbox(X[i], y1, colw, h1, "box", t, ls))
    ym = y1 + h1 / 2
    for i in range(4):
        b.append(edge(f"M{X[i]+colw} {ym} H{X[i+1]-1}", mid))

    # ---- linha 2: análise (lida da direita para a esquerda)
    y2, h2 = 186, 118
    b.append(tbox(X[4], y2, colw, h2, "zana", "analytics.series_point",
                  ["dia, source_id", "tema_id, marca_id  FK", "volume, share", "sentimento_medio", "engajamento, cobertura"]))
    b.append(tbox(X[3], y2, colw, h2, "zana", "analytics.signal",
                  ["signal_id  PK", "tipo, escopo, periodo", "magnitude, z_robusto", "itens_distintos", "cobertura_ok, prioridade", "metodo_versao"]))
    b.append(tbox(X[2], y2, colw, h2, "zana", "analytics.insight",
                  ["insight_id  PK", "nivel  (N3, N4, N5)", "escopo, texto, saida_json", "payload_hash, prompt_hash", "confianca, status", "modelo_id  FK"]))
    b.append(tbox(X[1], y2, colw, h2, "zana", "analytics.report",
                  ["report_id  PK", "periodo, tipo", "status, publicado_em", "report_insight  (ordem)"]))
    # label -> series_point (desce)
    xc = X[4] + colw / 2
    b.append(edge(f"M{xc} {y1+h1} V{y2-1}", mid))
    ym2 = y2 + h2 / 2
    b.append(edge(f"M{X[4]-0.5} {ym2} H{X[3]+colw+1}", mid))
    b.append(edge(f"M{X[3]-0.5} {ym2} H{X[2]+colw+1}", mid))
    b.append(edge(f"M{X[2]-0.5} {ym2} H{X[1]+colw+1}", mid))
    # nota de leitura (coluna 1 da linha 2)
    b.append(T(X[0], y2 + 30, "Leitura da análise:", "s"))
    for i, ln in enumerate(["da direita para a esquerda.", "Cada seta aponta para o que", "é derivado da caixa de onde", "ela sai."]):
        b.append(T(X[0], y2 + 48 + i * 14, ln, "t2 s"))

    # ---- linha 3: referência (esquerda) e evidência (sob o insight)
    y3, h3 = 348, 96
    ref_x, ref_w = X[0] - 6, X[1] + colw - X[0] + 12
    b.append(f'<rect class="env" x="{ref_x}" y="{y3-8}" width="{ref_w}" height="{h3+16}" rx="8" style="stroke-dasharray:5 4"/>')
    b.append(tbox(X[0], y3, colw, h3, "box", "core.taxonomy", ["tax_id  PK", "tipo  (tema, marca)", "nome, pai_id  FK", "versao"]))
    b.append(tbox(X[1], y3, colw, h3, "box", "core.model_version", ["modelo_id  PK", "provedor, nome", "versao_fixa", "parametros, ativo"]))
    b.append(tbox(X[2], y3, colw, h3, "zana", "analytics.insight_evidence",
                  ["insight_id  FK", "tipo, ref_id", "papel", "PK: os três primeiros"]))
    b.append(edge(f"M{X[2]+colw/2} {y2+h2} V{y3-1}", mid))
    b.append(T(X[2] + colw / 2 + 8, y2 + h2 + 27, "cita", "t2 s"))
    # nota sobre a referência polimórfica (colunas 4 e 5 da linha 3)
    ex = X[3]
    b.append(T(ex, y3 + 18, "ref_id é polimórfico:", "s"))
    for i, ln in enumerate(["aponta para signal, series_point,", "item ou outro insight. Uma rotina", "de integridade valida cada referência."]):
        b.append(T(ex, y3 + 36 + i * 14, ln, "t2 s"))

    # ---- linha 4: governança
    y4, h4 = 476, 76
    b.append(tbox(X[0], y4, colw, h4, "zgov", "gov.eval_label", ["set_id, item_id", "pergunta, resposta_ouro", "rotulador"], first=32))
    b.append(tbox(X[1], y4, colw, h4, "zgov", "gov.eval_run", ["run_id  PK", "modelo_id, set_id  FK", "f1 por pergunta, custo"], first=32))
    b.append(tbox(X[2], y4, colw, h4, "zgov", "gov.review_task", ["task_id  PK", "tipo, ref_id, motivo", "status, revisor"], first=32))
    b.append(tbox(X[3], y4, colw, h4, "zgov", "gov.cost_ledger", ["id  PK", "provedor, run_id, unidade", "quantidade, custo_usd"], first=32))
    b.append(edge(f"M{X[0]+colw} {y4+h4/2} H{X[1]-1}", mid))
    b.append(T(X[4], y4 + 14, "Só acrescenta. review_task", "t2 s"))
    for i, ln in enumerate(["e cost_ledger apontam por", "ref_id para rótulos, insights", "e execuções."]):
        b.append(T(X[4], y4 + 30 + i * 14, ln, "t2 s"))

    return svg("f4", (W, H),
               "Diagrama de entidades: coleta e dado, análise, referência e evidência, e governança, com as setas de derivação de source até report.",
               mid, "".join(b))


# ---------------------------------------------------------------- Figura 5: os seis níveis
def fig5():
    mid = "a5"
    W, H = 1100, 500
    cx = 190
    widths = [350, 310, 270, 230, 190, 150, 120]
    levels = [
        ("N0 · Item rotulado", "milhares de itens", "ext",
         ("Jev, versão fixa", "Claude pequeno só na 2ª opinião"),
         ("Rótulo com confiança ≥ τ, ou resolvido pela 2ª opinião", "ou por um humano, e com relevante = sim.")),
        ("N1 · Ponto de série", "um por dia, tema, marca e fonte", "box",
         ("SQL no Postgres", "agregação recalculável"),
         ("Cobertura do dia ≥ 0,8 (valor inicial) e amostra mínima;", "senão vira “dados incompletos” e não sobe.")),
        ("N2 · Sinal", "dezenas por ciclo", "box",
         ("Estatística em código", "z robusto, CUSUM, regras"),
         ("Estar entre os K sinais de maior prioridade do escopo:", "o número de chamadas segue os sinais, não os itens.")),
        ("N3 · Insight local", "um por sinal prioritário", "ext",
         ("Claude · analista de sinal", "pacote fechado, saída em JSON"),
         ("Passar nos validadores V1 a V6 e na revisão por amostra.", "Sem evidência citada, o insight não sobe.")),
        ("N4 · Insight cruzado", "poucas conexões", "ext",
         ("Claude · cruzamento", "fase 2, depois do M3"),
         ("Passar nos validadores e na revisão humana de 100%.", "Só conecta; não afirma causa nem traz fato novo.")),
        ("N5 · Relatório", "um por ciclo", "ext",
         ("Claude · redator executivo", "só usa insights aprovados"),
         ("Revisão humana de 100% antes de publicar.", "Todo número do texto já está nos insights.")),
    ]
    b = []
    y0, bh, gap = 34, 62, 14
    b.append(T(10, 14, "NÍVEL E PEÇA (A LARGURA É O VOLUME)", "t2 m s"))
    b.append(T(395, 14, "QUEM PRODUZ", "t2 m s"))
    b.append(T(675, 14, "PARA SUBIR AO NÍVEL SEGUINTE", "t2 m s"))
    for i, (name, sub, cls, prod, cond) in enumerate(levels):
        y = y0 + i * (bh + gap)
        wt, wb = widths[i], widths[i + 1]
        pts = f"{cx-wt/2},{y} {cx+wt/2},{y} {cx+wb/2},{y+bh} {cx-wb/2},{y+bh}"
        extra = ' style="opacity:.82"' if i == 4 else ""
        b.append(f'<polygon class="{cls}" points="{pts}"{extra}/>')
        b.append(T(cx, y + 28, name, "c"))
        b.append(T(cx, y + 46, sub, "t2 c"))
        ymid = y + bh / 2
        xr = cx + (wt + wb) / 4
        b.append(f'<path class="edge soft" d="M{xr+3} {ymid} H394"/>')
        # produtor
        b.append(f'<rect class="{cls}" x="395" y="{ymid-25}" width="245" height="50" rx="6"{extra}/>')
        b.append(T(407, ymid - 4, prod[0], "s"))
        b.append(T(407, ymid + 13, prod[1], "t2 s"))
        # condição
        b.append(f'<rect class="src" x="675" y="{ymid-25}" width="415" height="50" rx="6"/>')
        b.append(T(687, ymid - 4, cond[0], "t2 s"))
        b.append(T(687, ymid + 13, cond[1], "t2 s"))
        if i < 5:
            b.append(edge(f"M{cx} {y+bh+1} V{y+bh+gap-1}", mid))
    return svg("f5", (W, H),
               "Funil de seis níveis, de item rotulado a relatório, com quem produz cada peça e a condição para subir ao nível seguinte.",
               mid, "".join(b))


# ---------------------------------------------------------------- Figura 6: uma chamada N3
def fig6():
    mid = "a6"
    W, H = 1100, 440
    b = []
    ym = 160
    # A: sinal
    b.append(tbox(10, 100, 140, 120, "zana", "Sinal prioritário",
                  ["analytics.signal", "um dos K de maior", "prioridade do", "escopo"], first=36))
    b.append(edge("M150 160 H183", mid))
    # B: pacote (código)
    b.append(tbox(185, 80, 195, 160, "key", "Pacote de contexto",
                  ["montado em código:", "· o sinal e o período", "· a série com janela", "· comparativo anterior", "· k exemplos curtos", "· insights anteriores", "grava payload_hash"], first=36))
    b.append(edge("M380 160 H413", mid))
    # C: Claude
    b.append(tbox(415, 100, 170, 120, "ext", "Claude · N3",
                  ["modelo do nível, versão", "fixa; prompt versionado;", "resposta em JSON", "grava modelo_id e", "prompt_hash"], first=36))
    b.append(edge("M585 160 H618", mid))
    # D: validadores (decisão)
    b.append('<polygon class="key" points="690,95 765,160 690,225 615,160"/>')
    b.append(T(690, 156, "V1 a V6", "c"))
    b.append(T(690, 172, "passam?", "c"))
    # sim
    b.append(edge("M765 160 H796", mid))
    b.append(T(780, 150, "sim", "t2 c"))
    b.append(tbox(798, 100, 140, 120, "zana", "Rascunho",
                  ["grava insight e", "insight_evidence;", "confiança calculada", "em código"], first=36))
    b.append(edge("M938 160 H964", mid))
    b.append(tbox(966, 104, 124, 112, "key", "Revisão humana",
                  ["N4 e N5: 100%;", "N3: amostra.", "aprovado: vira", "publicado"], first=36))
    # 1ª falha: volta ao Claude
    b.append(edge("M690 95 V52 H500 V99", mid))
    b.append(T(595, 44, "1ª falha: volta ao Claude com a lista de erros (uma nova tentativa)", "t2 c"))
    # 2ª falha ou V6: fila
    b.append(edge("M690 225 V300", mid))
    b.append(T(698, 262, "2ª falha, ou V6 (dado pessoal)", "t2 s"))
    b.append(f'<rect class="zgov" x="590" y="302" width="200" height="56" rx="6"/>')
    b.append(T(690, 326, "Fila de revisão humana", "c"))
    b.append(T(690, 344, "gov.review_task", "t2 c"))
    # revisor decide -> revisão
    b.append(edge("M790 330 H1028 V217", mid))
    b.append(T(912, 322, "o revisor aprova, corrige ou descarta", "t2 c"))
    # custo
    b.append(f'<rect class="src" x="185" y="392" width="905" height="36" rx="6"/>')
    b.append(T(197, 414, "Toda chamada grava custo e tokens em gov.cost_ledger. Pelo par modelo e prompt, mais o payload_hash, a chamada pode ser reconstruída.", "t2 s"))
    return svg("f6", (W, H),
               "Chamada do nível N3: o sinal vira um pacote de contexto montado em código, o Claude responde em JSON, os validadores V1 a V6 aprovam ou devolvem uma vez, e a segunda falha vai para revisão humana.",
               mid, "".join(b))


# ---------------------------------------------------------------- Figura 7: cadeia de evidências
def fig7():
    mid = "a7"
    W, H = 1100, 522
    bx, bw, bh, gap = 190, 380, 48, 26
    rows = [
        ("zana", "Relatório do ciclo (N5)", "“…subiu de 2,0% para 6,2%…” → cita ins-0412",
         "report_insight", "analytics.report", "A frase que o gestor lê, ligada aos insights aprovados."),
        ("zana", "Insight ins-0412 (N3)", "confiança média · modelo_id e prompt_hash gravados",
         "saida_json.numeros[].origem", "analytics.insight", "Texto, hipóteses, limitações e o caminho de cada número."),
        ("zana", "Sinal sig-0877 e pacote de contexto", "pico · 10 a 12/11 · z robusto 4,1 · payload_hash",
         "signal.escopo + periodo", "analytics.signal", "O que o Claude recebeu e por que este sinal subiu."),
        ("zana", "Ponto de série", "2026-11-12 · embalagem · Marca A · portal-x · share 0,062",
         "dia, fonte, tema e marca", "analytics.series_point", "Os números do dia: volume, share, cobertura."),
        ("box", "Rótulos (N0)", "tema = embalagem · sentimento = 2 · jev-1.13.0",
         "label.item_id", "core.label, core.model_version", "Quem classificou, com qual versão e qual confiança."),
        ("box", "Item itm-9f3a", "portal-x · texto_hash · autor_hash · métricas",
         "item.raw_id", "core.item", "Texto limpo e hash; o autor só aparece em hash."),
        ("box", "Payload bruto e post original", "raw_item.uri_objeto · URL canônica da fonte",
         None, "core.raw_item e armazenamento de objetos", "Payload original e imutável, com o link da publicação."),
    ]
    b = []
    b.append(T(190, 12, "PEÇA E EXEMPLO", "t2 m s"))
    b.append(T(600, 12, "ONDE ESTÁ E O QUE MOSTRA", "t2 m s"))
    y0 = 20
    ys = []
    for i, (cls, title, ex, key, where, what) in enumerate(rows):
        y = y0 + i * (bh + gap)
        ys.append(y)
        b.append(f'<rect class="{cls}" x="{bx}" y="{y}" width="{bw}" height="{bh}" rx="6"/>')
        b.append(T(bx + 12, y + 20, title, "s"))
        b.append(T(bx + 12, y + 37, ex, "t2 s"))
        b.append(f'<rect class="src" x="600" y="{y}" width="490" height="{bh}" rx="6"/>')
        b.append(T(612, y + 20, where, "m s"))
        b.append(T(612, y + 37, what, "t2 s"))
        if key:
            xa = bx + 60
            b.append(edge(f"M{xa} {y+bh+1} V{y+bh+gap-1}", mid))
            b.append(T(xa + 12, y + bh + 17, "chave: " + key, "t2 m s"))
    # atalho: insight -> item (evidências citadas)
    ya, yb = ys[1] + bh / 2, ys[5] + bh / 2
    b.append(f'<path class="edge" style="stroke:var(--accent);stroke-width:2" d="M{bx-1} {ya} H150 V{yb} H{bx-1}" marker-end="url(#{mid})"/>')
    b.append(T(138, ya + 28, "insight_evidence", "m e"))
    b.append(T(138, ya + 44, "as frases e os posts", "t2 e"))
    b.append(T(138, ya + 58, "citados no texto,", "t2 e"))
    b.append(T(138, ya + 72, "com papel: base,", "t2 e"))
    b.append(T(138, ya + 86, "exemplo ou", "t2 e"))
    b.append(T(138, ya + 100, "contraexemplo", "t2 e"))
    return svg("f7", (W, H),
               "Cadeia de evidências, do relatório ao post original, passando por insight, sinal, ponto de série, rótulos e item, com as chaves de cada ligação e um atalho do insight direto aos itens citados.",
               mid, "".join(b))


FIGS = {"FIG4": fig4, "FIG5": fig5, "FIG6": fig6, "FIG7": fig7}
