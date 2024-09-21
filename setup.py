from setuptools import setup, find_packages

setup(
    name="midi_harmonic_analysis",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "music21",
    ],
    description="A library for analyzing musical scores using music21",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/e7mac/midi_harmonic_analysis",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
