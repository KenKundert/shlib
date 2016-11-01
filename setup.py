try:                                                                                                                   
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst') as f:
    readme = f.read()

setup(
    name='shlib',
    version='0.3.0',
    description='shell library',
    long_description=readme,
    author="Ken Kundert",
    author_email='shlib@nurdletech.com',
    py_modules=['shlib'],
    url='http://nurdletech.com/linux-utilities/shlib',
    download_url='https://github.com/kenkundert/shlib/tarball/master',
    license='GPLv3+',
    zip_safe=True,
    install_requires=[
        'braceexpand',  # this is optional
        'extended_pathlib>=0.1',
    ],
    keywords=[
        'shlib',
        'shell',
        'utilities',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities',
    ],
)
