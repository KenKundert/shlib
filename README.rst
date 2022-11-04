ShLib — Shell Library
=====================

.. image:: https://pepy.tech/badge/shlib/month
    :target: https://pepy.tech/project/shlib

..  image:: https://github.com/KenKundert/shlib/actions/workflows/build.yaml/badge.svg
    :target: https://github.com/KenKundert/shlib/actions/workflows/build.yaml


.. image:: https://img.shields.io/coveralls/KenKundert/shlib.svg
    :target: https://coveralls.io/r/KenKundert/shlib

.. image:: https://img.shields.io/pypi/v/shlib.svg
    :target: https://pypi.python.org/pypi/shlib

.. image:: https://img.shields.io/pypi/pyversions/shlib.svg
    :target: https://pypi.python.org/pypi/shlib/

:Author: Ken Kundert
:Version: 1.5
:Released: 2022-11-04

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

Use 'pip3 install shlib' to install. Requires Python3.6 or better.


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

May also be used in a *with* block::

   with cd(path):
       cwd()

The working directory returns to its original value upon leaving the *with* 
block.


Current Working Directory (cwd)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns the current working directory::

   path = cwd()


Mount and Unmount a Filesystem (mount)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Mount a filesystem with::

   mount(path)

Then unmount it with::

   umount(path)

You can test to determine if a filesystem is mounted with::

   is_mounted(path)

May also be used in a *with* block::

   with mount(path):
       cp(path/data, '.')

The filesystem is unmounted upon leaving the *with* block.


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


File Permissions
~~~~~~~~~~~~~~~~

Change the file permissiongs of a file, or files, or directory, or directories::

   chmod(mode, path)

where *mode* is a three digit octal number.

You may read the permissions of a file or directory using::

   mode = getmod(path)


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

*to_path* returns a Path object that has been extended from the standard Python 
pathlib Path object.  Specifically, it includes the following methods::

   p.is_readable()   — return True if path exists and is readable
   p.is_writable()   — return True if path exists and is writable
   p.is_executable() — return True if path exists and is executable
   p.is_hidden()     — return True if path exists and is hidden (name starts with .)
   p.is_newer()      — return True if path exists and is newer than argument
   p.path_from()     — differs from relative_to() in that returned path will not start with ..
   p.sans_ext()      — return full path without the extension

See `extended_pathlib <https://github.com/KenKundert/extended_pathlib>`_ for 
more information.


Leaves
~~~~~~

Recursively descend into a directory yielding paths to all of the files it 
contains. Normally hidden files are excluded unless the *hidden* argument is 
True.  OSErrors found during the scan are ignored unless the *report* argument 
is specified, and if specified it must be a function that takes one argument, 
the exception raised by the error.


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

   Cmd(cmd[, modes][, env][, encoding][, log][, option_args])

*cmd* may be a list or a string.
*mode* is a string that specifies various options. The options are specified 
using a single letter, with upper case enabling the option and lower case 
disabling it:

   |  S, s: Use, or do not use, a shell
   |  O, o: Capture, or do not capture, stdout
   |  E, e: Capture, or do not capture, stderr
   |  M, m: Merge, or do not merge, stderr into stdout (M overrides E, e)
   |  W, w: Wait, or do not wait, for command to terminate before proceeding

If a letter corresponding to a particular option is not specified, the default 
is used for that option.  In addition, one of the following may be given, and it 
must be given last

   |  ``*``: accept any output status code
   |  N: accept any output status code equal to or less than N
   |  M,N,...: accept status codes M, N, ...

If you do not specify the status code behavior, only 0 is accepted as normal 
termination, all other codes will be treated as errors.  An exception is raised 
if exit status is not acceptable. By default an *OSError* is raised, however if 
the *use_inform* preference is true, then *inform.Error* is used. In this case 
the error includes attributes that can be used to access the *stdout*, *stderr*, 
*status*, *cmd*, and *msg*.

*env* is a dictionary of environment variable and their values.

*encoding* is used on the input and output streams when converting them to and
from strings.

*log* specifies whether details about the command should be sent to log file.
May be True, False, or None. If None, then behavior is set by *log_cmd*
preference. Use of *log* requires that *Inform* package be installed.

*option_args* is used when rendering command to logfile, it indicates how many
arguments each option takes.  This only occurs when *use_inform* preference is 
true and *Inform* package is installed.

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

   >>> ref_bytes_written = to_path('./REF').write_text(ref)
   >>> test_bytes_written = to_path('./TEST').write_text(test)

   >>> cat = Cmd(['cat', 'TEST'], 'sOeW')
   >>> cat.run()
   0

   >>> print(cat.stdout)
   line1
   line2

   >>> diff = Cmd('diff TEST REF', 'sOEW1')
   >>> status = diff.run()
   >>> status
   1

Use of *O* in the modes allows access to stdout, which is needed to access the 
differences. Specifying *E* also allows access to stderr, which in this case is 
helpful in case something goes wrong because it allows the error handler to 
access the error message generated by diff. Specifying *W* indicates that run() 
should block until diff completes. This is also necessary for you to be able to 
capture either stdout or stderr.  Specifying 1 indicates that either 0 or 1 are 
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
       status = diff.wait()
   except KeyboardInterrupt:
       diff.kill()

Casting the object to a string returns the command itself::

   >>> print(str(cat))
   cat TEST

If you call run(), then you should either specify 'W' as the wait mode, or you 
should call the wait() method. If you do not, then any string you specified as 
stdin is not applied. If your intention is to kick off a process and not wait 
for it to finish, you should use start() instead. It also allows you to specify 
a string to pass to stdin, however you cannot access stdout, stderr, or the exit 
status. If you specify the 'O' or 'E' modes when using start(), those outputs 
are simply discarded. This is a useful way of discarding uninteresting 
diagnostics from the program you are calling.

*Cmd* also provides the *render* method, which converts the command to a string.  
It takes the same optional arguments as does *render_command*.


Run
~~~

*Run* subclasses *Cmd*. It basically constructs the process and then immediately 
calls the run() method. It takes the same arguments as Cmd, but an additional 
argument that allows you to specify stdin for the process::

   Run(cmd[, modes][, stdin][, env][, encoding])

Run expect you to wait for the process to end, either by specify the 'W' mode, 
or by calling wait().  For example::

   >>> echo = Run('cat > helloworld', 'SoeW', 'hello world')
   >>> echo.status
   0

   >>> echo = Run(['echo', 'helloworld'], 'sOew')
   >>> echo.wait()
   0

   >>> print(echo.stdout.strip())
   helloworld


Start
~~~~~

Start also subclasses Cmd. It is similar to Run in that it immediately executes 
the command, but it differs in that it does not expect you to wait for the 
command to terminate. You may specify stdin to the command if you wish, but 
since you are not waiting for the command to terminate you cannot access stdout, 
stderr or the exit status.  Effectively, Start() kicks off the process and then 
ignores it.  You may pass wait or accept in the mode string, but they are 
ignored. If you select either stdout or stderr to be captured, then are wired to 
/dev/null, meaning that the selected output is swallowed and discarded.

::

   >>> cat = Start('cat helloworld', 'sOe')


which
~~~~~

Given a name, a path, and a collection of read, write, or execute flags, this 
function returns the locations along the path where a file or directory can be 
found with matching flags::

   which(name, path=None, flags=os.X_OK)

By default the path is specified by the PATH environment variable and the flags 
check whether you have execute permission.


render_command
~~~~~~~~~~~~~~

Render a command to a string::

    render_command(cmd[, option_args][, width])

Converts the command to a string.  The formatting is such that you should be 
able to feed the result directly to a shell and have command execute properly.

*cmd* is the command to render. It may be a string or a list of strings.

*option_args* is a dictionary.  The keys are options accepted by the command and 
the value is the number of arguments for that option.  If an option is not 
found, it is assumed to have 0 arguments.

*width* specifies how long the string must be before it is broken into multiple 
lines.  If length of resulting line would be width or less, return as a
single line, otherwise place each argument and option on separate line.

If the command is rendered as multiple lines, each argument and option is placed 
on a separate line, while keeping argument to options on the same line as the 
option.  Placing each option and argument on its own line allows complicated 
commands with long arguments to be displayed cleanly.

For example::

    >>> args = {'--dux': 2, '-d': 2, '--tux': 1}
    >>> print(render_command('bux --dux a b -d c d --tux e f g h', args))
    bux --dux a b -d c d --tux e f g h

    >>> print(render_command('bux --dux a b -d c d --tux e f g h', args, width=0))
    bux \
        --dux a b \
        -d c d \
        --tux e \
        f \
        g \
        h


set_prefs
~~~~~~~~~

Used to set preferences that affect the *Cmd* class. The preferences are given 
as keyword arguments.

*use_inform* indicates that the *Inform* exception *Error* should be raised if 
the exit status from a command is not acceptable. If this not given or is False, 
an OSError is raised instead.  Use of this preference requires that *Inform* be 
available.  If *use_inform* is True, then inform.Error() is used by *Cmd* and 
its subclasses (*Run* and *Start*).

*log_cmd* specifies that the command and its exit status should be written to 
the *Inform* log file.  Use of this preference requires that *Inform* be 
available.


Error Reporting with Inform
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The *Cmd* class and its subclasses (*Run* and *Start*) raise an `Inform 
<https://inform.readthedocs.io>`_ Error if the *use_inform* preference was 
specified. This allows for rich error reporting. In particular, the command, 
exit status, stdout and stderr are all returned with the exception and are 
available to insert into an error message. For example::

    >> from shlib import Run, set_prefs
    >> from inform import Error

    >> set_prefs(use_inform=True)

    >> try:
    ..     c = Run('sort words', 'sOEW0')
    .. except Error as e:
    ..     e.report(template=(
    ..         '"{cmd}" exits with status {status}.\n    {stderr}',
    ..         '"{cmd}" exits with status {status}.',
    ..     ))
    error: "sort words" exits with status 2.
        sort: cannot read: words: No such file or directory.

If command returns a non-zero exit status, an exception is raised and one of two 
error messages are printed. The first is printed if *stderr* is not empty, and 
the second is printed if it is.

Most other functions raise an OSError upon an error.  You can use *Inform* to 
convert this exception into a reasonable error message::

    >> from inform import fatal, os_error
    >>
    >> try:
    ..    cp(from, to)
    .. except OSError as e:
    ..    fatal(os_error(e))
