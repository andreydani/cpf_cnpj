from typing import Callable


def calcular_dv1(cnpj: str) -> int:
    """
    Calculo do dígito verificdor 1, já preparado
    para lidar com CNPJ alfanumérico
    :param cnpj:
    :return:
    """
    pesos1: list[int] = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma: int = sum((ord(cnpj[i]) - 48) * pesos1[i] for i in range(12))
    dv1: int = 11 - (soma % 11)
    return 0 if dv1 >= 10 else dv1


def calcular_dv2(cnpj: str) -> int:
    """
    Calculo do dígito verificdor 1, já preparado
    para lidar com CNPJ alfanumérico
    :param cnpj:
    :return:
    """
    pesos2: list[int] = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum((ord(cnpj[i]) - 48) * pesos2[i] for i in range(13))
    dv2: int = 11 - (soma % 11)
    return 0 if dv2 >= 10 else dv2


def validar_cnpj_base(cnpj: str, limpa: Callable[[str], str]) -> bool:
    # Remove caracteres não numéricos
    cnpj: str = limpa(cnpj)

    # Verifica se o CNPJ tem 14 caracteres
    if len(cnpj) != 14:
        return False

    # Verifica se todos os caracteres são iguais
    if cnpj == cnpj[0] * 14:
        return False

    # Validação do primeiro dígito verificador
    dv1: int = calcular_dv1(cnpj)
    if int(cnpj[12]) != dv1:
        return False

    # Validação do segundo dígito verificador
    dv2: int = calcular_dv2(cnpj)
    if int(cnpj[13]) != dv2:
        return False

    return True


def validar_cnpj(cnpj: str) -> bool:
    return validar_cnpj_base(
        cnpj,
        lambda cnpj: ''.join(filter(str.isdigit, cnpj))
    )


def validar_cnpj_alfanumerico(cnpj: str) -> bool:
    return validar_cnpj_base(
        cnpj,
        lambda cnpj: ''.join(filter(str.isalnum, cnpj[:-2])).upper() +
                     ''.join(filter(str.isdigit, cnpj[-2:]))
    )
