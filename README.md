# cpf_alfacnpj

Biblioteca de validação de CPF e CNPJ - suporta o CNPJ alfanumérico (2026).

Veja no PyPI: https://pypi.org/project/cpf-alfacnpj/

[Nota técnica com o racional da mudança](NotaCocad20240549CNPJAlfa.pdf)

[Manual de cálculo divulgado pela RFB](https://www.gov.br/receitafederal/pt-br/centrais-de-conteudo/publicacoes/documentos-tecnicos/cnpj)

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
