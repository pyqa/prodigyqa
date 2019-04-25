"""Setup package installs Prodigy QA Package dependencies and plugins."""

from setuptools import setup, find_packages  # noqa
from os import path


this_directory = path.abspath(path.dirname(__file__))
long_description = None
try:
    with open(path.join(this_directory, 'README.md'), 'rb') as f:
        long_description = f.read().decode('utf-8')
except IOError:
    long_description = 'Unified Automation Testing Framework'

setup(
    name='prodigyqa',
    version='1.0.10',
    description='Test Automation Framework',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://pyqa.github.io/prodigyqa/',
    platforms=["Windows", "Linux", "Unix", "Mac OS-X"],
    author='Revant',
    author_email='revanth.mvs@hotmail.com',
    maintainer='Revant',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Internet",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Acceptance",
        "Topic :: Utilities",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=[
        'pip',
        'setuptools',
        'scikit-image',
        'selenium',
        'nose',
        'jsondiff',
        'openpyxl',
        'pytesseract',
        'beautifulsoup4',
        'opencv-python',
        'flake8==3.7.7',
        'pycodestyle<2.6.0,>=2.5.0',
        'pandas==0.24.2',
        'requests>=2.19.1',
        'urllib3==1.24.2',
        'ipdb==0.12',
        'pytest>=4.0.2',
        'pytest-html<1.21.0',
        'xlrd>=0.9.0',
        'scrapy',
        'nltk',
    ],)
print("\n*** Prodigy QA Installation Complete! ***\n")
