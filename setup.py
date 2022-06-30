#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open("candidate-README.md") as readme_file:
    readme = readme_file.read()

base_requirements = [
    "requests",
    "pandas",
]

extras = ["umap-learn", "whatlies[all]", "jupyterlab", "ipywidgets"]

lint = ["black", "isort>=5.7.0", "pre-commit", "flake8>=3.8.4", "nbstripout"]

test = [
    "pytest>=6.2.2",
    "pytest-cov",
    "toml",
]

azure_pipelines = ["pytest-azurepipelines"]

extras_require = {
    "extras": extras,
    "dev": extras + lint + test,
    "azure": lint + test + azure_pipelines,
}

setup(
    author="Candidate",
    author_email="candidate@mail",
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description=("CashFlow data management"),
    install_requires=base_requirements,
    extras_require=extras_require,
    long_description=readme,
    keywords="cashflow_dm",
    name="cashflow_dm",
    packages=find_packages(include=["cashflow_dm", "cashflow_dm.*"]),
    test_suite="cashflow_dm/tests",
    tests_require=test,
    url="https://github.com/utsavjha/cashflow-datamaker-api.git",
    version="0.0.1",
    zip_safe=False,
)
