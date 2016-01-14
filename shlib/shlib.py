# scripts -- Scripting utilities
#
# A light-weight package with few dependencies that allows users to do 
# shell-script like things relatively easily in Python.

# License {{{1
# Copyright (C) 2016 Kenneth S. Kundert
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].

# Imports {{{1
from pathlib import Path
import itertools
import shutil
import errno
import os
import sys

# Parameters {{{1
DEFAULT_ENCODING = 'utf-8'

# Utilities {{{1
# is_str {{{2
from six import string_types
def is_str(obj):
    """Identifies strings in all their various guises."""
    return isinstance(obj, string_types)

# is_iterable {{{2
import collections
def is_iterable(obj):
    """Identifies objects that can be iterated over, including strings."""
    return isinstance(obj, collections.Iterable)

# is_collection {{{2
def is_collection(obj):
    """Identifies objects that can be iterated over, excluding strings."""
    return is_iterable(obj) and not is_str(obj)

# to_path {{{2
def to_path(arg):
    return Path(arg)

# to_paths {{{2
def to_paths(args):
    "Iterate through up to two levels of arguments, converting them to paths"
    for arg in args:
        if is_collection(arg):
            for each in arg:
                yield to_path(each)
        else:
            yield to_path(arg)
 
# to_str {{{2
def to_str(path):
    # following is preferred because an error will eventually result if 
    # something other than a path or a string is passed to this function, 
    # unfortunately it will not work until python 3.4.5
    #return getattr(path, 'path', path)
    return str(path)

# os_error {{{2
def os_error(errno, filename=None):
    if filename:
        raise OSError(errno, os.strerror(errno), str(filename))
    else:
        raise OSError(errno, os.strerror(errno))

# File system utility functions (cp, mv, rm, ln, touch, mkdir, ls, etc.) {{{1
# cp {{{2
def cp(*paths):
    "Copy files or directories (equivalent to 'cp -rf')"
    dest = to_path(paths[-1])
    srcs = list(to_paths(paths[:-1]))
    if dest.is_dir():
        for src in srcs:
            if src.is_dir():
                fulldest = Path(dest, src.name)
                # required because dest cannot exist with copytree
                shutil.copytree(to_str(src), to_str(fulldest))
            else:
                shutil.copy2(to_str(src), to_str(dest))
        return
    if len(srcs) > 1:
        os_error(errno.ENOTDIR, dest)
    src = srcs[0]
    if src.is_dir() and dest.is_file():
        os_error(errno.EISDIR, src)
    if src.is_dir():
        # src is directory and dest does not exist
        shutil.copytree(to_str(src), to_str(dest))
    else:
        shutil.copy2(to_str(src), to_str(dest))

# mv {{{2
def mv(*paths):
    "Move file or directory (supports moves across filesystems)"
    dest = to_path(paths[-1])
    srcs = list(to_paths(paths[:-1]))
    assert len(srcs) >= 1
    if dest.is_dir():
        for src in srcs:
            fulldest = Path(dest, src.name)
            # required because dest cannot exist with shutil.move
            shutil.move(to_str(src), to_str(fulldest))
        return
    else:
        if len(srcs) > 1:
            os_error(errno.ENOTDIR, dest)
    src = srcs[0]
    if dest.is_file():
        if src.is_dir():
            os_error(errno.EISDIR, src)
        else:
            # overwrite destination
            shutil.move(to_str(src), to_str(dest))
    else:
        # destination does not exist
        assert not dest.exists()
        shutil.move(to_str(src), to_str(dest))


# rm {{{2
def rm(*paths):
    "Remove files or directories (equivalent to rm -rf)"
    for path in to_paths(paths):
        try:
            if path.is_dir():
                shutil.rmtree(to_str(path))
            else:
                path.unlink()
        except FileNotFoundError:
            pass

# ln {{{2
def ln(src, dest):
    "Create symbolic link."
    dest = to_path(dest)
    dest.symlink_to(src)

# touch {{{2
def touch(*paths):
    """
    Touch one or more files. If files do not exist, create them.
    """
    for path in to_paths(paths):
        path.touch()

# mkdir {{{2
def mkdir(*paths):
    """
    Create a directory and all parent directories. Returns without complaint if
    directory already exists.
    """
    for path in to_paths(paths):
        try:
            path.mkdir(parents=True)
            #KSK: in py3.5 and beyond use: path.mkdir(parents=True, exist_ok=True)
        except FileExistsError:
            if path.is_file():
                raise

# cd {{{2
def cd(path):
    """Set current working directory to the given path"""
    os.chdir(to_str(path))

# cwd {{{2
def cwd():
    """Return current working directory as a pathlib path"""
    return Path.cwd()

# chmod {{{2
def chmod(mode, *paths):
    "Change the mode bits of one or more file or directory"
    for path in to_paths(paths):
        path.chmod(mode)

# ls {{{2
def ls(*paths, match='*'):
    """
    Paths may be files or directories. If path is a file, it is returned if it 
    matches the glob string. If path is a directory, the items in the directory 
    if they match the glob string.

    >>> from shlib import *

    >>> sorted(ls('*.py'))
    ['clones.py', 'scripts.py', 'setup.py', 'test.clones.py', 'test.doctests.py']

    """
    discard_dot_files = not match.startswith('.')
    paths = paths if paths else ['.']
    for path in to_paths(paths):
        if path.is_file() and path.match(match):
            yield path
        elif path.is_dir():
            for each in path.glob(match):
                if not discard_dot_files or not each.name.startswith('.'):
                    yield each

# lsd {{{2
def lsd(*paths, match='*'):
    """
    Path is expected to be a directory. If match is not given, the directory is 
    listed (minus any dot files). If match is given, it is applied to the items 
    in the directory and only those items that match are returned.

    >>> sorted(lsd('.hg*'))
    ['.hg']

    """
    for path in ls(paths, match=match):
        if path.is_dir():
            yield path

# lsf {{{2
def lsf(*paths, match='*'):
    """
    Path is expected to be a directory. If match is not given, the directory is 
    listed (minus any dot files). If match is given, it is applied to the items 
    in the directory and only those items that match are returned.

    >>> sorted(lsf('.hg*'))
    ['.hgignore']

    """
    for path in ls(paths, match=match):
        if path.is_file():
            yield path

# Path functions (is_readable, etc.) {{{1
# is_readable {{{2
def is_readable(path):
    """
    Tests whether path exists and is readable.

    >>> is_readable('/usr/bin/python')
    True

    """
    return os.access(to_str(path), os.R_OK)

# is_writable {{{2
def is_writable(path):
    """
    Tests whether path exists and is writable.

    >>> is_writable('/usr/bin/python')
    False

    """
    return os.access(to_str(path), os.W_OK)

# is_executable {{{2
def is_executable(path):
    """
    Tests whether path exists and is executable.

    >>> is_executable('/usr/bin/python')
    True

    """
    return os.access(to_str(path), os.X_OK)

# Path list functions (walk, cartesian_product, brace_expand, etc.) {{{1
# cartesian_product()  {{{2
def cartesian_product(*fragments):
    """
    Combine path fragments to to a path list. Each fragment must be a string or 
    path or an iterable that generates strings or paths.
    """
    if not len(fragments):
        return []
    return [Path(*f) for f in itertools.product(
        *(f if is_collection(f) else (f,) for f in fragments)
    )]

# brace_expand()  {{{2
try:
    from braceexpand import braceexpand

    def brace_expand(pattern):
        """Bash-style brace expansion"""
        for path in braceexpand(pattern):
            yield Path(path)

except ImportError:
    pass

# Execution classes and functions (Cmd, Run, Sh, run, bg, shbg, which){{{1
# Command class {{{2
class Cmd(object):
    """
    Specify a command

    cmd may be a string or a list.
    modes is a string that specifies various options
        S, s: Use, or do not use, shell
        O, o: Capture, or do not capture, stdout
        E, e: Capture, or do not capture, stderr
        W, s: Wait, or do not wait, for command to terminate before proceeding
    only one of the following may be given, and it must be given last
        *: accept any output status code
        N: accept any output status code equal to N or less
        M,N,...: accept status codes M, N, ...
    """
    # __init__ {{{3
    def __init__(self, cmd, modes=None, encoding=None):
        self.cmd = cmd
        self.use_shell = False
        self.save_stdout = False
        self.save_stderr = False
        self.status = None
        self.wait_for_termination = True
        self.encoding = DEFAULT_ENCODING if encoding is None else encoding
        self._interpret_modes(modes)
        self._sanity_check()

    # _interpret_modes {{{3
    def _interpret_modes(self, modes):
        accept = ''
        if modes:
            for i in range(len(modes)):
                mode = modes[i]
                if   mode == 's': self.use_shell = False
                elif mode == 'S': self.use_shell = True
                elif mode == 'o': self.save_stdout = False
                elif mode == 'O': self.save_stdout = True
                elif mode == 'e': self.save_stderr = False
                elif mode == 'E': self.save_stderr = True
                elif mode == 'w': self.wait_for_termination = False
                elif mode == 'W': self.wait_for_termination = True
                else: accept = modes[i:]; break
        self.accept = _Accept(accept)

    # _sanity_check {{{3
    def _sanity_check(self):
        if self.save_stdout or self.save_stderr:
            #assert self.wait_for_termination
            pass
            # turns out this is a valid use model. Basically stdout or stderr 
            # is swallowed up and does not bother the user. It becomes 
            # available if one waits for the process to terminate.

    # run {{{3
    def run(self, stdin=None):
        """
        Run the command

        If stdin is given, it should be a string. Otherwise, no connection is
        made to stdin of the command.

        Returns exit status if wait_for_termination is True.
        """
        import subprocess

        # Popen seems to want cmd to be a string is the shell is being use, or 
        # a list otherwise
        if is_str(self.cmd):
            cmd = self.cmd if self.use_shell else self.cmd.split()
        else:
            if self.use_shell:
                cmd = ' '.join(to_str(c) for c in self.cmd)
            else:
                cmd = [to_str(c) for c in self.cmd]

        # indicate streams to intercept
        streams = {}
        if stdin is not None:
            streams['stdin'] = subprocess.PIPE
        if self.save_stdout:
            streams['stdout'] = subprocess.PIPE
        if self.save_stderr:
            streams['stderr'] = subprocess.PIPE

        # run the command
        process = subprocess.Popen(
            cmd, shell=self.use_shell, **streams
        )

        # write to stdin
        if stdin is not None:
            process.stdin.write(stdin.encode(self.encoding))
            process.stdin.close()

        # store needed information and wait for termination if desired
        self.pid = process.pid
        self.process = process
        if self.wait_for_termination:
            return self.wait()

    # wait {{{3
    def wait(self):
        """
        Wait for command to terminate.

        This should only be used it wait-for-termination is False.

        Returns exit status of the command.
        """
        process = self.process

        # Read the outputs
        if self.save_stdout:
            self.stdout = process.stdout.read().decode(self.encoding)
        else:
            self.stderr = None
        if self.save_stderr:
            self.stderr = process.stderr.read().decode(self.encoding)
        else:
            self.stderr = None

        # wait for process to complete
        self.status = process.wait()

        # close output streams
        if process.stdout:
            process.stdout.close()
        if process.stderr:
            process.stderr.close()

        # check return code
        if self.accept.unacceptable(self.status):
            if self.stderr:
                raise OSError(None, self.stderr.strip())
            else:
                raise OSError(
                    None, "unexpected exit status (%d)." % self.status
                )
        return self.status

    # kill {{{3
    def kill(self):
        self.process.kill()
        self.process.wait()

    # __str__ {{{3
    def __str__(self):
        if is_str(self.cmd):
            return self.cmd
        else:
            return ' '.join(to_str(c) for c in self.cmd)

# Run class {{{2
class Run(Cmd):
    "Run a command immediately."
    def __init__(self, cmd, modes=None, stdin=None, encoding=None):
        self.cmd = cmd
        self.stdin = None
        self.use_shell = False
        self.save_stdout = False
        self.save_stderr = False
        self.wait_for_termination = True
        self.accept = (0,)
        self.encoding = DEFAULT_ENCODING if not encoding else encoding
        self._interpret_modes(modes)
        self._sanity_check()
        self.run(stdin)

# Sh class {{{2
class Sh(Cmd):
    "Run a command immediately in the shell."
    def __init__(self, cmd, modes=None, stdin=None, encoding=None):
        self.cmd = cmd
        self.stdin = None
        self.use_shell = True
        self.save_stdout = False
        self.save_stderr = False
        self.wait_for_termination = True
        self.encoding = DEFAULT_ENCODING if not encoding else encoding
        self._interpret_modes(modes)
        self._sanity_check()
        self.run(stdin)


# run {{{2
def run(cmd, stdin=None, accept=0, shell=False):
    "Run a command without capturing its output."
    import subprocess

    # I have never been able to get Popen to work properly if cmd is not
    # a string when using the shell
    if shell and not is_str(cmd):
        cmd = ' '.join(to_str(c) for c in cmd)
    elif is_str(cmd) and not shell:
        cmd = cmd.split()

    streams = {} if stdin is None else {'stdin': subprocess.PIPE}
    process = subprocess.Popen(cmd, shell=shell, **streams)
    if stdin is not None:
        process.stdin.write(stdin.encode(DEFAULT_ENCODING))
        process.stdin.close()
    status = process.wait()
    if _Accept(accept).unacceptable(status):
        raise OSError(None, "unexpected exit status (%d)." % status)
    return status

# sh {{{2
def sh(cmd, stdin=None, accept=0, shell=True):
    "Execute a command with a shell without capturing its output"
    return run(cmd, stdin, accept, shell=True)


# bg {{{2
def bg(cmd, stdin=None, shell=False):
    "Execute a command in the background without capturing its output."
    import subprocess
    streams = {'stdin': subprocess.PIPE} if stdin is not None else {}
    process = subprocess.Popen(cmd, shell=shell, **streams)
    if stdin is not None:
        process.stdin.write(stdin.encode(DEFAULT_ENCODING))
        process.stdin.close()
    return process.pid

# shbg {{{2
def shbg(cmd, stdin=None, shell=True):
    "Execute a command with a shell in the background without capturing its output."
    return bg(cmd, stdin, shell=True)


# which {{{2
def which(name, path=None, flags=os.X_OK):
    "Search PATH for executable files with the given name."
    result = []
    if path is None:
        path = os.environ.get('PATH', '')
    for p in path.split(os.pathsep):
        p = os.path.join(p, name)
        if os.access(p, flags):
            result.append(p)
    return result

# _Accept class {{{2
class _Accept(object):
    # accept exit codes may be specified as:
    # 1. True or the string '*':
    #       all codes are acceptable, or
    # 2. an integer N or the string 'N':
    #       code must be less than or equal to N, or
    # 3. a tuple of integers or a string of the form 'M,N,...':
    #       code must be one of the numbers
    # 4. 0 or empty string:
    #       the only valid return code is 0 (default)
    def __init__(self, accept=0):
        if is_str(accept):
            if accept == '*':
                accept = True
            else:
                try:
                    codes = tuple([int(n) for n in accept.split(',')])
                    accept = codes[0] if len(codes) == 1 else codes
                except ValueError:
                    if accept:
                        raise AssertionError('invalid modes string')
                    else:
                        accept = 0
        self.accept = accept

    def unacceptable(self, status):
        if self.accept is True:
            return False
        elif type(self.accept) is tuple:
            return status not in self.accept
        else:
            return status < 0 or status > self.accept
