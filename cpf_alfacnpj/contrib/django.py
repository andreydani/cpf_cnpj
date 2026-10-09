"""
Validators e campos de formulário para Django (``pip install "cpf-alfacnpj[django]"``).

Em models::

    from django.db import models
    from cpf_alfacnpj.contrib.django import CNPJValidator, validar_cpf_django

    class Cliente(models.Model):
        cpf = models.CharField(max_length=14, validators=[validar_cpf_django])
        cnpj = models.CharField(max_length=18, validators=[CNPJValidator()])

Em forms::

    from django import forms
    from cpf_alfacnpj.contrib.django import CNPJField, CPFField

    class ClienteForm(forms.Form):
        cpf = CPFField()
        cnpj = CNPJField(alfanumerico=True)
"""

from __future__ import annotations

from typing import Any, Optional

from django import forms
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from ..cnpj import limpar_cnpj, validar_cnpj
from ..cpf import limpar_cpf, validar_cpf

__all__ = [
    "CNPJField",
    "CNPJValidator",
    "CPFField",
    "CPFValidator",
    "validar_cnpj_django",
    "validar_cpf_django",
]


@deconstructible
class CPFValidator:
    """Levanta ``ValidationError`` (code ``"cpf_invalido"``) se o valor não for um CPF válido."""

    message = _("CPF inválido.")
    code = "cpf_invalido"

    def __init__(self, message: Optional[str] = None, code: Optional[str] = None) -> None:
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value: Any) -> None:
        if not validar_cpf(value):
            raise ValidationError(self.message, code=self.code, params={"value": value})

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, CPFValidator)
            and self.message == other.message
            and self.code == other.code
        )

    def __hash__(self) -> int:
        return hash((CPFValidator, self.code))


@deconstructible
class CNPJValidator:
    """
    Levanta ``ValidationError`` (code ``"cnpj_invalido"``) se o valor não for um CNPJ válido.

    Aceita o CNPJ alfanumérico por padrão; use ``alfanumerico=False`` para exigir base numérica.
    """

    message = _("CNPJ inválido.")
    code = "cnpj_invalido"

    def __init__(
        self,
        alfanumerico: bool = True,
        message: Optional[str] = None,
        code: Optional[str] = None,
    ) -> None:
        self.alfanumerico = alfanumerico
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value: Any) -> None:
        if not validar_cnpj(value, alfanumerico=self.alfanumerico):
            raise ValidationError(self.message, code=self.code, params={"value": value})

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, CNPJValidator)
            and self.alfanumerico == other.alfanumerico
            and self.message == other.message
            and self.code == other.code
        )

    def __hash__(self) -> int:
        return hash((CNPJValidator, self.alfanumerico, self.code))


validar_cpf_django = CPFValidator()
validar_cnpj_django = CNPJValidator()


class CPFField(forms.CharField):
    """Campo de formulário que valida o CPF e devolve os 11 dígitos sem máscara."""

    default_validators = [validar_cpf_django]

    def clean(self, value: Any) -> Any:
        valor = super().clean(value)
        return limpar_cpf(valor) if valor else valor


class CNPJField(forms.CharField):
    """Campo de formulário que valida o CNPJ e devolve os 14 caracteres sem máscara."""

    def __init__(self, *, alfanumerico: bool = True, **kwargs: Any) -> None:
        self.default_validators = [CNPJValidator(alfanumerico=alfanumerico)]
        super().__init__(**kwargs)

    def clean(self, value: Any) -> Any:
        valor = super().clean(value)
        return limpar_cnpj(valor) if valor else valor
