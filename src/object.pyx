'''
Author: Víctor Ruiz Gómez
Description: This file defines the class Object which is the base class of the
rest of the classes defined by this extension (except System).
'''



######## Mixin classes ########


class NamedObject(ABC):
    def __eq__(self, other):
        return (self is other) or ((type(self) == type(other)) and self.get_name() == other.get_name())



class LatexRenderable(ABC):
    def print_latex(self):
        _print_latex_ipython(self.to_latex())





######## Class Object ########


cdef class Object:
    '''
    This is the base class of Expr, SymbolNumeric, Base, Matrix, Vector and Point
    classes
    '''
    def __getattr__(self, key):
        if isinstance(self, NamedObject):
            if key == 'name':
                return self.get_name()

        if isinstance(self, LatexRenderable):
            if key == 'latex':
                return self.to_latex()
            if key == 'print_latex':
                return MethodType(LatexRenderable.print_latex, self)

        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{key}'")


    def __dir__(self):
        entries = super().__dir__()
        if isinstance(self, NamedObject):
            entries.append('name')
        if isinstance(self, LatexRenderable):
            entries.extend(['latex', 'print_latex'])
        return entries


    def __eq__(self, other):
        if isinstance(self, NamedObject) and isinstance(other, NamedObject):
            return NamedObject.__eq__(self, other)
        return super().__eq__(self, other)


    def __repr__(self):
        return self.__str__()





######## Global methods ########


def get_name(obj):
    if not isinstance(obj, NamedObject):
        raise TypeError('Invalid input argument: Expected SymbolNumeric, Base, Matrix, Vector3D or Point')
    return obj.get_name()


def to_latex(*args):
    def _to_latex(x):
        if isinstance(x, LatexRenderable):
            return x.to_latex()
        return x.decode() if isinstance(x, bytes) else x

    if not all(map(lambda arg: isinstance(arg, (LatexRenderable, str, bytes)), args)):
        raise TypeError('Invalid input arguments: Expected SymbolNumeric, Expr, Matrix, Vector3D, str or bytes')
    return r'\:'.join(map(_to_latex, args))


def print_latex(*args):
    _print_latex_ipython(to_latex(*args))
