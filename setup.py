"""
@Author  : chouxiaohui
@Date    : 2021/1/26 10:21 上午
@Version : 1.0
"""
import glob

from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
import os

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
# with open(path.join(here, 'README.md'), encoding='utf-8') as f:
#     long_description = f.read()

# glob.glob(os.path.join('check_duplicate/', 'web/templates/', 'index.html'))

setup(
    name='check_duplicate',
    version='0.0.1',

    description='文章重复率检测',
    long_description='',

    # Author details
    author='XiaoHui Chou',
    # Choose your license
    # license='MIT',


    # What does your project relate to?
    keywords='',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    include_package_data=True,
    # package_data= {'check_duplicate':os.listdir(os.path.join('check_duplicate/', 'web/templates/'))},
    zip_safe=False,
    install_requires=['Flask', 'jieba'],

)
