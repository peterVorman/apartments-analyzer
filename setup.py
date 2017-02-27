from distutils.core import setup

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
        'newrelic==2.74.0.54'
    ]
)
