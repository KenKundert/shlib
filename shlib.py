# scripts -- Scripting utilities
#
# A light-weight package with few dependencies that allows users to do 
# shell-script like things relatively easily in Python.

# License {{{1
# Copyright (C) 2016-2018 Kenneth S. Kundert
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

__version__ = '0.8.1'
__released__ = '2018-08-30'

# Imports {{{1
from extended_pathlib import Path
import itertools
import shlex
import shutil
import errno
import os
import sys

# Parameters {{{1
DEFAULT_ENCODING = 'utf-8'
preferences = {}

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
def to_path(*args):
    try:
        return Path(*args).expanduser()
    except AttributeError:
        return Path(*args)

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
    # first convert to path to assure ~ expansion is done, then convert back to 
    # string.
    return str(to_path(path))

# _error {{{2
#     Raise an error based on the errno.
def _error(errno, filename=None):
    if preferences.get('use_inform') == 'all':
        from inform import Error, full_stop
        raise Error(
            msg = full_stop(os.strerror(errno)),
            errno = errno,
            filename = filename,
            template = ('{filename}: {msg}', '{msg}')
        )
    if filename:
        raise OSError(errno, os.strerror(errno), str(filename))
    else:
        raise OSError(errno, os.strerror(errno))

# _os_error {{{2
#     Process an OSError.
def _os_error(e, filename=None, ignore=None):
    if ignore and e.errno == ignore:
        return
    if preferences.get('use_inform') == 'all':
        from inform import Error, full_stop
        raise Error(
            msg = full_stop(os.strerror(e.errno)),
            errno = e.errno,
            filename = e.filename,
            template = ('{filename}: {msg}', '{msg}')
        )
    raise

# split_cmd {{{2
def split_cmd(cmd):
    from shlex import split
    return split(cmd)

# quote_arg {{{2
def quote_arg(arg):
    """Return a shell-escaped version of the string *arg*."""
    try:
        from shlex import quote
    except ImportError:
        try:
            from pipes import quote
        except ImportError:
            def quote(arg):
                if not arg:
                    return "''"
                if re.search(r'[^\w@%+=:,./-]', arg, re.ASCII) is None:
                    return s
                return "'" + arg.replace("'", "'\"'\"'") + "'"
    return quote(str(arg))

# use_log {{{2
def use_log(log):
    if log is None:
        return preferences.get('log_cmd')
    return log

# Preferences {{{1
def set_prefs(**kwargs):
    """Set ShLib preferences

    Args:
        use_inform (bool or 'all'):
            Use inform for error reporting in the Cmd class and its subclasses.
            This provides a richer form of error reporting than simply using the
            OSError. Requires that inform be installed.
            If *use_inform* is 'all', inform.Error() is used for all errors.
        log_cmd (bool):
            Log the command invocation and exit status in the Cmd class and its
            subclasses. Requires that inform be installed.
    """
    preferences.update(kwargs)


# File system utility functions (cp, mv, rm, ln, touch, mkdir, ls, etc.) {{{1
# cp {{{2
def cp(*paths):
    "Copy files or directories (equivalent to 'cp -rf')"
    dest = to_path(paths[-1])
    srcs = list(to_paths(paths[:-1]))
    if dest.is_dir():
        try:
            for src in srcs:
                if src.is_dir():
                    fulldest = Path(dest, src.name)
                    # required because dest cannot exist with copytree
                    shutil.copytree(to_str(src), to_str(fulldest))
                else:
                    shutil.copy2(to_str(src), to_str(dest))
        except (OSError, IOError) as e:
            _os_error(e)
        return
    if len(srcs) > 1:
        _error(errno.ENOTDIR, dest)
    src = srcs[0]
    if src.is_dir() and dest.is_file():
        _error(errno.EISDIR, src)
    try:
        if src.is_dir():
            # src is directory and dest does not exist
            shutil.copytree(to_str(src), to_str(dest))
        else:
            shutil.copy2(to_str(src), to_str(dest))
    except (OSError, IOError) as e:
        _os_error(e)

# mv {{{2
def mv(*paths):
    "Move file or directory (supports moves across filesystems)"
    dest = to_path(paths[-1])
    srcs = list(to_paths(paths[:-1]))
    assert len(srcs) >= 1
    if dest.is_dir():
        try:
            for src in srcs:
                fulldest = Path(dest, src.name)
                # required because dest cannot exist with shutil.move
                shutil.move(to_str(src), to_str(fulldest))
            return
        except (OSError, IOError) as e:
            _os_error(e)
    else:
        if len(srcs) > 1:
            _error(errno.ENOTDIR, dest)
    src = srcs[0]
    if dest.is_file():
        if src.is_dir():
            _error(errno.EISDIR, src)
        else:
            # overwrite destination
            try:
                shutil.move(to_str(src), to_str(dest))
            except (OSError, IOError) as e:
                _os_error(e)
    else:
        # destination does not exist
        assert not dest.exists()
        try:
            shutil.move(to_str(src), to_str(dest))
        except (OSError, IOError) as e:
            _os_error(e)


# rm {{{2
def rm(*paths):
    "Remove files or directories (equivalent to rm -rf)"
    for path in to_paths(paths):
        try:
            if path.is_dir():
                shutil.rmtree(to_str(path))
            else:
                path.unlink()
        except (IOError, OSError) as e:
            _os_error(e, ignore=errno.ENOENT)

# ln {{{2
def ln(src, dest):
    "Create symbolic link."
    dest = to_path(dest)
    try:
        dest.symlink_to(src)
    except (OSError, IOError) as e:
        _os_error(e)

# touch {{{2
def touch(*paths):
    """
    Touch one or more files. If files do not exist, create them.
    """
    try:
        for path in to_paths(paths):
            path.touch()
    except (OSError, IOError) as e:
        _os_error(e)

# mkdir {{{2
def mkdir(*paths):
    """
    Create a directory and all parent directories. Returns without complaint if
    directory already exists.
    """
    try:
        for path in to_paths(paths):
            path.mkdir(parents=True)
                # older versions of pathlib ignore exist_ok
                # in Python3.5, just add exist_ok=True to arg list
    except (IOError, OSError) as e:
        _os_error(e, ignore=(errno.EEXIST if path.is_dir() else None))

# cd {{{2
class cd:
    def __init__(self, path):
        self.starting_dir = cwd()
        try:
            os.chdir(to_str(path))
        except (OSError, IOError) as e:
            _os_error(e)

    # support __enter__ and __exit__ so cd can be called in a with statement.
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, exc_traceback):
        try:
            os.chdir(to_str(self.starting_dir))
        except (OSError, IOError) as e:
            _os_error(e)

# cwd {{{2
def cwd():
    """Return current working directory as a pathlib path"""
    try:
        return Path.cwd()
    except (OSError, IOError) as e:
        _os_error(e)

# chmod {{{2
def chmod(mode, *paths):
    "Change the mode bits of one or more file or directory"
    try:
        for path in to_paths(paths):
            path.chmod(mode)
    except (OSError, IOError) as e:
        _os_error(e)

# ls {{{2
def ls(*paths, **kwargs):
    """
    List paths

    Paths may be files or directories. If path is a file, it is returned.
    If path is a directory, the items in the directory are returned.

    Args:
        paths: the paths to list ('.' if no paths given).
        select: a returned path will match this glob string, use **/* to enable 
            recursion
        reject: a returned path will not match this glob string
        only: specifies the type of returned paths, choose from 'file' or 'dir'
        hidden (bool): specifies whether hidden files should be returned, if 
            not given hidden files are returned if select string starts with 
            '.'

    KSK: it is a bit weird that I allow paths to be a list, but not select or
    reject. It would be nice to pass lists to both of those.

    Returns:
        path generator: iterates through filtered paths

    >>> from shlib import *

    >>> mkdir('d1', 'd2')
    >>> touch('d1/f1', 'd1/f2', 'd2/f1', 'd2/f2')

    >>> files = ls('d1')
    >>> set(str(f) for f in files) == set('d1/f1 d1/f2'.split())
    True

    >>> files = ls('d1', 'd2', select='*2')
    >>> set(str(f) for f in files) == set('d1/f2 d2/f2'.split())
    True

    >>> rm('d1', 'd2')

    """
    select = kwargs.get('select', '*')
    reject = kwargs.get('reject', '\0')
        # KSK: I have used '\0' as the default reject pattern because using ''
        # generates an exception. I put in an enhancement request to the pathlib
        # team to fix this, but it was rejected.
    only = kwargs.get('only')
    hidden = kwargs.get('hidden')

    def acceptable(path):
        if only == 'file' and not path.is_file():
            return False
        if only == 'dir' and not path.is_dir():
            return False
        if not retain_hidden and path.name.startswith('.'):
            return False
        if path.match(reject):
            return False
        return True

    select = to_str(select)
    retain_hidden = select.startswith('.') if hidden is None else hidden
    paths = paths if paths else ['.']
    try:
        for path in to_paths(paths):
            if path.is_file() and acceptable(path):
                if path.match(select):
                    yield path
            elif path.is_dir():
                for each in path.glob(select):
                    # glob() supports recursion so use it rather than iterdir()
                    if acceptable(each):
                        yield each
    except (OSError, IOError) as e:
        _os_error(e)

# lsd {{{2
def lsd(*args, **kwargs):
    """
    List directories

    Same as ls with only='dir'.

    >>> dirs = lsd(select='xyz*')
    >>> set(str(d) for d in dirs) == set(''.split())
    True

    >>> mkdir('d1', 'd2')
    >>> touch('d1/f1', 'd1/f2', 'd2/f1', 'd2/f2')

    >>> dirs = lsd(select='d*')
    >>> set(str(d) for d in dirs) == set('d1 d2'.split())
    True

    >>> dirs = ls(select='*2')
    >>> set(str(d) for d in dirs) == set('d2'.split())
    True

    >>> rm('d1', 'd2')

    """
    kwargs['only'] = 'dir'
    for d in ls(*args, **kwargs):
        yield d

# lsf {{{2
def lsf(*args, **kwargs):
    """
    List files

    Same as ls with only='file'.

    >>> mkdir('d1', 'd2')
    >>> touch('d1/f1', 'd1/f2', 'd2/f1', 'd2/f2')

    >>> files = lsf('d1')
    >>> set(str(f) for f in files) == set('d1/f1 d1/f2'.split())
    True

    >>> files = lsf('d1', 'd2', select='f2')
    >>> set(str(f) for f in files) == set('d1/f2 d2/f2'.split())
    True

    >>> rm('d1', 'd2')

    """
    kwargs['only'] = 'file'
    for f in ls(*args, **kwargs):
        yield f

# Path list functions (leaves, cartesian_product, brace_expand, etc.) {{{1
def _leaves(path, hidden=False):
    try:
        for each in os.scandir(path):
            if each.is_dir(follow_symlinks=False):
                for e in _leaves(each):
                    if hidden or not e.startswith('.'):
                        yield e
            else:
                if hidden or not each.name.startswith('.'):
                    yield each.path
    except (OSError, IOError) as e:
        _os_error(e)

# leaves()  {{{2
def leaves(path, hidden=False):
    """Recursively descend into a directory yielding all of the file."""
    for each in _leaves(str(path)):
        yield Path(each)

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

# Execution classes and functions (Cmd, Run, Sh, Start, run, bg, shbg, which) {{{1
# Command class {{{2
class Cmd(object):
    # description {{{3
    """
    Specify a command

    cmd may be a string or a list.
    modes is a string that specifies various options
        S, s: Use, or do not use, shell
        O, o: Capture, or do not capture, stdout
        E, e: Capture, or do not capture, stderr
        M, m: Merge, or do not merge, stderr into stdout (M overrides E, e)
        W, s: Wait, or do not wait, for command to terminate before proceeding

        Only one of the following may be given, and it must be given last:
        *: accept any output status code
        N: accept any output status code equal to N or less
        M,N,...: accept status codes M, N, ...
    env is a dictionary of environment variable and their values.
    encoding is used on the input and output streams when converting them to and
        from strings.
    log specifies whether details about the command should be sent to log file.
        May be True, False, or None. If None, then behavior is set by log_cmd
        preference.
    option_args is used when rendering command to logfile, it indicates how many
        arguments each option takes.

    An exception is raised if exit status is not acceptable. By default an
    OSError is raised, however if the *use_inform* preference is true, then
    inform.Error is used. In this case the error includes attributes that can be
    used to access the stdout, stderr, status, cmd, and msg.
    """

    # __init__ {{{3
    def __init__(
        self, cmd, modes=None, env=None, encoding=None,
        log=None, option_args=None
    ):
        self.cmd = cmd
        self.env = env
        self.use_shell = False
        self.save_stdout = False
        self.save_stderr = False
        self.merge_stderr_into_stdout = False
        self.status = None
        self.wait_for_termination = True
        self.encoding = DEFAULT_ENCODING if encoding is None else encoding
        self.log = log
        self.option_args = option_args
        self._interpret_modes(modes)

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
                elif mode == 'm': self.merge_stderr_into_stdout = False
                elif mode == 'M': self.merge_stderr_into_stdout = True
                elif mode == 'w': self.wait_for_termination = False
                elif mode == 'W': self.wait_for_termination = True
                else: accept = modes[i:]; break
        self.accept = _Accept(accept)

    # run {{{3
    def run(self, stdin=None):
        """
        Run the command, will wait for it to terminate.

        If stdin is given, it should be a string. Otherwise, no connection is
        made to stdin of the command.

        Returns exit status if wait_for_termination is True.
        If wait_for_termination is False, you must call wait(), otherwise stdin
        is not be applied.  If you don't want to wait, call start() instead.
        """
        self.stdin = stdin
        import subprocess

        if is_str(self.cmd):
            cmd = self.cmd if self.use_shell else split_cmd(self.cmd)
        else:
            # cannot use to_str() because it can change some arguments when not intended.
            # this is particularly problematic the duplicity arguments in embalm
            cmd = [str(c) for c in self.cmd]
        if use_log(self.log):
            from inform import log
            log('Running:', render_command(cmd, option_args=self.option_args))

        # indicate streams to intercept
        streams = {}
        if stdin is not None:
            streams['stdin'] = subprocess.PIPE
        if self.save_stdout:
            streams['stdout'] = subprocess.PIPE
        if self.save_stderr:
            streams['stderr'] = subprocess.PIPE
        if self.merge_stderr_into_stdout:
            streams['stderr'] = subprocess.STDOUT

        # run the command
        process = subprocess.Popen(
            cmd, shell=self.use_shell, env=self.env, **streams
        )

        # store needed information and wait for termination if desired
        self.pid = process.pid
        self.process = process
        if self.wait_for_termination:
            return self.wait()

    # start {{{3
    def start(self, stdin=None):
        """
        Start the command, will not wait for it to terminate.

        If stdin is given, it should be a string. Otherwise, no connection is
        made to stdin of the command.
        """
        self.stdin = None
        import subprocess

        if is_str(self.cmd):
            cmd = self.cmd if self.use_shell else split_cmd(self.cmd)
        else:
            cmd = self.cmd
        if use_log(self.log):
            from inform import log
            log('Running:', render_command(cmd, option_args=self.option_args))

        if self.save_stdout or self.save_stderr:
            try:
                DEVNULL = subprocess.DEVNULL
            except AttributeError:
                DEVNULL = open(os.devnull, 'wb')
        assert self.merge_stderr_into_stdout is False, 'M not supported, use E'

        streams = {}
        if stdin is not None:
            streams['stdin'] = subprocess.PIPE
        if self.save_stdout:
            streams['stdout'] = DEVNULL
        if self.save_stderr:
            streams['stderr'] = DEVNULL

        # run the command
        process = subprocess.Popen(
            cmd, shell=self.use_shell, env=self.env, **streams
        )

        # store needed information and wait for termination if desired
        self.pid = process.pid
        self.process = process

        # write to stdin
        if stdin is not None:
            process.stdin.write(stdin.encode(self.encoding))
            process.stdin.close()

    # wait {{{3
    def wait(self):
        """
        Wait for command to terminate.

        This should only be used if wait-for-termination is False.

        Returns exit status of the command.
        """
        process = self.process

        stdin = self.stdin if self.stdin else ''
        stdout, stderr = process.communicate(stdin.encode(self.encoding))
        self.stdout = None if stdout is None else stdout.decode(self.encoding)
        self.stderr = None if stderr is None else stderr.decode(self.encoding)
        self.status = process.returncode

        if use_log(self.log):
            from inform import log
            log('Exit status:', self.status)

        # check return code
        if self.accept.unacceptable(self.status):
            if self.stderr:
                msg = self.stderr.strip()
            else:
                msg = 'unexpected exit status (%d)' % self.status
            if preferences.get('use_inform'):
                from inform import Error
                raise Error(
                    msg = msg,
                    status = self.status,
                    stdout = self.stdout.rstrip() if self.stdout else None,
                    stderr = self.stderr.rstrip() if self.stderr else None,
                    cmd = render_command(self.cmd),
                    template = '{msg}'
                )
            else:
                raise OSError(None, msg)
        return self.status

    # kill {{{3
    def kill(self):
        self.process.kill()
        self.process.wait()

    # render {{{3
    def render(self, option_args=None, width=70):
        render_command(self.cmd, option_args=option_args, width=width)

    # __str__ {{{3
    def __str__(self):
        if is_str(self.cmd):
            return self.cmd
        else:
            return ' '.join(str(c) for c in self.cmd)


# Run class {{{2
class Run(Cmd):
    """Run a command immediately.

    See Cmd for information on the arguments.
    Default mode is 'soeW0'.

    Common Examples:
       Run command without capturing stdout and stderr:
           Run(['grep', filename], modes='soeW1')
       Run command and capture stdout; stderr is not captured:
           output = Run(['grep', filename], modes='sOeW1').stdout
       Run command and capture stdout; merge stderr into stdout:
           output = Run(['grep', filename], modes='sOMW1').stdout
    """
    def __init__(
        self, cmd, modes=None, stdin=None, env=None, encoding=None,
        log=None, option_args=None
    ):
        self.cmd = cmd
        self.stdin = None
        self.use_shell = False
        self.save_stdout = False
        self.save_stderr = False
        self.merge_stderr_into_stdout = False
        self.wait_for_termination = True
        self.accept = (0,)
        self.env = env
        self.encoding = DEFAULT_ENCODING if not encoding else encoding
        self.log = log
        self.option_args = option_args
        self._interpret_modes(modes)
        self.run(stdin)

# Sh class (deprecated) {{{2
class Sh(Cmd):
    """Run a command immediately in the shell.

    See Cmd for information on the arguments, see Run for examples.
    Sh() is the same as Run except S mode is default.
    Default mode is 'SoeW0'.
    """
    def __init__(
        self, cmd, modes=None, stdin=None, env=None, encoding=None,
        log=None, option_args=None
    ):
        self.cmd = cmd
        self.stdin = None
        self.use_shell = True
        self.save_stdout = False
        self.save_stderr = False
        self.merge_stderr_into_stdout = False
        self.wait_for_termination = True
        self.env = env
        self.encoding = DEFAULT_ENCODING if not encoding else encoding
        self.log = log
        self.option_args = option_args
        self._interpret_modes(modes)
        self.run(stdin)


# Start class {{{2
class Start(Cmd):
    """Run a command immediately, don't wait for it to exit.

    See Cmd for information on the arguments.
    Start() is the similar to Run when using 'w' mode.  The difference is if you
    specify O or E modes, those streams are suppressed rather than being
    captured.
    """
    def __init__(
        self, cmd, modes=None, stdin=None, env=None, encoding=None,
        log=None, option_args=None
    ):
        self.cmd = cmd
        self.stdin = None
        self.use_shell = False
        self.save_stdout = False
        self.save_stderr = False
        self.merge_stderr_into_stdout = False
        self.wait_for_termination = False
        self.accept = (0,)
        self.env = env
        self.encoding = DEFAULT_ENCODING if not encoding else encoding
        self.log = log
        self.option_args = option_args
        self._interpret_modes(modes)
        self.start(stdin)


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


# which {{{2
def which(name, path=None, flags=os.X_OK):
    "Search PATH for executable files with the given name."
    try:
        result = []
        if path is None:
            path = os.environ.get('PATH', '')
        for p in path.split(os.pathsep):
            p = os.path.join(p, name)
            if os.access(p, flags):
                result.append(p)
        return result
    except (OSError, IOError) as e:
        _os_error(e)

# render_command {{{2
def render_command(cmd, option_args=None, width=70):
    """ Render a command.

    Converts the command to a string.  The formatting is such that you should be
    able to feed the result directly to a shell and have command execute
    properly.

    *cmd* is the command to render. It may be a string or a list of strings.

    *option_args* is a dictionary.  The keys are options accepted by the command
    and the value is the number of arguments for that option.  If an option is
    not found, it is assumed to have 0 arguments.

    *width* specifies how long the string must be before it is broken into
    multiple lines.  If length of resulting line would be width or less, return
    as a single line, otherwise place each argument and option on separate line.

    If the command is rendered as multiple lines, each argument and option is
    placed on a separate line, while keeping argument to options on the same
    line as the option.  Placing each option and argument on its own line allows
    complicated commands with long arguments to be displayed cleanly.

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

    """
    if option_args is None:
        option_args = {}

    if is_str(cmd):
        components = split_cmd(cmd)
    else:
        components = [quote_arg(c) for c in cmd]
        cmd = ' '.join(components)
    if len(cmd) <= width:
        return cmd

    components.reverse()
    lines = []
    while components:
        opt = components.pop()
        num_args = option_args.get(opt, 0)
        argument = [quote_arg(opt)]
        for i in range(num_args):
            argument.append(quote_arg(components.pop()))
        lines.append(' '.join(argument))
    return ' \\\n    '.join(lines)
