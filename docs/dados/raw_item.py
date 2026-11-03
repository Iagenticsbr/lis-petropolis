"""Contrato RawItem (referência).

Origem: Anexo B de docs/arquitetura/LIS-arquitetura-dados-e-motor-de-analise.pdf (Proposta v2, 03/11/2026).
Todo coletor, próprio ou Apify, devolve este objeto: é a única fronteira entre a coleta e o resto do pipeline.
Status: proposta. Quando for implementado, mora em src/lis/contracts/.
"""
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, HttpUrl

class RawItem(BaseModel):
    source_id: str
    run_id: str
    url: HttpUrl
    coletor: Literal["own_http", "own_js", "apify"]
    coletado_em: datetime
    publicado_em: datetime | None = None
    autor: str | None = None            # sai da normalização como autor_hash
    texto: str
    idioma_declarado: str | None = None
    metricas: dict[str, int] = {}
    payload_uri: str                    # onde o payload original foi gravado
