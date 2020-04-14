from pathlib import Path

from setuptools import setup, find_namespace_packages

requirements = Path("requirements.txt").read_text().strip().split("\n")

# this is a namespace package for `docassemble`, see:
# https://packaging.python.org/guides/packaging-namespace-packages/
setup(
    name="docassemble-sarkui",
    install_requires=requirements,
    packages=find_namespace_packages(include=["docassemble.*"]),
    package_data={"docassemble.sarkui": ["data/*"]},
)
