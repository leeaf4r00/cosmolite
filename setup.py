from setuptools import setup, find_packages

setup(
    name="cosmolite",
    version="1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Pillow",
        "PySimpleGUI",
        "sqlite3"
    ],
    entry_points={
        "console_scripts": [
            "cosmolite = cosmolite.janela_principal.janela_principal:main"
        ]
    },
)
