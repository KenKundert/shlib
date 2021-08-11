try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from codecs import open

with open("README.rst", encoding="utf-8") as f:
    readme = f.read()

setup(
    name = "shlib",
    version = "1.3.0",
    description = "shell library",
    long_description = readme,
    long_description_content_type = 'text/x-rst',
    author = "Ken Kundert",
    author_email = "shlib@nurdletech.com",
    packages = ["shlib"],
    url = "https://nurdletech.com/linux-utilities/shlib",
    download_url = "https://github.com/kenkundert/shlib/tarball/master",
    license = "GPLv3+",
    zip_safe = False,
    install_requires = [
        "braceexpand",  # this one is optional
        "inform",  # this one is optional
    ],
    setup_requires = ["pytest-runner>=2.0"],
    tests_require = ["pytest", "inform"],
    keywords = ["shlib", "shell", "utilities"],
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Utilities",
    ],
)
