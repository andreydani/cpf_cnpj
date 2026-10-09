import io
import json
import subprocess
import sys

import pytest

from cpf_alfacnpj import __version__, validar_cnpj, validar_cpf
from cpf_alfacnpj.cli import main


def test_validar_todos_validos(capsys):
    assert main(["validar", "111.444.777-35", "12.ABC.345/01DE-35"]) == 0
    saida = capsys.readouterr().out.splitlines()
    assert saida == ["111.444.777-35\tVÁLIDO\tCPF", "12.ABC.345/01DE-35\tVÁLIDO\tCNPJ"]


def test_validar_algum_invalido(capsys):
    assert main(["validar", "111.444.777-35", "123"]) == 1
    assert capsys.readouterr().out.splitlines()[1] == "123\tINVÁLIDO\t-"


def test_validar_json(capsys):
    assert main(["validar", "--json", "111.444.777-36"]) == 1
    assert json.loads(capsys.readouterr().out) == [
        {"valor": "111.444.777-36", "valido": False, "tipo": "CPF"}
    ]


def test_validar_stdin(capsys, monkeypatch):
    monkeypatch.setattr(sys, "stdin", io.StringIO("111.444.777-35\n\n12ABC34501DE35\n"))
    assert main(["validar", "-"]) == 0
    assert len(capsys.readouterr().out.splitlines()) == 2


def test_formatar(capsys):
    assert main(["formatar", "12abc34501de35", "11144477735"]) == 0
    assert capsys.readouterr().out.splitlines() == ["12.ABC.345/01DE-35", "111.444.777-35"]


def test_formatar_invalido(capsys):
    assert main(["formatar", "123", "11144477736", "11144477735"]) == 1
    capturado = capsys.readouterr()
    assert capturado.out.splitlines() == ["111.444.777-35"]
    assert capturado.err.count("erro:") == 2


def test_gerar(capsys):
    assert main(["gerar", "cpf", "-n", "3"]) == 0
    cpfs = capsys.readouterr().out.split()
    assert len(cpfs) == 3 and all(map(validar_cpf, cpfs))

    assert main(["gerar", "cnpj", "--quantidade", "2", "--formatado", "--numerico"]) == 0
    cnpjs = capsys.readouterr().out.split()
    assert len(cnpjs) == 2 and all(validar_cnpj(c, alfanumerico=False) for c in cnpjs)
    assert all("/" in c for c in cnpjs)


def test_versao(capsys):
    with pytest.raises(SystemExit) as saida:
        main(["--version"])
    assert saida.value.code == 0
    assert __version__ in capsys.readouterr().out


def test_erro_de_uso():
    with pytest.raises(SystemExit) as saida:
        main([])
    assert saida.value.code == 2


def test_python_m():
    resultado = subprocess.run(
        [sys.executable, "-m", "cpf_alfacnpj", "validar", "12.ABC.345/01DE-35"],
        capture_output=True,
        text=True,
    )
    assert resultado.returncode == 0
    assert "VÁLIDO" in resultado.stdout
