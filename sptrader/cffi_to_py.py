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


class FfiConverter(object):
    """Converts dict to and from ffi cdata objects"""
    def __init__(self, ffi):
        self.ffi = ffi

    def __convert_struct_field(self, s, fields):
        for field, fieldtype in fields:
            if fieldtype.type.kind == 'primitive':
                d = getattr(s, field)
                if d == b'\x00':
                    yield(field, '')
                elif fieldtype.type.cname == 'char':
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
                    return [s[i] for i in range(type.length)]
            else:
                return [self.to_py(s[i]) for i in range(type.length)]
        elif type.kind == 'primitive':
            return int(s)
