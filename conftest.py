import importlib.util

# As integrações dependem de extras opcionais; sem eles, não coleta os doctests desses módulos.
collect_ignore = [
    f"cpf_alfacnpj/contrib/{modulo}.py"
    for modulo in ("pydantic", "django")
    if importlib.util.find_spec(modulo) is None
]

if importlib.util.find_spec("django") is not None:
    import django
    from django.conf import settings

    if not settings.configured:
        settings.configure(USE_I18N=False)
        django.setup()
