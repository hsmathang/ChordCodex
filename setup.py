from setuptools import setup, find_packages

# Function to read requirements.txt
def read_requirements():
    with open("requirements.txt") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="chordcodex",
    version="0.1.0",
    author="MachineMindCore",
    author_email="machine.mind.core@gmail.com",
    description="ChordCodex project specific package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MachineMindCore/chordcodex",
    packages=find_packages(),
    install_requires=read_requirements(),  # Load dependencies from requirements.txt
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
