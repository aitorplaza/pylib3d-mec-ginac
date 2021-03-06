'''
Author: Víctor Ruiz Gómez
Description: This file contains all the declarations of the C++ header
Wrench3D.h that are going to be used by this library
'''


######## Imports ########

# Imports from the standard C++ library
from libcpp.string cimport string



# Imports from .pxd file definitions
from src.core.pxd.cvector3D cimport Vector3D
from src.core.pxd.cpoint cimport Point
from src.core.pxd.csolid cimport Solid
from src.core.pxd.ginac.cexpr cimport ex


######## Class Wrench3D ########

cdef extern from "Wrench3D.h":
    cdef cppclass Wrench3D:
        # Constructors
        Wrench3D(string, Vector3D, Vector3D, Point*, Solid*, string) except +

        # Getters
        string get_name()
        Vector3D get_Force()
        Vector3D get_Moment()
        Point* get_Point()
        Solid* get_Solid()
        string get_Type()

        # Operations
        Wrench3D unatomize()
        Wrench3D at_Point(Point*)

        # Arithmetic operations
        Wrench3D operator+(Wrench3D&)
        Wrench3D operator-(Wrench3D&)
        Wrench3D operator-()
        ex operator*(Wrench3D&)
