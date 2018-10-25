__version__ = '0.8.4'
__released__ = '2018-10-24'

from .extended_pathlib import Path
from .shlib import (
    # path utilities
    is_str, is_iterable, is_collection, to_path, to_paths,

    # preferences
    set_prefs,

    # filesystem utilities
    cp, mv, rm, ln, touch, mkdir, cd, cwd, chmod, ls, lsd, lsf,

    # path expansion utilities
    leaves, cartesian_product, brace_expand,

    # execution utilities
    Cmd, Run, Start, which, split_cmd, quote_arg, render_command

    # deprecated execution utilities
    # run, sh, bg, shbg
)
