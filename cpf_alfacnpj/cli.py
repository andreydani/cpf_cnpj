"""Interface de linha de comando: ``cpf-alfacnpj`` ou ``python -m cpf_alfacnpj``."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Iterable, Iterator, Sequence

from . import __version__
from .cnpj import formatar_cnpj
from .cpf import formatar_cpf
from .documento import tipo_documento, validar_documento
from .gerador import gerar_cnpj, gerar_cpf


def _valores(argumentos: Iterable[str]) -> Iterator[str]:
    for arg in argumentos:
        if arg == "-":
            for linha in sys.stdin:
                linha = linha.strip()
                if linha:
                    yield linha
        else:
            yield arg


def _validar(args: argparse.Namespace) -> int:
    resultados = [
        {"valor": v, "valido": validar_documento(v), "tipo": tipo_documento(v)}
        for v in _valores(args.valores)
    ]
    if args.json:
        print(json.dumps(resultados, ensure_ascii=False))
    else:
        for r in resultados:
            status = "VÁLIDO" if r["valido"] else "INVÁLIDO"
            print(f"{r['valor']}\t{status}\t{r['tipo'] or '-'}")
    return 0 if all(r["valido"] for r in resultados) else 1


def _formatar(args: argparse.Namespace) -> int:
    codigo = 0
    for valor in _valores(args.valores):
        tipo = tipo_documento(valor)
        try:
            if tipo == "CPF":
                print(formatar_cpf(valor))
            elif tipo == "CNPJ":
                print(formatar_cnpj(valor))
            else:
                raise ValueError(f"documento não reconhecido: {valor!r}")
        except ValueError as erro:
            print(f"erro: {erro}", file=sys.stderr)
            codigo = 1
    return codigo


def _gerar(args: argparse.Namespace) -> int:
    for _ in range(args.quantidade):
        if args.tipo == "cpf":
            print(gerar_cpf(formatado=args.formatado))
        else:
            print(gerar_cnpj(alfanumerico=not args.numerico, formatado=args.formatado))
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cpf-alfacnpj",
        description="Valida, formata e gera CPF e CNPJ (inclusive o CNPJ alfanumérico).",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="comando", required=True)

    validar = sub.add_parser("validar", help="valida CPFs e CNPJs ('-' lê do stdin)")
    validar.add_argument("valores", nargs="+", metavar="DOCUMENTO")
    validar.add_argument("--json", action="store_true", help="saída em JSON")
    validar.set_defaults(func=_validar)

    formatar = sub.add_parser("formatar", help="formata CPFs e CNPJs ('-' lê do stdin)")
    formatar.add_argument("valores", nargs="+", metavar="DOCUMENTO")
    formatar.set_defaults(func=_formatar)

    gerar = sub.add_parser("gerar", help="gera documentos válidos para testes")
    gerar.add_argument("tipo", choices=["cpf", "cnpj"])
    gerar.add_argument("-n", "--quantidade", type=int, default=1)
    gerar.add_argument("--formatado", action="store_true", help="aplica a máscara")
    gerar.add_argument("--numerico", action="store_true", help="CNPJ só com números")
    gerar.set_defaults(func=_gerar)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    codigo: int = args.func(args)
    return codigo


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
