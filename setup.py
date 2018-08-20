from setuptools import setup, find_packages

setup(
    name='pytest-web-result-server',
    version='0.1',
    packages=find_packages(exclude=('web_result_server.tests',)),
    url='https://github.com/TamirShalit/pytest-web-result-server',
    requires=['flask-sqlalchemy', 'sqlalchemy-utils', 'enum34'],
    author='tamir',
    author_email='shalit.tamir@gmail.com',
    description='Web server for viewing pytest results'
)
