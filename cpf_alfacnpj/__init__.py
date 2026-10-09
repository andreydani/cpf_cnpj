"""Validação, formatação e geração de CPF e CNPJ, com suporte ao CNPJ alfanumérico."""

__version__ = "1.0.0"

from .cnpj import (
    calcular_dv_cnpj,
    formatar_cnpj,
    limpar_cnpj,
    validar_cnpj,
    validar_cnpj_alfanumerico,
)
from .cpf import calcular_dv_cpf, formatar_cpf, limpar_cpf, validar_cpf
from .documento import tipo_documento, validar_documento
from .gerador import gerar_cnpj, gerar_cpf

__all__ = [
    "__version__",
    "calcular_dv_cnpj",
    "calcular_dv_cpf",
    "formatar_cnpj",
    "formatar_cpf",
    "gerar_cnpj",
    "gerar_cpf",
    "limpar_cnpj",
    "limpar_cpf",
    "tipo_documento",
    "validar_cnpj",
    "validar_cnpj_alfanumerico",
    "validar_cpf",
    "validar_documento",
]
