import os
import re
import sys
from ._ffi import ffi


class RegexError(Exception):
    pass


class SyntaxError(RegexError):
    pass


class CompiledTooBigError(RegexError):
    pass


def find_library():
    libname = "rewrapper"
    if sys.platform == 'win32':
        prefix = ''
        suffix = 'dll'
    elif sys.platform == 'darwin':
        prefix = 'lib'
        suffix = 'dylib'
    else:
        prefix = 'lib'
        suffix = 'so'
    cur_dir = os.path.dirname(__file__)
    return os.path.join(cur_dir, "{}{}.{}".format(prefix, libname, suffix))


lib = ffi.dlopen(find_library())

EXCEPTION_MAP = {
    'std::io::Error': OSError,
    'regex::Error': RegexError,
    'regex::Error::Syntax': re.error,
    'regex::Error::CompiledTooBig': CompiledTooBigError,
}


def checked_call(fn, ctx, *args):
    res = fn(ctx, *args)
    if not ctx.has_error:
        return res
    msg = ffi.string(ctx.error_display).decode('utf8').replace('\n', ' ')
    type_str = ffi.string(ctx.error_type).decode('utf8')
    err_type = EXCEPTION_MAP.get(type_str)
    if err_type is RegexError:
        desc_str = ffi.string(ctx.error_description).decode('utf8')
        enum_val = re.match(r'(\w+)\(.*?\)', desc_str, re.DOTALL).group(1)
        err_type = EXCEPTION_MAP.get("{}::{}".format(type_str, enum_val))
        if err_type is None:
            msg = "{}: {}".format(enum_val, msg)
    if err_type is None:
        err_type = RegexError
    raise err_type(msg)
