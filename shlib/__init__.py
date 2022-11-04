__version__ = '1.5'
__released__ = '2022-11-04'

from .extended_pathlib import Path
from .shlib import (
    # path utilities
    is_str, is_iterable, is_collection, to_path, to_paths,

    # preferences
    set_prefs, get_state, set_state,

    # filesystem utilities
    cp, mv, rm, ln, touch, mkdir, mount, umount, is_mounted, cd, cwd,
    chmod, getmod, ls, lsd, lsf,

    # path expansion utilities
    leaves, cartesian_product, brace_expand,

    # execution utilities
    Cmd, Run, Start, which, split_cmd, quote_arg, render_command,

    # deprecated execution utilities
    run, sh, bg, shbg,
)
