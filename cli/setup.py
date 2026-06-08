from setuptools import setup, find_packages
setup(
    name="oh-my-lazybones",
    version="0.4.0",
    packages=find_packages(),
    install_requires=["typer", "httpx", "pyyaml"],
    entry_points={
        "console_scripts": ["lazy=lazybones.main:main"],
    },
)
