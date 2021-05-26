import os
from setuptools import setup

root_dir_path = os.path.dirname(os.path.abspath(__file__))

try:
    import pypandoc
    long_description = pypandoc.convert("README.md", "rst")
except(IOError, ImportError):
    long_description = open(os.path.join(root_dir_path, "README.md")).read()

with open(os.path.join(root_dir_path, "requirements.txt")) as requirements_file:
    requirements = requirements_file.readlines()

setup(
    name="atecina",
    version="0.1",
    author="Diego J. Romero López",
    author_email="diegojromerolopez@gmail.com",
    description="A simple image converter to art.",
    long_description=long_description,
    classifiers=[
        "Development Status :: 3 - Alpha",
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=requirements,
    license="MIT",
    keywords="images pillow svg converter",
    url='https://github.com/diegojromerolopez/atecina',
    packages=["converters"],
    package_dir={"converters": "src/converters"},
    data_files=[],
    include_package_data=True,
    scripts=[
        "bin/random_circler.py",
        "bin/mount_mongofs.py"
    ]
)
