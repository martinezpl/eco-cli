from setuptools import setup, find_packages

setup(
    name='eco-cli',
    version='0.1.4',
    packages=find_packages(),
    install_requires=['pandas', 'inquirer'],
    url='https://github.com/martinezpl/eco-cli',
    license='MIT',
    author='Marcin Szleszynski',
    author_email='mszlesz@gmail.com',
    description='A CLI tool for personal finance management',
    entry_points= {
        'console_scripts': 
        ['eco=eco.main:main']},
    include_package_data = True
)
