from setuptools import setup, find_packages

setup(
    name="fio",
    version='0.1',
    description='',
    author='FIO Team',
    author_email='fioteam@fio.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['fio=command_line:main'],
    },
    test_suite="tests",
    install_requires=[
        'click', 'click-log'
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"])
