# setup.py
from setuptools import setup, find_packages

setup(
    name="cpf_alfacnpj",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'cpf-alfacnpj=cpf_alfacnpj.main:main',
        ],
    },
    author="Andrey Sant'Anna",
    author_email="andreysantanna@gmail.com",
    description="Biblioteca de validação de CPF e CNPJ, inclusive com suporte ao CNPJ alfanumérico (2026)",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/andreydani/cpf_cnpj",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
