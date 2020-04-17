from pathlib import Path

from setuptools import setup, find_namespace_packages

requirements = [
    p
    for p in Path("requirements.txt").read_text().strip().split("\n")
    if "github" not in p
]

# this is a namespace package for `docassemble`, see:
# https://packaging.python.org/guides/packaging-namespace-packages/
setup(
    name="docassemble-sarkui",
    version="0.1.dev0",
    description="A Q&A driven UI for SENTINEL archive",
    install_requires=requirements,
    packages=find_namespace_packages(
        include=["docassemble.*"], exclude=["doc", "tests"],
    ),
    package_data={"docassemble.sarkui": ["data/*"]},
)
