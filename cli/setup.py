from setuptools import setup, find_packages
setup(
    name="lazybones",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["typer", "httpx", "pyyaml"],
    entry_points={
        "console_scripts": ["lazy=lazybones.main:main"],
    },
)