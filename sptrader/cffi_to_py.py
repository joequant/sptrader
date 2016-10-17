"""
From
https://gist.github.com/inactivist/4ef7058c2132fa16759d#file-cffi_to_py-py

Convert a CFFI cdata structure to Python dict.

Based on http://stackoverflow.com/q/20444546/1309774 with conversion of
char[] to Python str.

Usage example:

>>> from cffi import FFI
>>> ffi = FFI()
>>> ffi.cdef('''
...     struct foo {
...         int a;
...         char b[10];
...     };
... ''')
>>> foo = ffi.new("struct foo*")
>>> foo.a = 10
>>> foo.b = "Hey"
>>> foo_elem = foo[0]
>>> ffi_convert = FfiConverter(ffi)
>>> foo_dict = ffi_convert.to_py(foo_elem)
>>> print(foo_dict)

{'a': 10, 'b': 'Hey'}
"""

###############################################################################
#
# Copyright (C) 2016 Bitquant Research Laboratories (Asia) Limited
#
# Licensed under the Simplified BSD License
#
###############################################################################

import copy

class FfiConverter(object):
    """Converts dict to and from ffi cdata objects"""
    def __init__(self, ffi):
        self.ffi = ffi
        self.debug = False

    def __convert_struct_field(self, s, fields):
        for field, fieldtype in fields:
            if fieldtype.type.kind == 'primitive':
                d = getattr(s, field)
                if fieldtype.type.cname == 'char':
                    yield(field, ord(d))
                else:
                    yield (field, d)
            else:
                yield (field, self.to_py(getattr(s, field)))

    def fields(self, s):
        type = self.ffi.typeof(s)
        if type.kind == 'struct':
            return [x[0] for x in type.fields]
        else:
            return []

    def typedefs(self, s):
        type = self.ffi.typeof(s)
        if type.kind == 'struct':
            retval = {}
            for x, y in type.fields:
                if self.debug:
                    print(x, y)
                retval[x] = {"kind": y.type.kind,
                             "cname": y.type.cname}
            return retval
        else:
            return {}

    def from_py(self, buffer, data):
        type = self.typedefs(buffer[0])
        for k, v in data.items():
            try:
                if type[k]['cname'][0:4] == 'char':
                    if isinstance(v, str):
                        v = bytes(v, 'utf-8')
                    elif isinstance(v, int):
                        v = bytes([v])
                elif type[k]['cname'][0:5] == 'float' or \
                     type[k]['cname'][0:6] == 'double':
                    v = float(v)
                elif type[k]['cname'][0:3] == 'int' or \
                     type[k]['cname'][0:4] == 'uint':
                    v = int(v)
                setattr(buffer[0], k, v)
            except TypeError as e:
                print("failed %s %s %s for %s" % (format(e), k, v,
                                                  type[k]['cname']))
                raise
        return None

    def to_py(self, s):
        type = self.ffi.typeof(s)
        if type.kind == 'struct':
            return dict(self.__convert_struct_field(s, type.fields))
        elif type.kind == 'array':
            if type.item.kind == 'primitive':
                if type.item.cname == 'char':
                    try:
                        d = self.ffi.string(s).decode('ascii')
                        if d == b'\x00':
                            return ''
                        else:
                            return d
                    except:
                        return ''
                else:
                    return [copy.copy(s[i]) for i in range(type.length)]
            else:
                return [self.to_py(s[i]) for i in range(type.length)]
        elif type.kind == 'primitive':
            return int(s)
