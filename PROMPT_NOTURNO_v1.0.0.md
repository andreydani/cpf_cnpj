# Tarefa: lançar a v1.0.0 da biblioteca `cpf-alfacnpj`

Você vai trabalhar sozinho, sem supervisão, no repositório `andreydani/cpf_cnpj`
(publicado no PyPI como `cpf-alfacnpj`). De manhã o mantenedor vai revisar o
resultado e fazer o merge. Trabalhe com autonomia: quando surgir uma dúvida de
detalhe, escolha a opção mais conservadora, registre a escolha na descrição do
PR e siga em frente.

## Regras que não podem ser quebradas

- **NÃO** publique no PyPI, **NÃO** crie release ou tag e **NÃO** faça push na `main`.
- Trabalhe na branch designada pela sessão. Se você puder escolher, use `release/v1.0.0`.
- Termine abrindo **um PR em rascunho (draft) contra a `main`** e deixe o CI verde.
  Se o CI falhar, investigue a causa, corrija e faça push de novo até ficar verde.
- Não pule, desative ou marque como xfail nenhum teste só para o CI passar.
- Faça **um commit por bloco** (A, B, C, D, E abaixo), com mensagem descritiva em português.
- Não apague o arquivo `NotaCocad20240549CNPJAlfa.pdf` e não altere a `LICENSE`.

## Contexto

O código atual fica em `cpf_alfacnpj/` (`cpf.py`, `cnpj.py`, `__init__.py`), com
testes em unittest dentro de `tests/`. O empacotamento usa `setup.py`, e os
workflows estão em `.github/workflows/`. O CNPJ alfanumérico da Receita Federal
**já está em vigor**: a base tem 12 caracteres `[0-9A-Z]` e o DV tem 2 dígitos
numéricos. O cálculo usa o valor `ord(c) - 48` com pesos de módulo 11. Exemplo
oficial da RFB: `12.ABC.345/01DE-35`, que é válido.

Decisões que o mantenedor já tomou:
1. `validar_cnpj` passa a aceitar o CNPJ alfanumérico **por padrão**.
2. A versão nova é a **1.0.0**.
3. Entram as integrações com **Pydantic v2** e **Django**, como extras opcionais.
4. O suporte mínimo passa a ser **Python 3.9+**, e o CI testa do 3.9 ao 3.14.

---

## Bloco A: corrigir os bugs (com teste de regressão para cada um)

1. O entry point `cpf-alfacnpj = cpf_alfacnpj.main:main` aponta para um módulo
   que não existe. Isso vai ser resolvido no bloco B com a criação de `cpf_alfacnpj/__main__.py`
   ou de `cli.py`; ajuste o entry point para apontar para o módulo certo.
2. O wheel publica o pacote `tests` no site-packages. Ele não pode entrar na
   distribuição (confira com `python -m zipfile -l dist/*.whl`).
3. `validar_cpf("111.444.777-3²")` e o equivalente de CNPJ lançam `ValueError`,
   porque `str.isdigit` aceita dígitos Unicode. O resultado tem que ser `False`.
4. A limpeza do CNPJ alfanumérico (`cnpj[:-2]` cortado antes de remover a máscara)
   é frágil e aceita letras fora do ASCII.
5. Entrada que não é `str` (`None`, `int`, etc.) lança `TypeError`. Tem que
   retornar `False`. Para `int`, decida se converte com `zfill`; o mais
   conservador é retornar `False` e documentar a escolha.
6. Corrija as docstrings ("verificdor"; a docstring do `dv2` diz "dígito 1") e
   remova o caso de teste duplicado.

**Regra de normalização (vale para tudo):** remova somente `.`, `-`, `/` e
espaços em branco nas pontas e no meio. Se sobrar **qualquer outro caractere**,
a entrada é inválida e retorna `False`, sem descartar o caractere em silêncio.
Converta letras minúsculas para maiúsculas. Depois de limpo:
- CPF: `^[0-9]{11}$`
- CNPJ: `^[0-9A-Z]{12}[0-9]{2}$` (use regex ASCII: `re.ASCII` ou classes explícitas)
- Continue rejeitando sequências com todos os caracteres iguais.

## Bloco B: API pública da 1.0.0

Todas as funções em português, com type hints completos e docstrings com exemplo
(que serão testadas com doctest). Inclua o arquivo `cpf_alfacnpj/py.typed`.
Organize em módulos (`cpf.py`, `cnpj.py`, `documento.py`, `gerador.py`, `cli.py`)
e exporte tudo no `__init__.py`, com `__all__` e `__version__ = "1.0.0"`.

- `validar_cpf(valor) -> bool`
- `validar_cnpj(valor, *, alfanumerico: bool = True) -> bool`. Com
  `alfanumerico=False`, só aceita a base numérica.
- `validar_cnpj_alfanumerico(valor) -> bool`: manter como **alias compatível**
  (sem DeprecationWarning; só uma nota na docstring).
- `limpar_cpf(valor) -> str` e `limpar_cnpj(valor) -> str`: retornam a forma
  normalizada e lançam `ValueError` se a entrada tiver caracteres inválidos ou o
  tamanho errado. Não validam o DV.
- `formatar_cpf(valor) -> str` → `"111.444.777-35"`;
  `formatar_cnpj(valor) -> str` → `"12.ABC.345/01DE-35"`. Lançam `ValueError`
  se o documento for inválido.
- `calcular_dv_cpf(base9: str) -> str` e `calcular_dv_cnpj(base12: str) -> str`
  (retornam os 2 dígitos).
- `gerar_cpf(*, formatado: bool = False) -> str` e
  `gerar_cnpj(*, alfanumerico: bool = True, formatado: bool = False, filial: int | None = None) -> str`
  (`filial` define a ordem `0001`). Use `random` normal e documente que é para
  massa de testes. Nunca gere sequências repetidas.
- `validar_documento(valor) -> bool` e
  `tipo_documento(valor) -> Literal["CPF", "CNPJ"] | None`: detectam pelo tamanho
  depois da limpeza.

**Compatibilidade:** todo uso válido da 0.3.0 tem que continuar funcionando. A única
mudança de comportamento intencional é o `validar_cnpj` aceitar letras, que vai
documentada no CHANGELOG como **BREAKING**, junto com a normalização estrita. Para
manter compatibilidade com 3.9, use `from __future__ import annotations` e
`Optional`/`Union` onde precisar em runtime.

**CLI** (`argparse`, sem dependências, entry point `cpf-alfacnpj` e também
`python -m cpf_alfacnpj`):
```
cpf-alfacnpj validar 111.444.777-35 12.ABC.345/01DE-35   # uma linha por item: "<valor>\tVÁLIDO|INVÁLIDO\t<tipo>"
cpf-alfacnpj validar -          # lê um documento por linha do stdin
cpf-alfacnpj formatar 12abc34501de35
cpf-alfacnpj gerar cnpj --quantidade 5 --formatado [--numerico]
cpf-alfacnpj gerar cpf
cpf-alfacnpj --version
```
Código de saída: 0 se tudo for válido, 1 se algum item for inválido, 2 para erro
de uso. Inclua a opção `--json` no `validar`.

## Bloco C: integrações opcionais

Ficam em `cpf_alfacnpj/contrib/`. O import da biblioteca principal **nunca** pode
exigir pydantic ou django.

- **Pydantic v2** (`cpf_alfacnpj.contrib.pydantic`, extra `[pydantic]`):
  tipos `CPF`, `CNPJ` e `CNPJNumerico` via `Annotated[str, AfterValidator(...)]`,
  que normalizam (salvam a forma limpa) e geram erro claro em português.
  Inclua um exemplo com `BaseModel` no README.
- **Django** (`cpf_alfacnpj.contrib.django`, extra `[django]`):
  validators `validar_cpf_django`/`CPFValidator` e `CNPJValidator(alfanumerico=True)`
  com `@deconstructible` (para funcionar em migrations), levantando
  `ValidationError` com `code`. Inclua os form fields `CPFField` e `CNPJField`
  (derivados de `forms.CharField`, que limpam o valor). Model fields ficam fora.
- Os testes das integrações usam `pytest.importorskip`. No CI, um job com os
  extras instalados roda esses testes (Django com `settings.configure()` mínimo
  num conftest).

## Bloco D: empacotamento, qualidade e CI

- Troque `setup.py` por **`pyproject.toml`** (backend `hatchling`), com:
  `name = "cpf-alfacnpj"`, versão dinâmica lida de `__version__`,
  `requires-python = ">=3.9"`, `license = "MIT"`, `readme = "README.md"`,
  `keywords` (cpf, cnpj, cnpj alfanumérico, validação, receita federal, brasil,
  documentos, pydantic, django), classifiers (`Development Status :: 5 - Production/Stable`,
  todas as versões de 3.9 a 3.14, `Natural Language :: Portuguese (Brazilian)`,
  `Typing :: Typed`, `Intended Audience :: Developers`, `Topic :: Software Development :: Libraries`),
  `[project.urls]` (Homepage, Source, Issues, Changelog), `[project.scripts]` e
  `[project.optional-dependencies]` (`pydantic`, `django`, `dev`).
  Garanta que o sdist e o wheel **não** incluam `tests/` como pacote, nem o PDF
  ou outros arquivos de desenvolvimento no wheel.
- Remova o `setup.py` e o `requirements_dev.txt` (as dependências de dev vão no
  extra `[dev]`). Atualize o `tasks.py` para usar `python -m build`, `pytest` e
  `ruff`; se não fizer sentido manter, remova e documente os comandos no
  CONTRIBUTING.
- Ferramentas: **ruff** (lint + format), **mypy --strict** no pacote, **pytest**
  com **pytest-cov** (meta de 100% de linhas no núcleo, excluindo `contrib`) e
  **hypothesis** com testes de propriedade:
  - tudo que `gerar_*` produz passa no `validar_*`;
  - `formatar(limpar(x))` é idempotente;
  - trocar um único caractere de um documento válido o torna inválido (pelo
    menos para dígitos do DV);
  - nenhuma string arbitrária faz o validador lançar exceção.
  Migre os testes atuais para pytest parametrizado, preservando todos os casos.
  Inclua o exemplo oficial `12.ABC.345/01DE-35`.
- Adicione `.pre-commit-config.yaml` (ruff, ruff-format, end-of-file e trailing-whitespace).
- **CI** (`.github/workflows/ci.yml`, substituindo o `python-package.yml`): roda
  em push/PR para a `main`; matriz Python 3.9 a 3.14 em ubuntu, mais um job
  windows e um macos no 3.12; passos: ruff check, ruff format --check, mypy,
  pytest com cobertura, `python -m build`, `twine check dist/*` e um teste de
  instalação do wheel num venv limpo, chamando `cpf-alfacnpj --version`. Inclua
  um job separado com os extras pydantic e django. Use as versões atuais das
  actions (`actions/checkout@v4`, `actions/setup-python@v5`).
- **Publicação** (`publish.yml`): dispara em `release: published`; builda,
  testa e publica via **PyPI Trusted Publishing** (`permissions: id-token: write`,
  `environment: pypi`, `pypa/gh-action-pypi-publish@release/v1`, sem token).
  Verifique se a tag do release (`v1.0.0`) bate com `__version__`; se não bater,
  o job falha.

## Bloco E: documentação e visibilidade

- **README.md** reescrito (em português, com uma seção curta "English" no final):
  - título e uma frase de valor; badges (PyPI version, Python versions, downloads
    via pepy.tech, CI, licença, "typed");
  - "Por que esta biblioteca": suporte ao CNPJ alfanumérico da RFB (já em vigor),
    zero dependências, tipada, com CLI e integrações;
  - instalação (`pip install cpf-alfacnpj`, `pip install "cpf-alfacnpj[pydantic]"`);
  - uso rápido com exemplos de cada função, da CLI, do Pydantic e do Django;
  - "Como o cálculo funciona" (tabela `ord(c) - 48`, pesos, exemplo do DV feito
    passo a passo com `12ABC34501DE`), com links para a nota técnica (PDF) e o
    manual da RFB que já estão no README atual;
  - "Migrando da 0.x" (as breaking changes);
  - links para Contribuição e Changelog.
- **CHANGELOG.md** no formato Keep a Changelog, com as seções 1.0.0 (Added /
  Changed / Fixed / **BREAKING**) e um resumo da 0.3.0.
- **CONTRIBUTING.md** curto (setup do ambiente, testes, lint, como lançar uma versão).
- `.github/ISSUE_TEMPLATE/` (bug e feature) e `.github/pull_request_template.md`.
- Confira que o README renderiza bem no PyPI (`twine check` sem avisos).

---

## Validação antes de cada push

Rode localmente e só faça push com tudo verde:
```
pip install -e ".[dev,pydantic,django]"
ruff check . && ruff format --check .
mypy cpf_alfacnpj
pytest --cov=cpf_alfacnpj --doctest-modules cpf_alfacnpj tests
python -m build && twine check dist/*
# wheel num venv limpo:
python -m venv /tmp/v && /tmp/v/bin/pip install dist/*.whl && /tmp/v/bin/cpf-alfacnpj validar 12.ABC.345/01DE-35
python -m zipfile -l dist/*.whl   # sem tests/, sem PDF
```
Teste também com o Python 3.9 se estiver disponível (por exemplo, via `uv python install 3.9`).
Antes do push final, releia o diff inteiro com olhar crítico.

## Entrega final

1. Abra o PR draft contra a `main` com o título **"Release v1.0.0: CNPJ alfanumérico por padrão, nova API, CLI e integrações"**.
2. A descrição do PR deve trazer:
   - um resumo por bloco (A a E);
   - **as breaking changes** com exemplos de antes e depois;
   - as decisões que você tomou sozinho e o motivo;
   - um **checklist manual para o mantenedor**:
     - [ ] Configurar o Trusted Publisher no PyPI (projeto `cpf-alfacnpj`,
       repositório `andreydani/cpf_cnpj`, workflow `publish.yml`, environment `pypi`)
       e criar o environment `pypi` no GitHub
     - [ ] Remover o secret `PYPI_API_TOKEN` depois da primeira publicação bem-sucedida
     - [ ] Fazer o merge, criar o release `v1.0.0` no GitHub (isso publica no PyPI)
     - [ ] Adicionar os topics do repositório: `cpf`, `cnpj`, `cnpj-alfanumerico`, `python`,
       `validacao`, `receita-federal`, `brasil`, `pydantic`, `django`
     - [ ] Atualizar a descrição do repositório no GitHub
3. Num **comentário separado no PR** (não no repositório), deixe os rascunhos de divulgação:
   um post para o TabNews/dev.to (cerca de 400 palavras, explicando o CNPJ alfanumérico e mostrando
   exemplos), um post curto para o LinkedIn e o texto de um PR para a lista
   awesome-python-brasil (ou equivalente).
4. Espere o CI terminar e corrija o que falhar até ficar verde.
