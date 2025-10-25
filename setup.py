from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="Hotel-reservation",
    version = "0.1",
    # 1. Corrected 'package' to 'packages'
    # 2. Added 'exclude' to ignore non-code folders
    packages=find_packages(exclude=['notebooks', 'logs', 'artifacts', 'config', 'tests*']), 
    
    # 3. Corrected 'installed_requires' to 'install_requires'
    install_requires = requirements, 
)