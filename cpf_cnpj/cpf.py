def calcular_dv1(cpf: str) -> int:
    soma: int = sum(int(cpf[i]) * (10 - i) for i in range(9))
    return (soma * 10 % 11) % 10


def calcular_dv2(cpf: str) -> int:
    soma: int = sum(int(cpf[i]) * (11 - i) for i in range(10))
    return (soma * 10 % 11) % 10


def validar_cpf(cpf: str) -> bool:
    # Remove caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))

    # Verifica se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return False

    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False

    # Validação do primeiro dígito verificador
    dv1: int = calcular_dv1(cpf)
    if int(cpf[9]) != dv1:
        return False

    # Validação do segundo dígito verificador
    dv2: int = calcular_dv2(cpf)
    if int(cpf[10]) != dv2:
        return False

    return True
