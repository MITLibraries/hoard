from setuptools import find_packages, setup

setup(
    name="hoard",
    packages=find_packages(exclude=["tests"]),
    entry_points="""
        [console_scripts]
        hoard=hoard.cli:main
        """,
)
