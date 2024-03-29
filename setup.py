from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name="physics_engine-robertgamer4",
    version="0.4.0",
    description="2D physics engine",
    long_description=readme,
    author="robertgamer4",
    url="https://github.com/robertgamer4/physics_engine",
    license=license,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OSX",
    ],
    python_requires='>=3.7'
)
