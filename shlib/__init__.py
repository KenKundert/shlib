__version__ = '0.1.2'

from .shlib import (
    to_path,
    cd, chmod, cp, cwd, ln, ls, lsd, lsf, mkdir, mv, rm, touch,
    cartesian_product, brace_expand,
    is_readable, is_writable, is_executable, is_file, is_dir,
    Cmd, Run, Sh, run, sh, bg, shbg, which
)
