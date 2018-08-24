from setuptools import setup, find_packages

setup(
    name='pytest-web-result-server',
    version='0.1',
    packages=find_packages(exclude=['tests']),
    url='https://github.com/TamirShalit/pytest-web-result-server',
    install_requires=['flask-sqlalchemy', 'sqlalchemy-utils'],
    tests_requires=['pytest'],
    author='tamir',
    author_email='shalit.tamir@gmail.com',
    description='Web server for viewing pytest results'
)
