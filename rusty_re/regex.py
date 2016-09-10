from collections import namedtuple

from .lib import ffi, lib, checked_call


FindResult = namedtuple("FindResult", ("start", "end"))


class Regex(object):
    """ A compiled regular expression for matching Unicode strings.

    It is represented as either a sequence of bytecode instructions (dynamic)
    or as a specialized Rust function (native). It can be used to search,
    split or replace text. All searching is done with an implicit .*?
    at the beginning and end of an expression. To force an expression to match
    the whole string (or a prefix or a suffix), you must use an anchor
    like ^ or $ (or \A and \z).

    While this crate will handle Unicode strings (whether in the regular
    expression or in the search text), all positions returned are byte indices.
    Every byte index is guaranteed to be at a Unicode code point boundary.
    """

    def __init__(self, re, size=None, _pointer=None):
        """ Compiles a regular expression. Once compiled, it can be used
        repeatedly to search, split or replace text in a string.

        :param re:      Expression to compile
        :param size:    Optional limit of compiled data structure
        """
        self._ctx = ffi.gc(lib.regex_context_new(), lib.regex_context_free)
        if re:
            if size is None:
                s = checked_call(
                    lib.regex_new,
                    self._ctx,
                    re.encode('utf8'),
                )
            else:
                s = checked_call(
                    lib.regex_with_size_limit,
                    self._ctx,
                    ffi.new("size_t", size),
                    re.encode('utf8'),
                )
        else:
            s = _pointer
        self._ptr = ffi.gc(s, lib.regex_free)

    def is_match(self, text):
        """ Returns true if and only if the regex matches the string given.

        It is recommended to use this method if all you need to do is test
        a match, since the underlying matching engine may be able to do less
        work.
        """
        return bool(lib.regex_is_match(
            self._ptr,
            text.encode('utf8'),
        ))

    def find(self, text):
        """ Returns the start and end byte range of the leftmost-first match
        in text. If no match exists, then None is returned.

        Note that this should only be used if you want to discover the position
        of the match. Testing the existence of a match is faster if you use
        is_match.
        """
        result = lib.regex_find(
            self._ptr,
            text.encode('utf8'),
        )
        fr = FindResult(result.start, result.end)
        ffi.gc(result, lib.regex_findresult_free)
        return fr
