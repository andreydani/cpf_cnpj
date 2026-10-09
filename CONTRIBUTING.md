# Contribuindo

Obrigado pelo interesse em contribuir! Bugs, sugestões e pull requests são bem-vindos.

## Ambiente de desenvolvimento

```bash
git clone https://github.com/andreydani/cpf_cnpj.git
cd cpf_cnpj
python -m venv .venv
source .venv/bin/activate          # no Windows: .venv\Scripts\activate
pip install -e ".[dev,pydantic,django]"
pre-commit install
```

## Antes de abrir um pull request

```bash
ruff check .            # lint
ruff format .           # formatação
mypy                    # tipagem (modo strict)
pytest --cov            # testes, doctests e cobertura (o núcleo exige 100%)
```

Ou tudo de uma vez, com `invoke check`.

Algumas regras do projeto:

- O núcleo (`cpf_alfacnpj/`, fora de `contrib/`) não pode ter dependências externas.
- Os validadores (`validar_*`) nunca lançam exceção: entrada inválida retorna `False`.
- Toda correção de bug vem acompanhada de um teste que falharia sem ela.
- Toda mudança visível para o usuário entra no [CHANGELOG.md](CHANGELOG.md), na seção "Unreleased".

## Lançando uma versão

1. Atualize `__version__` em `cpf_alfacnpj/__init__.py` e mova as entradas do CHANGELOG para a nova
   versão.
2. Faça o merge na `main` com o CI verde.
3. Crie um release no GitHub com a tag `vX.Y.Z` (igual a `__version__`). O workflow
   `publish.yml` testa, constrói e publica no PyPI via Trusted Publishing.
