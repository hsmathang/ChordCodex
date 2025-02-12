from setuptools import setup, find_packages

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
    install_requires=[
        "dotenv-python",
        "greenlet",
        "numpy",
        "pandas",
        "polars",
        "psycopg2",
        "python-dateutil",
        "python-dotenv",
        "pytz",
        "six",
        "SQLAlchemy",
        "typing_extensions",
        "tzdata",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
