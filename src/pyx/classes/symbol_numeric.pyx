'''
Author: Víctor Ruiz Gómez
Description: This module defines the wrapper class SymbolNumeric.
'''




######## Class SymbolNumeric ########


cdef class SymbolNumeric(Object):
    '''
    Objects of this class can be used to perform math symbolic computation.
    '''

    ######## C Attributes  ########


    cdef c_symbol_numeric* _c_handler
    cdef object _owner



    ######## Constructor & Destructor  ########

    def __cinit__(self, Py_ssize_t ptr, owner):
        self._c_handler = <c_symbol_numeric*>ptr
        self._owner = owner


    ######## Getters ########


    cpdef double get_value(self):
        '''get_value() -> float
        :return: The numeric value of this symbol as a float value.
        :rtype: float
        '''
        return self._c_handler.get_value().to_double()


    cpdef get_tex_name(self):
        '''get_tex_name() -> str
        Get the name in latex of this symbol
        :rtype: str
        '''
        return (<bytes>self._c_handler.print_TeX_name()).decode()


    def get_owner(self):
        '''get_owner() -> System
        Get the system where this numeric symbol was created
        :rtype: System
        '''
        return self._owner


    def get_type(self):
        '''get_type() -> str
        Get the type of this symbol.
        :returns: One of the next values:
            'parameter', 'joint_unknown', 'input',
            'coordinate', 'velocity', 'acceleration',
            'aux_coordinate', 'aux_velocity', 'aux_acceleration'
            'time' (the last one only if this instance is the time symbol)
        :rtype: str
        '''
        owner = self.get_owner()
        if self == owner._get_time():
            return 'time'
        for symbol_type in _symbol_types:
            if self in owner._get_symbols(symbol_type):
                return symbol_type.decode()
        raise RuntimeError



    ######## Setters ########


    cpdef set_value(self, value):
        '''set_value(value: float)
        Assigns a new numeric value to this symbol.
        :param value: It must be the new numeric value to assign for this symbol
        :type value: int, float
        :raises TypeError: If value has an incorrect type.
        '''
        self._c_handler.set_value(c_numeric(<double>_parse_numeric_value(value)))



    cpdef set_tex_name(self, tex_name):
        '''set_tex_name(tex_name: str)
        Changes the latex name of this symbol
        :param str tex_name: The new latex name
        :raise TypeError: If the input argument has an incorrect type
        '''
        self._c_handler.set_TeX_name(_parse_text(tex_name))




    ######## Properties  ########


    @property
    def value(self):
        '''
        Property that returns the numeric value of this symbol (as a float number). It also supports
        assignment.
        :rtype: float
        '''
        return self.get_value()

    @value.setter
    def value(self, value):
        self.set_value(value)


    @property
    def tex_name(self):
        '''
        Property that returns the name in latex of this symbol. It also supports assignment.
        :rtype: str
        '''
        return self.get_tex_name()


    @tex_name.setter
    def tex_name(self, tex_name):
        self.set_tex_name(tex_name)


    @property
    def owner(self):
        '''
        Property that returns the system where this symbol was created
        :rtype: System
        '''
        return self.get_owner()


    @property
    def type(self):
        '''
        Only read property that returns the kind of symbol
        :rtype: str
        '''
        return self.get_type()

    @property
    def kind(self):
        '''
        This is an alias of property "type"
        :rtype: str
        '''
        return self.get_type()



    ######## Arithmetic operations ########


    def __neg__(self):
        '''
        Negates this symbol. The result is a symbolic expression.
        :rtype: Expr
        '''
        return -Expr(self)


    def __pos__(self):
        '''
        Performs unary positive operation on this symbol. The result is a symbol
        expression.
        :rtype: Expr
        '''
        return +Expr(self)


    def __add__(self, other):
        '''
        Performs the sum operation with another symbol. The result is a symbolic
        expression.
        :rtype: Expr
        .. note:: Sum operation can be performed between symbols and expressions, but
            this logic is implemented in Expr.__add__ metamethod
        '''
        return NotImplemented if isinstance(other, Expr) else Expr(self) + Expr(other)


    def __sub__(self, other):
        '''
        Performs the subtraction operation with another symbol. The result is a symbolic
        expression.
        :rtype: Expr
        .. note:: Subtraction operation can be performed between symbols and expressions, but
            this logic is implemented in Expr.__sub__ metamethod
        '''
        return NotImplemented if isinstance(other, Expr) else Expr(self) - Expr(other)


    def __mul__(self, other):
        '''
        Multiplies this symbol with another. The result is a symbolic expression.
        :rtype: Expr
        .. note:: Symbols can be multiplied with matrices (or its subclasses) and expressions, but this is implemented
            in the metamethods Expr.__mul__, Matrix.__mul__, Vector3D.__mul__ and Tensor3D.__mul__
        '''
        return NotImplemented if isinstance(other, (Expr, Matrix)) else Expr(self) * Expr(other)


    def __truediv__(self, other):
        '''
        :rtype: Expr
        Divides this symbol with another. The result is a symbolic expression.
        .. note:: Symbols can also divide or be divided by expressions. This
            functionality is implemented in Expr.__truediv__
        '''
        return NotImplemented if isinstance(other, Expr) else Expr(self) / other


    def __pow__(self, other, modulo):
        '''
        :rtype: Expr
        Raises this symbol by another one (the exponent could also be an expression).
        The result is an expression.
        '''
        return pow(Expr(self), other, modulo)




    ######## Number conversions ########


    def __float__(self):
        '''
        Alias of get_value().
        '''
        return self.get_value()


    def __int__(self):
        '''
        Returns the numeric value of this symbol truncated (as an integer)
        '''
        return int(self.get_value())


    def __complex__(self):
        '''
        Returns the numeric value of this symbol as a complex number.
        .. note:: The imaginary part is set to zero
        '''
        return complex(self._c_handler.get_value().real().to_double(), self._c_handler.get_value().imag().to_double())







NamedObject.register(SymbolNumeric)
LatexRenderable.register(SymbolNumeric)
