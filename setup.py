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
        "dotenv-python==0.0.1",
        "greenlet==3.1.1",
        "numpy==2.2.2",
        "pandas==2.2.3",
        "polars==1.21.0",
        "psycopg2==2.9.10",
        "python-dateutil==2.9.0.post0",
        "python-dotenv==1.0.1",
        "pytz==2024.2",
        "six==1.17.0",
        "SQLAlchemy==2.0.37",
        "typing_extensions==4.12.2",
        "tzdata==2025.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
