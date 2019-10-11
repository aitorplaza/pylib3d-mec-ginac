'''
Author: Víctor Ruiz Gómez
Description: This file declares the C++ Class GiNaC::ex and all its methods
which are going to be used by this library
'''


######## Imports ########

from src.pxd.ginac.cprint cimport print_context
from src.pxd.ginac.cbasic cimport basic
from src.pxd.cvector3D cimport Vector3D
from src.pxd.ctensor3D cimport Tensor3D



######## Class GiNaC::ex ########

cdef extern from "ginac/ex.h" namespace "GiNaC":
    cdef cppclass ex:
        # Constructors
        ex() except +
        ex(const double value) except +
        ex(const basic& value) except +

        # Queries
        bint is_equal(ex& other)
        bint is_zero()

        # Evaluation
        ex eval() const

        # Arithmetic operations
        ex operator-()
        ex operator+()
        ex operator+(ex& other)
        ex operator-(ex& other)
        ex operator*(ex& other)
        ex operator/(ex& other)
        Vector3D operator*(Vector3D&)
        Tensor3D operator*(Tensor3D&)


        # Printing
        void print(print_context&, unsigned level=0) const