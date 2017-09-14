from setuptools import setup

setup(
    name='apartments-analyzer',
    version='0.0.1',
    packages=['analyzer'],
    url='',
    license='MIT',
    author='Peter Vorman',
    author_email='peter.vorman@gmail.com',
    description='',
    install_requires=[
        'pip==9.0.1',
        'setuptools==36.4.0',
        'aiohttp==2.2.5',
        'motor==1.1',
        'beautifulsoup4==4.6.0',
    ],
    setup_requires=['pytest-runner'],
    tests_require=[
        'pytest==3.2.2',
        'pytest-asyncio==0.7.0',
        'pytest-cov',
        'pytest-flake8',
    ],
)
