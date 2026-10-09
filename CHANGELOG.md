# Changelog

Todas as mudanças relevantes deste projeto são documentadas aqui.

O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e o projeto adota o
[Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2026-10-09

### BREAKING

- `validar_cnpj` passa a aceitar o **CNPJ alfanumérico por padrão**, já que o novo formato está em
  vigor. Para manter o comportamento antigo, use `validar_cnpj(valor, alfanumerico=False)`.
- **Normalização estrita:** só `.`, `-`, `/` e espaços são removidos como máscara. Qualquer outro
  caractere (letras no CPF, `_`, `:`, `!`, etc.) torna o documento inválido. Antes esses caracteres
  eram descartados em silêncio, e `"CPF: 111.444.777-35"` era aceito.
- Versão mínima do Python passa a ser a **3.9**.
- A função interna `validar_cnpj_base` foi removida.

### Added

- `limpar_cpf` e `limpar_cnpj`: retornam o documento sem máscara (e em maiúsculas).
- `formatar_cpf` e `formatar_cnpj`: aplicam a máscara padrão.
- `calcular_dv_cpf` e `calcular_dv_cnpj`: calculam os dígitos verificadores.
- `gerar_cpf` e `gerar_cnpj`: geram documentos válidos para testes (CNPJ numérico ou alfanumérico,
  com máscara opcional e escolha da filial).
- `tipo_documento` e `validar_documento`: detectam automaticamente se é CPF ou CNPJ.
- CLI `cpf-alfacnpj` com os comandos `validar` (com `--json` e leitura do stdin), `formatar` e
  `gerar`; também disponível via `python -m cpf_alfacnpj`.
- Integração com **Pydantic v2** (`cpf_alfacnpj.contrib.pydantic`): tipos `CPF`, `CNPJ` e
  `CNPJNumerico`. Extra `[pydantic]`.
- Integração com **Django** (`cpf_alfacnpj.contrib.django`): `CPFValidator`, `CNPJValidator` e os
  form fields `CPFField` e `CNPJField`. Extra `[django]`.
- `__version__`, `__all__` e marcador `py.typed`.

### Changed

- Empacotamento migrado de `setup.py` para `pyproject.toml` (hatchling).
- `validar_cnpj_alfanumerico` passa a ser um alias de `validar_cnpj`.
- CI testa do Python 3.9 ao 3.14 (Linux, Windows e macOS), com ruff, mypy `--strict`, 100% de
  cobertura e testes de propriedade (hypothesis).
- Publicação no PyPI via Trusted Publishing.

### Fixed

- O comando `cpf-alfacnpj` falhava porque apontava para um módulo inexistente.
- O wheel instalava um pacote `tests` no site-packages.
- Dígitos Unicode (como `²`) causavam `ValueError` em vez de retornar `False`.
- Letras fora do ASCII (como `Ç`) eram processadas no cálculo do CNPJ alfanumérico.
- Entradas que não são `str` (como `None`) causavam `TypeError` em vez de retornar `False`.

## [0.3.0] - 2024-06-23

### Added

- `validar_cpf`, `validar_cnpj` (numérico) e `validar_cnpj_alfanumerico`.

[1.0.0]: https://github.com/andreydani/cpf_cnpj/compare/v0.3.0...v1.0.0
[0.3.0]: https://github.com/andreydani/cpf_cnpj/releases/tag/v0.3.0
