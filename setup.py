from setuptools import setup, find_packages

setup(
    name="dialog2rasa",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "dialog2rasa=dialog2rasa.converter:main",
        ],
    },
)
