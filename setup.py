from setuptools import find_packages, setup

setup(
    name="textwordcount",
    packages=find_packages(include=["textwordcount", "tests"]),
    version="0.1.0",
    description="A Python library to analyze text with nltk",
    author="Yitsy Mosqueda",
    install_requires=["nltk", "bs4"],
    setup_requires=["pytest-runner"],
    test_suite="tests"
)
