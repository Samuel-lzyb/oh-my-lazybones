from setuptools import setup, find_packages
setup(
    name="oh-my-lazybones",
    version="0.2.1",
    packages=find_packages(),
    install_requires=["typer", "httpx", "pyyaml"],
    entry_points={
        "console_scripts": ["lazy=lazybones.main:main"],
    },
)
