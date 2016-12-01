"""Secrets setup.py"""

from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def readme():
    """Long form readme for secrets."""
    with open('README.md') as readme_file:
        return readme_file.read()


setup(
    name='validation-common-py',
    version='0.0.1',
    description='Common entity validators.',
    long_description=readme(),
    keywords='validation common',
    url='http://github.com/ocelot-saas/validation-common-py',
    author='Horia Coman',
    author_email='horia141@gmail.com',
    license='All right reserved',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    install_requires=[
        'validation-py==0.0.3',
    ],
    test_suite='tests',
    tests_require=[
        'coverage>=4,<5',
        'coveralls>=1,<2',
        'tabletest3>=1,<2',
    ],
    include_package_data=True,
    zip_safe=False
)
