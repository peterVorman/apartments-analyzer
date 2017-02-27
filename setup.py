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
        'aiohttp==1.1.6',
        'motor==1.1',
        'newrelic==2.74.0.54',
        'beautifulsoup4==4.5.3'
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==3.0.5',
                   'pytest-asyncio==0.5.0',
                   'pytest-cov==2.4.0',
                   'pytest-flake8==0.8.1'],
)
