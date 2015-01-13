from setuptools import setup, find_packages

setup(
    name = 'docker-ship',
    version = 0.1,
    packages = find_packages(),
    scripts = ['src/docker-ship.py'],
    author = 'Elliot Smith',
    author_email = 'elliot.smith91@gmail.com',
    license = 'MIT',
)
