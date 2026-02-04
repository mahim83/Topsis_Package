from setuptools import setup, find_packages

setup(
    name="Topsis-Mahim-102303958",
    version="1.0.0",
    author="Mahim",
    author_email="mkatiyar_be23@thapar.edu",
    description="Implementation of TOPSIS method as a Python package",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy"
    ],
    entry_points={
        "console_scripts": [
            "topsis=topsis_mahim_102303958.topsis:main"
        ]
    },
    python_requires=">=3.7",
)
