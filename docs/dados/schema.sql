-- LIS · DDL de referência (Postgres)
-- Origem: Anexo A de docs/arquitetura/LIS-arquitetura-dados-e-motor-de-analise.pdf (Proposta v2, 03/11/2026).
-- Cobre as entidades dos schemas core e analytics da seção 3.4 do documento.
-- Ainda não cobre: gov.* (conjunto de referência, execuções de avaliação, fila de revisão, custos),
-- analytics.report e as views bi.* (descritas só em resumo no documento).
-- Status: proposta; não é migração. Quando virar migração, vai para o diretório de migrações do pipeline.

CREATE SCHEMA core; CREATE SCHEMA analytics; CREATE SCHEMA gov; CREATE SCHEMA bi;

CREATE TABLE core.source (
  source_id        text PRIMARY KEY,
  nome             text NOT NULL,
  trilha           text NOT NULL CHECK (trilha IN ('own_http','own_js','apify','fora_mvp')),
  cadencia         interval,
  status_juridico  text NOT NULL DEFAULT 'pendente'
                   CHECK (status_juridico IN ('liberado','pendente','negado')),
  ativo            boolean NOT NULL DEFAULT true
);

CREATE TABLE core.collector_run (
  run_id           uuid PRIMARY KEY,
  source_id        text NOT NULL REFERENCES core.source,
  iniciado_em      timestamptz NOT NULL,
  concluido_em     timestamptz,
  status           text NOT NULL CHECK (status IN ('ok','parcial','falhou')),
  itens_coletados  integer NOT NULL DEFAULT 0,
  erros            integer NOT NULL DEFAULT 0
);

CREATE TABLE core.raw_item (
  raw_id        uuid PRIMARY KEY,
  run_id        uuid NOT NULL REFERENCES core.collector_run,
  uri_objeto    text NOT NULL,
  hash_payload  text NOT NULL,
  coletado_em   timestamptz NOT NULL
);

CREATE TABLE core.taxonomy (
  tax_id  integer PRIMARY KEY,
  tipo    text NOT NULL CHECK (tipo IN ('tema','marca','produto')),
  nome    text NOT NULL,
  pai_id  integer REFERENCES core.taxonomy,
  versao  integer NOT NULL
);

CREATE TABLE core.model_version (
  modelo_id    integer PRIMARY KEY,
  provedor     text NOT NULL CHECK (provedor IN ('jev','anthropic')),
  nome         text NOT NULL,
  versao_fixa  text NOT NULL,
  parametros   jsonb,
  ativo        boolean NOT NULL DEFAULT true
);

CREATE TABLE core.item (
  item_id       text PRIMARY KEY,          -- sha256(source_id || url_canonica)
  source_id     text NOT NULL REFERENCES core.source,
  raw_id        uuid NOT NULL REFERENCES core.raw_item,
  publicado_em  timestamptz NOT NULL,
  coletado_em   timestamptz NOT NULL,
  idioma        text,
  texto         text NOT NULL,
  texto_hash    text NOT NULL,
  autor_hash    text,                      -- HMAC-SHA256, nunca o identificador
  dedupe_grupo  text,
  metricas      jsonb
);
CREATE INDEX ON core.item (source_id, publicado_em);
CREATE INDEX ON core.item (dedupe_grupo);

CREATE TABLE core.label (
  label_id    uuid PRIMARY KEY,
  item_id     text NOT NULL REFERENCES core.item,
  texto_hash  text NOT NULL,
  pergunta    text NOT NULL CHECK (pergunta IN ('relevante','tema','marca','sentimento')),
  resposta    text NOT NULL,
  prob        jsonb,
  confianca   real CHECK (confianca BETWEEN 0 AND 1),
  origem      text NOT NULL CHECK (origem IN ('jev','claude','humano')),
  modelo_id   integer REFERENCES core.model_version,
  criado_em   timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX ON core.label (item_id, pergunta, criado_em DESC);

-- resposta vigente: humano primeiro, depois a mais recente sobre o texto atual
CREATE VIEW core.label_current AS
SELECT DISTINCT ON (l.item_id, l.pergunta) l.*
FROM core.label l
JOIN core.item i ON i.item_id = l.item_id AND i.texto_hash = l.texto_hash
ORDER BY l.item_id, l.pergunta, (l.origem = 'humano') DESC, l.criado_em DESC;

CREATE TABLE analytics.series_point (
  dia               date NOT NULL,
  tema_id           integer NOT NULL REFERENCES core.taxonomy,
  marca_id          integer REFERENCES core.taxonomy,
  source_id         text NOT NULL REFERENCES core.source,
  volume            integer NOT NULL,
  share             real NOT NULL,
  sentimento_medio  real,
  engajamento       bigint,
  cobertura         real NOT NULL CHECK (cobertura BETWEEN 0 AND 1)
);
-- marca_id pode ser nulo, então a unicidade usa COALESCE
CREATE UNIQUE INDEX ON analytics.series_point (dia, tema_id, COALESCE(marca_id, 0), source_id);

CREATE TABLE analytics.signal (
  signal_id        uuid PRIMARY KEY,
  tipo             text NOT NULL
                   CHECK (tipo IN ('pico','vale','patamar','emergencia','divergencia')),
  escopo           jsonb NOT NULL,
  periodo          daterange NOT NULL,
  magnitude        real,
  z_robusto        real,
  itens_distintos  integer NOT NULL,
  cobertura_ok     boolean NOT NULL,
  prioridade       real,
  metodo_versao    text NOT NULL,
  criado_em        timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE analytics.insight (
  insight_id    uuid PRIMARY KEY,
  nivel         text NOT NULL CHECK (nivel IN ('N3','N4','N5')),
  escopo        jsonb NOT NULL,
  texto         text NOT NULL,
  saida_json    jsonb NOT NULL,
  payload_hash  text NOT NULL,
  confianca     text NOT NULL CHECK (confianca IN ('baixa','media','alta')),
  status        text NOT NULL DEFAULT 'rascunho'
                CHECK (status IN ('rascunho','revisado','publicado','obsoleto')),
  modelo_id     integer NOT NULL REFERENCES core.model_version,
  prompt_hash   text NOT NULL,
  criado_em     timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE analytics.insight_evidence (
  insight_id  uuid NOT NULL REFERENCES analytics.insight,
  tipo        text NOT NULL CHECK (tipo IN ('signal','series_point','item','insight')),
  ref_id      text NOT NULL,
  papel       text NOT NULL CHECK (papel IN ('base','exemplo','contraexemplo')),
  PRIMARY KEY (insight_id, tipo, ref_id)
);
