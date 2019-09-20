import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
#with open("requirements.txt", "r") as fh:
#    requirements = fh.read().splitlines()

setuptools.setup(
    name="fw-gear-audit",
    version="0.0.2",
    author="Tinashe M. Tapera",
    author_email="tinashemtapera@gmail.com",
    description="A Python SDK tool for auditing gear run data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PennBBL/fw-gear-audit",
    packages=setuptools.find_packages(),
    install_requires=[
        "flywheel-sdk",
        "heudiconv",
        "pandas",
        "fw-heudiconv",
        "tabulate"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'fw-gear-audit=FlywheelGearAudit.__main__:main',
        ],
    }
)
