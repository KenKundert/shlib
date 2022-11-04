try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from codecs import open

with open("README.rst", encoding="utf-8") as f:
    readme = f.read()

setup(
    name = "shlib",
    version = "1.5",
    description = "shell library",
    long_description = readme,
    long_description_content_type = 'text/x-rst',
    author = "Ken Kundert",
    author_email = "shlib@nurdletech.com",
    packages = ["shlib"],
    url = "https://nurdletech.com/linux-utilities/shlib",
    download_url = "https://github.com/kenkundert/shlib/tarball/master",
    license = "GPLv3+",
    zip_safe = True,
    install_requires = [
        "braceexpand",  # this one is optional
        "inform",       # this one is optional
    ],
    keywords = ["shlib", "shell", "utilities"],
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ],
)
