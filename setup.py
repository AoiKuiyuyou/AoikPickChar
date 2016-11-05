# coding: utf-8
"""
Setup module.
"""
from __future__ import absolute_import

# External imports
from setuptools import find_packages
from setuptools import setup


# Run setup
setup(
    name='AoikPickChar',

    version='0.1.0',

    description='Render picked font characters to images.',

    long_description="""`Documentation on Github
<https://github.com/AoiKuiyuyou/AoikPickChar>`_""",

    url='https://github.com/AoiKuiyuyou/AoikPickChar',

    author='Aoi.Kuiyuyou',

    author_email='aoi.kuiyuyou@google.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='render font character image',

    package_dir={
        '': 'src'
    },

    packages=find_packages('src'),

    include_package_data=True,

    install_requires=[
        'pillow>=3.4.2',
    ],

    entry_points={
        'console_scripts': [
            'aoikpickchar=aoikpickchar.__main__:main',
        ],
    },
)
