from setuptools import setup

setup(
    name='nuamo',
    version='0.1.0',
    description='Tool to generate potential project names',
    url='https://github.com/MatthewScholefield/nuamo',
    author='Matthew Scholefield',
    author_email='matthew331199@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    keywords='nuamo project name nlp',
    packages=['nuamo'],
    install_requires=[
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'nuamo=nuamo.__main__:main'
        ],
    }
)
