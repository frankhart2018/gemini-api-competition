# Write a basic setup.py for a shared library

from setuptools import setup, find_packages

setup(
    name="persona_sync_pylib",
    version="0.1",
    packages=find_packages(),
    install_requires=["pika==1.3.2", "pymongo>=4.7.0", "pydantic==2.7.1"],
)
