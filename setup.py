from setuptools import find_packages, setup

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="clickhouse-migrate",
    packages=find_packages(),
    version="0.0.1b",
    description="Migration library for Clickhouse",
    author="trushad0w",
    install_requires=["click>=8.0.3", "clickhouse_driver>=0.2.2"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/trushad0w/clickhouse-migrate",
    author_email="xpen95@gmail.com",
    entry_points={
        "console_scripts": ["clickhouse-migrate=clickhouse_migrate.manage:main"],
    },
    test_suite="tests",
    license="MIT",
    license_file="LICENSE",
    python_requires=">=3.6",
)
