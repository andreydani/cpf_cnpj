# cpf_alfacnpj

Biblioteca de validação de CPF e CNPJ, inclusive com suporte ao CNPJ alfanumérico (2026).

> [!CAUTION]
> Por favor, note que o cálculo está baseado na pouca documentação fornecida até junho de 2024.
> Ainda não foram fornecidos exemplos de CNPJs válidos para que seja possível testar completamente.

Veja no PyPI: https://pypi.org/project/cpf-alfacnpj/

## Instalação

Você pode instalar a biblioteca via pip:

```bash
pip install cpf-alfacnpj
```

## Uso em programas

```bash
>>> from cpf_alfacnpj import validar_cnpj_alfanumerico
>>> print(validar_cnpj_alfanumerico("AB.C4A.678/0001-60"))
True
```
