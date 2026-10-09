"""Atalhos de desenvolvimento (``pip install -e ".[dev]"`` e depois ``invoke --list``)."""

import shutil

from invoke import task


@task
def clean(c):
    """Remove arquivos gerados pela build anterior"""
    for pasta in ("build", "dist", ".pytest_cache", ".mypy_cache", ".ruff_cache", "htmlcov"):
        shutil.rmtree(pasta, ignore_errors=True)
    print("Arquivos de build removidos.")


@task
def lint(c):
    """Roda ruff (lint e formatação) e mypy"""
    c.run("ruff check .")
    c.run("ruff format --check .")
    c.run("mypy")


@task
def test(c):
    """Executa os testes com cobertura"""
    c.run("pytest --cov")


@task(pre=[clean])
def build(c):
    """Constrói o sdist e o wheel e confere os metadados"""
    c.run("python -m build")
    c.run("twine check --strict dist/*")


@task(pre=[lint, test, build])
def check(c):
    """Roda tudo o que o CI roda"""
    print("Tudo certo.")
