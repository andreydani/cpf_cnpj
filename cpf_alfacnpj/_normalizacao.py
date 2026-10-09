"""Normalização de entradas compartilhada pelos validadores."""

from __future__ import annotations

import re
from typing import Optional

# Únicos caracteres de máscara aceitos: ponto, hífen, barra e espaços.
_SEPARADORES = re.compile(r"[.\-/\s]")


def normalizar(valor: object) -> Optional[str]:
    """
    Remove a máscara e converte para maiúsculas.

    Retorna ``None`` quando a entrada não é ``str`` ou contém caracteres
    fora do ASCII (por exemplo ``"²"`` ou ``"Ç"``), que nunca fazem parte
    de um CPF ou CNPJ.
    """
    if not isinstance(valor, str):
        return None
    limpo = _SEPARADORES.sub("", valor)
    if not limpo.isascii():
        return None
    return limpo.upper()
