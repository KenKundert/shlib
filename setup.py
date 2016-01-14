try:                                                                                                                   
    from setuptools import setup
except ImportError:
    from distutils.core import setup
         
with open('README.rst') as f:
    readme = f.read()

setup(
    name='shlib',
    version='0.0.2',
    description='shell library',
    long_description=readme,
    author="Ken Kundert",
    author_email='shlib@nurdletech.com',
    packages=['shlib'],
    url='https://github.com/kenkundert/shlib',
    license='GPLv3+',
    zip_safe=True,
    keywords=[
        'shlib',
        'pathlib',
        'shell',
        'utilities',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities',
    ],
)
