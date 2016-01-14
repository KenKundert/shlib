__version__ = '0.0.2'

from pathlib import Path
from .shlib import (
    cd, chmod, cp, cwd, ln, ls, lsd, lsf, mkdir, mv, rm, touch,
    cartesian_product, brace_expand,
    is_readable, is_writable, is_executable,
    Cmd, Run, Sh, run, sh, bg, shbg, which
)
