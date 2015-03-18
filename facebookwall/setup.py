from setuptools import setup, find_packages

setup(
    name="facebookwall",
    version="1.0",
    url='',
    license='BSD',
    description="a facebook wall like app",
    author='Jonathan Tumulak',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=['setuptools'],
)
