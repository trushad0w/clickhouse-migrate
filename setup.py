from setuptools import find_packages, setup

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="clickhouse-migrate",
    packages=find_packages(),
    version="0.0.3",
    description="Migration library for Clickhouse",
    author="trushad0w",
    install_requires=["click>=8.0.3", "clickhouse_driver>=0.2.2", "envparse==0.2.0 "],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/trushad0w/clickhouse-migrate",
    author_email="xpen95@gmail.com",
    entry_points={
        "console_scripts": ["clickhouse-migrate=clickhouse_migrate.manage:main"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: SQL",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Database",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    keywords="ClickHouse db database analytics migrations migrate",
    test_suite="pytest",
    license="MIT",
    license_file="LICENSE",
    python_requires=">=3.6",
)
