ShLib - Shell Library
=====================

A light-weight package with few dependencies that allows users to do 
shell-script like things relatively easily in Python. Is a natural complement to 
the pathlib library. Pathlib does pretty much what you would like to do with 
a single path; shlib does similar things with many paths at once. For example, 
with pathlib you can remove (unlink) a single file, but with shlib you can 
remove many files at once. Furthermore, most of the features of pathlib are 
implemented as pathlib methods, so you must convert your strings to paths before 
you can use them. ShLib is equally comfortable with strings as with paths.

Writing programs that substantially interact with the file system can be 
surprisingly painful in Python because the code that is used to do so is spread 
over many packages and those packages are not very compatible with each other 
nor do they follow the conventions of the corresponding shell commands.

This package, shlib, attempts to address those issues by providing one package 
that combines the commonly used utilities for interacting with the filesystem 
that follows the conventions used by the corresponding shell commands.  

It consists of replacements for some very common Unix utilities that interact 
with the filesystem, such as cp, mv, rm, ln, mkdir, and cd. These tend to be 
less fussy than their command line counter parts. For example, rm deletes both 
files and directories without distinction and will not complain if the file or 
directory does not exist. Similarly mkdir will create any child directories 
needed and will not complain if the directory already exists.

Finally, it provides several ways to run external programs.

Each feature is designed to allow you to express your desires simply and 
efficiently without worrying too much about exceptions.

Most of the functions in this package take paths to files or directories. Those 
paths may be specified either as strings or pathlib paths. Many of the functions 
accept multiple paths, and those can be specified either as an array or as 
individual arguments. Several of the functions return either a path or 
a collection of paths. These paths are returned as pathlib paths.


Installation
------------

Use 'pip3 install shlib' to install. Requires Python2.7 or Python3.3 or better.

.. image:: https://img.shields.io/travis/KenKundert/shlib/master.svg
    :target: https://travis-ci.org/KenKundert/shlib

.. image:: https://img.shields.io/coveralls/KenKundert/shlib.svg
    :target: https://coveralls.io/r/KenKundert/shlib

.. image:: https://img.shields.io/pypi/v/shlib.svg
    :target: https://pypi.python.org/pypi/shlib

.. image:: https://img.shields.io/pypi/pyversions/shlib.svg
    :target: https://pypi.python.org/pypi/shlib/

.. image:: https://img.shields.io/pypi/dd/shlib.svg
    :target: https://pypi.python.org/pypi/shlib/


System Utility Functions
------------------------

Copy (cp)
~~~~~~~~~

Copy files or directories::

    cp(src, ..., dest)

or::

    cp([src, ...], dest)

Copy all source items, whether they be files or directories to dest. If there is 
more than one src item, then dest must be a directory and the copies will be 
placed in that directory.  The src arguments may be strings, pathlib paths, or 
collections of strings and paths.  The dest must be a string or path.

Example:

.. code-block:: python

   >>> from shlib import *
   >>> testdir = 'testdir'
   >>> rm(testdir)
   >>> mkdir(testdir)
   >>> files = cartesian_product(testdir, ['f1', 'f2'])
   >>> touch(files)
   >>> dirs = cartesian_product(testdir, ['d1', 'd2'])
   >>> mkdir(dirs)
   >>> print(sorted(str(e) for e in ls(testdir)))
   ['testdir/d1', 'testdir/d2', 'testdir/f1', 'testdir/f2']

   >>> cp('testdir/f1', 'testdir/f4')
   >>> print(sorted(str(f) for f in lsf(testdir)))
   ['testdir/f1', 'testdir/f2', 'testdir/f4']

   >>> dest1 = to_path(testdir, 'dest1')
   >>> mkdir(dest1)
   >>> cp(files, dest1)
   >>> print(sorted(str(f) for f in lsf(dest1)))
   ['testdir/dest1/f1', 'testdir/dest1/f2']

   >>> cp(dirs, dest1)
   >>> print(sorted(str(d) for d in lsd(dest1)))
   ['testdir/dest1/d1', 'testdir/dest1/d2']

   >>> f1, f2 = tuple(files)
   >>> dest2 = to_path(testdir, 'dest2')
   >>> mkdir(dest2)
   >>> cp(f1, f2, dest2)
   >>> print(sorted(str(f) for f in lsf(dest2)))
   ['testdir/dest2/f1', 'testdir/dest2/f2']

   >>> dest3 = to_path(testdir, 'dest3')
   >>> mkdir(dest3)
   >>> cp([f1, f2], dest3)
   >>> print(sorted(str(f) for f in lsf(dest3)))
   ['testdir/dest3/f1', 'testdir/dest3/f2']


Move (mv)
~~~~~~~~~

Move files or directories::

    mv(src, ..., dest)

Move all source items, whether they be files or directories to dest. If there is 
more than one src item, then dest must be a directory and everything will be 
placed in that directory.  The src arguments may be strings or lists of strings.  
The dest must be a string.

.. code-block:: python

   >>> from shlib import *
   >>> testdir = 'testdir'
   >>> rm(testdir)
   >>> mkdir(testdir)
   >>> files = cartesian_product(testdir, ['f1', 'f2'])
   >>> touch(files)
   >>> dirs = cartesian_product(testdir, ['d1', 'd2'])
   >>> mkdir(dirs)
   >>> print(sorted(str(e) for e in ls(testdir)))
   ['testdir/d1', 'testdir/d2', 'testdir/f1', 'testdir/f2']

   >>> dest = to_path(testdir, 'dest')
   >>> mkdir(dest)
   >>> mv(files, dest)                  # move a list of files
   >>> print(sorted(str(f) for f in lsf(dest)))
   ['testdir/dest/f1', 'testdir/dest/f2']

   >>> mv(dirs, dest)                   # move a list of directories
   >>> print(sorted(str(d) for d in lsd(dest)))
   ['testdir/dest/d1', 'testdir/dest/d2']


Remove (rm)
~~~~~~~~~~~

Remove files or directories::

    rm(path, ...)

Delete all files and directories given as arguments. Does not complain if any of 
the items do not exist.  Each argument must be either a string or a list of 
strings.

.. code-block:: python

   >>> print(sorted(str(e) for e in ls(testdir)))
   ['testdir/dest']

   >>> print(sorted(str(e) for e in ls(dest)))
   ['testdir/dest/d1', 'testdir/dest/d2', 'testdir/dest/f1', 'testdir/dest/f2']

   >>> rm(lsf(dest))
   >>> print(sorted(str(e) for e in ls(dest)))
   ['testdir/dest/d1', 'testdir/dest/d2']

   >>> rm(dest)
   >>> print(sorted(str(e) for e in ls(testdir)))
   []

   >>> rm(testdir)

Link (ln)
~~~~~~~~~~~

Create a symbolic link::

   ln(src, link)

Creates a symbolic link *link* that points to *src*.  Each argument must be 
either a string.


Make File (touch)
~~~~~~~~~~~~~~~~~

Create a new empty file or update the timestamp on an existing file::

   touch(path, ...)

Each argument must be either a string or a list of strings.


Make Directory (mkdir)
~~~~~~~~~~~~~~~~~~~~~~

Create an empty directory::

   mkdir(path, ...)

For each argument it creates a directory and any needed parent directories.  
Returns without complaint if the directory already exists. Each argument must be 
either a string or a list of strings.


Change Directory (cd)
~~~~~~~~~~~~~~~~~~~~~

Change to an existing directory::

   cd(path)

Makes path the current working directory.

May also be used in a with block::

   with cd(path):
       cwd()

The working directory returns to its original value upon leaving the with block.


List Directory (ls, lsd, lsf)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List a directory::

   ls(path, ... [<kwargs>])
   lsd(path, ... [<kwargs>])
   lsf(path, ... [<kwargs>])

The first form returns a list of all items found in a directory. The second 
returns only the directories, and the third returns only the files.

One or more paths may be specified using unnamed arguments. The paths may be 
strings or pathlib paths, or collections of those.  If no paths are not given, 
the current working directory is assumed.

The remaining arguments must be specified as keyword arguments.

::

   select=<glob-str>

If *select* is specified, an item is returned only if it matches the given 
pattern.  Using '\*\*' in *select* enables a recursive walk through a directory 
and all its subdirectories.  Using '\*\*' alone returns only directories whereas 
'\*\*/\*' returns files and directories.

::

   reject=<glob-str>

If *reject* is specified, an item is not returned if it matches the given 
pattern.

::

   only={'file','dir'}


If *only* is specified, it may be either 'file' or 'dir', in which case only 
items of the corresponding type are returned.

::

    hidden=<bool>

The value of hidden is a boolean that indicates whether items that begin with 
'.' are included in the output. If hidden is not specified, hidden items are not 
included unless *select* begins with '.'.

Examples::

   pyfiles = lsf(select='*.py')
   subdirs = lsd()
   tmp_mutt = lsf('/tmp/', select='mutt-*')


Paths
-----

to_path
~~~~~~~

Create a path from a collection of path segments::

   p = to_path(seg, ...)

The segments are combined to form a path. Expands a leading ~. Returns a pathlib 
path. It is generally not necessary to apply to_path() to paths being given to 
the shlib functions, but using it gives you access to all of the various pathlib 
methods for the path.

.. code-block:: python

   >>> path = to_path('A', 'b', '3')
   >>> str(path)
   'A/b/3'


Cartesian Product
~~~~~~~~~~~~~~~~~

Create a list of paths by combining from path segments in all combinations::

   cartesian_product(seg, ...)

Like with to_path(), the components are combined to form a path, but in this 
case each component may be a list. The results is the various components are 
combined in a Cartesian product to form a list. For example:

.. code-block:: python

   >>> paths = cartesian_product(['A', 'B'], ['a', 'b'], ['1', '2'])
   >>> for p in paths:
   ...     print(p)
   A/a/1
   A/a/2
   A/b/1
   A/b/2
   B/a/1
   B/a/2
   B/b/1
   B/b/2


Brace Expand
~~~~~~~~~~~~

Create a list of paths using Bash-like brace expansion::

   brace_expand(pattern)

.. code-block:: python

   >>> paths = brace_expand('python{2.{5..7},3.{2..6}}')

   >>> for p in sorted(str(p) for p in paths):
   ...     print(p)
   python2.5
   python2.6
   python2.7
   python3.2
   python3.3
   python3.4
   python3.5
   python3.6


Executing Programs
------------------

The following classes and functions are used to execute external programs from 
within Python.

Command (Cmd)
~~~~~~~~~~~~~

A class that runs an external program::

   Cmd(cmd[, modes][, encoding])

*cmd* may be a list or a string.
*mode* is a string that specifies various options. The options are specified 
using a single letter, with upper case enabling the option and lower case 
disabling it:

   |  S, s: Use, or do not use, shell
   |  O, o: Capture, or do not capture, stdout
   |  E, e: Capture, or do not capture, stderr
   |  W, s: Wait, or do not wait, for command to terminate before proceeding

If a letter corresponding to a particular option is not specified, the default 
is used for that option.  In addition, one of the following may be given, and it 
must be given last

   |  ``*``: accept any output status code
   |  N: accept any output status code equal to or less than N
   |  M,N,...: accept status codes M, N, ...

If you do not specify the status code behavior, only 0 is accepted as normal 
termination, all other codes will be treated as errors.

For example, to run diff you might use::

   >>> import sys, textwrap
   >>> ref = textwrap.dedent('''
   ...     line1
   ...     line2
   ...     line3
   ... ''').strip()
   >>> test = textwrap.dedent('''
   ...     line1
   ...     line2
   ... ''').strip()

   >>> ref_bytes_written = to_path('./ref').write_text(ref)
   >>> test_bytes_written = to_path('./test').write_text(test)

   >>> cat = Cmd(['cat', 'test'], 'sOeW')
   >>> cat.run()
   0

   >>> print(cat.stdout)
   line1
   line2

   >>> diff = Cmd('diff test ref', 'sOEW1')
   >>> status = diff.run()
   >>> status
   1

Use of O in the modes allows access to stdout, which is needed to access the 
differences. Specifying E also allows access to stderr, which in this case is 
helpful in case something goes wrong because it allows the error handler to 
access the error message generated by diff. Specifying W indicates that run() 
should block until diff completes. Specifying 1 indicates that either 0 or 1 are 
valid output status codes; any other code output by diff would be treated as an 
error.

If you do not indicate that stdout or stderr should be captured, those streams 
remain connected to your TTY. You can specify a string to the run() method, 
which is fed to the program through stdin. If you don't specify anything the 
stdin stream for the program also remains connected to the TTY.

If you indicate that run() should return immediately without out waiting for the 
program to exit, then you can use the wait() and kill() methods to manage the 
execution. For example::

   diff = Cmd(['gvim', '-d', lfile, rfile], 'w')
   diff.run()
   try:
       diff.wait()
   except KeyboardInterrupt:
       diff.kill()


Run and Sh
~~~~~~~~~~

Run and Sh are subclasses of Cmd. They are the same except that they both run 
the program right away (you would not explicitly run the program with the 
run()).  Run does not use a shell by default whereas Sh does.

   >>> echo = Run('echo hello world > helloworld', 'SoeW')
   >>> echo.status
   0

   >>> cat = Run(['cat', 'helloworld'], 'sOeW')
   >>> cat.status
   0

   >>> print(cat.stdout)
   hello world
   <BLANKLINE>

run, sh, bg, shbg
~~~~~~~~~~~~~~~~~

These are functions that run a program without capturing its output::

   run(cmd, stdin=None, accept=0, shell=False)
   sh(cmd, stdin=None, accept=0, shell=True)
   bg(cmd, stdin=None, shell=False)
   shbg(cmd, stdin=None, shell=True)

run and sh block until the program completes, whereas bg and shbg do not. run 
and bg do not use a shell by default where as sh and shbg do. accept specifies 
the exit status codes that will be accepted without being treated as being an 
error. If you specify a simple number, than any code greater than that value is 
treated as an error. If you provide a collection of numbers in a tuple or list, 
then any code not found in the collection is considered an error.

which
~~~~~

Given a name, a path, and a collection of read, write, or execute flags, this 
function returns the locations along the path where a file or directory can be 
found with matching flags::

   which(name, path=None, flags=os.X_OK)

By default the path is specified by the PATH environment variable and the flags 
check whether you have execute permission.
