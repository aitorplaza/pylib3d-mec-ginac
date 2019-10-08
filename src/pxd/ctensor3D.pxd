
'''
Author: Víctor Ruiz Gómez
Description: This file will declare all the methods and classes defined in the lib3d
mec ginac Tensor3D.h header which are going to be used by this library.
'''

######## Imports ########

# Imports from the standard C++ library
from libcpp.string cimport string

# Imports from .pxd file definitions
from src.pxd.cmatrix cimport Matrix
from src.pxd.cvector3D cimport Vector3D
from src.pxd.cbase cimport Base
from src.pxd.cginac cimport ex




######## Class Tensor3D ########


cdef extern from "Tensor3D.h":
    cdef cppclass Tensor3D(Matrix):
        # Constructor
        Tensor3D(Matrix values, Base* base)

        # Getters
        Base* get_Base()
        void set_Base(Base* base)

        # Operations
        Tensor3D operator+(Tensor3D& other)
        Tensor3D operator-(Tensor3D& other)
        Tensor3D operator*(Tensor3D& other)
        Vector3D operator*(Vector3D& other)
        Tensor3D operator*(ex& other)