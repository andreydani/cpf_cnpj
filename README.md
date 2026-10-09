# cpf-alfacnpj

[![PyPI](https://img.shields.io/pypi/v/cpf-alfacnpj)](https://pypi.org/project/cpf-alfacnpj/)
[![Python](https://img.shields.io/pypi/pyversions/cpf-alfacnpj)](https://pypi.org/project/cpf-alfacnpj/)
[![Downloads](https://static.pepy.tech/badge/cpf-alfacnpj/month)](https://pepy.tech/project/cpf-alfacnpj)
[![CI](https://github.com/andreydani/cpf_cnpj/actions/workflows/ci.yml/badge.svg)](https://github.com/andreydani/cpf_cnpj/actions/workflows/ci.yml)
[![Licença: MIT](https://img.shields.io/badge/licen%C3%A7a-MIT-blue)](https://github.com/andreydani/cpf_cnpj/blob/main/LICENSE)
[![Tipado: mypy](https://img.shields.io/badge/tipado-mypy%20strict-2a6db2)](https://mypy-lang.org/)

Validação, formatação e geração de **CPF** e **CNPJ** em Python, com suporte completo ao
**CNPJ alfanumérico** da Receita Federal.

```python
>>> from cpf_alfacnpj import validar_cnpj
>>> validar_cnpj("12.ABC.345/01DE-35")
True
```

## Por que esta biblioteca

- **CNPJ alfanumérico por padrão.** A partir de julho de 2026 a Receita Federal passou a emitir CNPJs
  com letras na raiz e na ordem (IN RFB nº 2.229/2024). Validadores que só aceitam números
  passam a recusar empresas reais. Aqui, `validar_cnpj` já aceita os dois formatos.
- **Sem dependências.** Só a biblioteca padrão do Python 3.9+.
- **Tipada** (`py.typed`, checada com `mypy --strict`) e com 100% de cobertura de testes.
- **Validadores que não quebram.** Entradas inválidas (`None`, números, caracteres estranhos) retornam
  `False` em vez de lançar exceção.
- **Pronta para usar:** CLI, gerador de documentos para testes e integrações com **Pydantic** e **Django**.

## Instalação

```bash
pip install cpf-alfacnpj

# com as integrações opcionais
pip install "cpf-alfacnpj[pydantic]"
pip install "cpf-alfacnpj[django]"
```

## Uso

### Validar

```python
from cpf_alfacnpj import validar_cpf, validar_cnpj, validar_documento

validar_cpf("111.444.777-35")  # True
validar_cpf("11144477735")  # True (com ou sem máscara)
validar_cnpj("12.ABC.345/01DE-35")  # True (alfanumérico)
validar_cnpj("04.252.011/0001-10")  # True (numérico)
validar_cnpj("12.ABC.345/01DE-35", alfanumerico=False)  # False (exige só números)
validar_documento("111.444.777-35")  # True (detecta CPF ou CNPJ)
validar_cpf(None)  # False, sem exceção
```

A máscara pode usar `.`, `-`, `/` e espaços, e letras minúsculas são aceitas. Qualquer outro
caractere torna o documento inválido.

### Limpar, formatar e identificar

```python
from cpf_alfacnpj import formatar_cnpj, formatar_cpf, limpar_cnpj, tipo_documento

limpar_cnpj("12.abc.345/01de-35")  # '12ABC34501DE35'
formatar_cpf("11144477735")  # '111.444.777-35'
formatar_cnpj("12abc34501de35")  # '12.ABC.345/01DE-35'
tipo_documento("111.444.777-35")  # 'CPF'
```

`limpar_*` e `formatar_*` lançam `ValueError` quando a entrada é inválida. `limpar_*` só confere o
formato; `formatar_*` também confere os dígitos verificadores.

### Calcular dígitos verificadores

```python
from cpf_alfacnpj import calcular_dv_cnpj, calcular_dv_cpf

calcular_dv_cpf("111444777")  # '35'
calcular_dv_cnpj("12ABC34501DE")  # '35'
```

### Gerar documentos para testes

```python
from cpf_alfacnpj import gerar_cnpj, gerar_cpf

gerar_cpf()  # '52998224725'
gerar_cpf(formatado=True)  # '529.982.247-25'
gerar_cnpj()  # 'Q0Z7AH9E000169' (alfanumérico)
gerar_cnpj(alfanumerico=False, filial=2)  # '41837562000252'
gerar_cnpj(formatado=True)  # '41.B8Y.EHE/0001-85'
```

Os números são aleatórios e servem para massa de testes; não correspondem, necessariamente, a
pessoas ou empresas reais.

### Linha de comando

```console
$ cpf-alfacnpj validar 111.444.777-35 12.ABC.345/01DE-35 123
111.444.777-35	VÁLIDO	CPF
12.ABC.345/01DE-35	VÁLIDO	CNPJ
123	INVÁLIDO	-

$ cat documentos.txt | cpf-alfacnpj validar - --json
$ cpf-alfacnpj formatar 12abc34501de35
12.ABC.345/01DE-35
$ cpf-alfacnpj gerar cnpj --quantidade 3 --formatado
$ cpf-alfacnpj gerar cnpj --numerico
$ cpf-alfacnpj gerar cpf
```

O comando `validar` sai com código `0` se todos os documentos forem válidos e `1` caso contrário,
o que facilita o uso em scripts. Também funciona como `python -m cpf_alfacnpj`.

### Pydantic v2

```python
from pydantic import BaseModel
from cpf_alfacnpj.contrib.pydantic import CNPJ, CPF


class Cliente(BaseModel):
    cpf: CPF
    cnpj_empresa: CNPJ  # numérico ou alfanumérico


Cliente(cpf="111.444.777-35", cnpj_empresa="12.abc.345/01de-35")
# Cliente(cpf='11144477735', cnpj_empresa='12ABC34501DE35')
```

Os valores são guardados sem máscara. Documentos inválidos geram `ValidationError`. Use `CNPJNumerico`
para aceitar só CNPJs com base numérica.

### Django

```python
from django import forms
from django.db import models
from cpf_alfacnpj.contrib.django import CNPJField, CNPJValidator, CPFField, validar_cpf_django


class Empresa(models.Model):
    cnpj = models.CharField(max_length=18, validators=[CNPJValidator()])
    cpf_responsavel = models.CharField(max_length=14, validators=[validar_cpf_django])


class EmpresaForm(forms.Form):
    cnpj = CNPJField()  # devolve '12ABC34501DE35'
    cpf_responsavel = CPFField()
    cnpj_antigo = CNPJField(alfanumerico=False, required=False)
```

Os validators são `deconstructible` (funcionam em migrations) e usam os códigos de erro
`cpf_invalido` e `cnpj_invalido`.

## Como o cálculo funciona

O CNPJ tem 14 posições: 8 de raiz, 4 de ordem (filial) e 2 dígitos verificadores (DV). No CNPJ
alfanumérico, as 12 primeiras posições podem ter letras de `A` a `Z`; os dois DVs continuam
numéricos.

Cada caractere vale o seu código ASCII menos 48, então os dígitos mantêm o valor de sempre e o
cálculo do CNPJ numérico não muda:

| Caractere | `0`–`9` | `A` | `B` | `C` | … | `Z` |
|---|---|---|---|---|---|---|
| Valor | 0–9 | 17 | 18 | 19 | … | 42 |

Exemplo com a base `12ABC34501DE`:

| | 1 | 2 | A | B | C | 3 | 4 | 5 | 0 | 1 | D | E | 1º DV |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Valor | 1 | 2 | 17 | 18 | 19 | 3 | 4 | 5 | 0 | 1 | 20 | 21 | |
| Peso do 1º DV | 5 | 4 | 3 | 2 | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 | |
| Peso do 2º DV | 6 | 5 | 4 | 3 | 2 | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 |

1. **1º DV:** soma dos produtos = 459; 459 mod 11 = 8; DV = 11 − 8 = **3**.
2. **2º DV:** soma dos produtos (incluindo o 1º DV, com peso 2) = 424; 424 mod 11 = 6; DV = 11 − 6 = **5**.

Se o resto for 0 ou 1, o DV é 0. Resultado: `12.ABC.345/01DE-35`.

Referências:
- [Nota técnica com o racional da mudança](https://github.com/andreydani/cpf_cnpj/blob/main/NotaCocad20240549CNPJAlfa.pdf)
- [Manual de cálculo divulgado pela RFB](https://www.gov.br/receitafederal/pt-br/centrais-de-conteudo/publicacoes/documentos-tecnicos/cnpj)

## Migrando da 0.x

A 1.0.0 mantém os nomes da 0.x, mas muda alguns comportamentos:

| Situação | 0.3.0 | 1.0.0 |
|---|---|---|
| `validar_cnpj("12.ABC.345/01DE-35")` | `False` | `True`. Para manter o comportamento antigo, use `validar_cnpj(x, alfanumerico=False)` |
| `validar_cpf("CPF: 111.444.777-35")` | `True` (letras eram descartadas) | `False`: só `.`, `-`, `/` e espaços são aceitos como máscara |
| `validar_cpf("111.444.777-3²")` | `ValueError` | `False` |
| `validar_cpf(None)` | `TypeError` | `False` |
| Python | 3.6+ (declarado) | 3.9+ |

`validar_cnpj_alfanumerico` continua disponível como alias de `validar_cnpj`. A função interna
`validar_cnpj_base` foi removida. Os detalhes estão no [CHANGELOG](https://github.com/andreydani/cpf_cnpj/blob/main/CHANGELOG.md).

## Contribuindo

Contribuições são bem-vindas! Veja o [CONTRIBUTING.md](https://github.com/andreydani/cpf_cnpj/blob/main/CONTRIBUTING.md) e o [CHANGELOG](https://github.com/andreydani/cpf_cnpj/blob/main/CHANGELOG.md).

## English

**cpf-alfacnpj** validates, formats and generates Brazilian taxpayer IDs: **CPF** (individuals) and
**CNPJ** (companies), including the new **alphanumeric CNPJ** introduced by the Brazilian Federal
Revenue Service (Receita Federal) in July 2026. It has no dependencies, is fully typed and ships with
a CLI and optional Pydantic v2 and Django integrations.

```python
from cpf_alfacnpj import validar_cnpj, validar_cpf, formatar_cnpj, gerar_cnpj

validar_cnpj("12.ABC.345/01DE-35")  # True
validar_cpf("111.444.777-35")  # True
formatar_cnpj("12abc34501de35")  # '12.ABC.345/01DE-35'
gerar_cnpj()  # random valid alphanumeric CNPJ for tests
```

## Licença

[MIT](https://github.com/andreydani/cpf_cnpj/blob/main/LICENSE) © Andrey Sant'Anna
