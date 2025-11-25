from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="Hotel-reservation",
    version = "0.1",
    packages=find_packages(exclude=['notebooks', 'logs', 'artifacts', 'config', 'tests*']), 
    install_requires = requirements, 
)