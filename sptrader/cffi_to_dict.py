"""
From https://gist.github.com/inactivist/4ef7058c2132fa16759d#file-cffi_to_dict-py

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
>>> foo_dict = convert_to_python(foo_elem)
>>> print foo_dict

{'a': 10, 'b': 'Hey'}
"""

def __convert_struct_field( ffi, s, fields ):
    for field,fieldtype in fields:
        if fieldtype.type.kind == 'primitive':
            yield (field,getattr( s, field ))
        else:
            yield (field, convert_to_python( ffi, getattr( s, field ) ))

def convert_to_python(ffi, s):
    type=ffi.typeof(s)
    if type.kind == 'struct':
        return dict(__convert_struct_field( ffi, s, type.fields ) )
    elif type.kind == 'array':
        if type.item.kind == 'primitive':
            if type.item.cname == 'char':
                return ffi.string(s)
            else:
                return [ s[i] for i in range(type.length) ]
        else:
            return [ convert_to_python(ffi, s[i]) for i in range(type.length) ]
    elif type.kind == 'primitive':
        return int(s)
