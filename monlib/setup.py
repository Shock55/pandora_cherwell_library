from setuptools import find_packages
from setuptools import setup

setup(
    name='monlib',
    version='0.1.0',
    packages=['landscapelib', 'pandora_api', 'monitoringlib'],
    install_requires=[
        'greenlet==1.1.2',
        'httplib2==0.20.4',
        'importlib-metadata==4.8.3',
        'jedi==0.18.1',
        'parso==0.8.3',
        'pyaml==21.10.1',
        'pycparser==2.21',
        'pymssql==2.2.5',
        'PyMySQL==1.0.2',
        'pyparsing==3.0.9',
        'pyrabbit==1.1.0',
        'pyspnego==0.5.3',
        'python-dateutil==2.8.2',
        'pytz==2022.1',
        'PyYAML==6.0',
        'semantic-version==2.10.0',
        'setuptools-rust==1.1.2',
        'six==1.16.0',
        'smbprotocol==1.9.0',
        'SQLAlchemy==1.4.39',
        'typing_extensions==4.1.1',
        'zipp==3.6.0',
        'cryptography==37.0.4'],
    author='Gregor Liedtke',
    author_email='your@email.com',
    description='Your sub-project'
)
