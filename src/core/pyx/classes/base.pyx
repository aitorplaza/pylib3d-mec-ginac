'''
Author: Víctor Ruiz Gómez
Description: This module defines the class Base
'''




######## Class Base ########


cdef class Base(Object):
    '''
    Objects of this class represent geometric bases defined within a system.
    '''

    ######## C Attributes ########


    cdef c_Base* _c_handler




    ######## Constructor & Destructor ########


    def __cinit__(self, Py_ssize_t handler):
        self._c_handler = <c_Base*>handler




    ######## Getters ########


    cpdef get_previous_base(self):
        '''get_previous_base() -> Base
        Get the previous base.

        :returns: The previous base of this one if it has
        :rtype: Base
        :raises RuntimeError: If this base dont any previous one

        '''
        cdef c_Base* c_prev_base = self._c_handler.get_Previous_Base()
        if c_prev_base == NULL:
            raise RuntimeError(f'base {self.name} dont have a preceding one')
        return Base(<Py_ssize_t>c_prev_base)

    get_previous = get_previous_base



    cpdef bint has_previous_base(self):
        '''has_previous_base() -> bool
        Check if this base has a previous one.

        :returns: True if this base has a preceding base, False otherwise.
        :rtype: bool

        '''
        return self._c_handler.get_Previous_Base() != NULL

    has_previous = has_previous_base



    cpdef get_rotation_angle(self):
        '''get_rotation_angle() -> Expr
        Get the rotation angle of this base

        :rtype: Expr

        '''
        return _expr_from_c(self._c_handler.get_Rotation_Angle())



    cpdef get_rotation_tupla(self):
        '''get_rotation_tupla() -> Matrix
        Get the rotation tupla of this base

        :rtype: Matrix

        '''
        return _matrix_from_c_value(self._c_handler.get_Rotation_Tupla())



    cpdef get_angular_velocity(self):
        '''get_angular_velocity() -> Vector3D
        Get the angular velocity of this base

        :rtype: Vector3D
        '''
        cdef c_Base* c_prev_base = self._c_handler.get_Previous_Base()
        if c_prev_base == NULL:
            raise RuntimeError('Cant compute the angular velocity for this base')
        return _vector_from_c_value(self._c_handler.angular_velocity())




    ######## Properties ########


    @property
    def previous_base(self):
        '''
        Read only property that returns the previous base

        :rtype: Base

        .. note::
            This calls internally to ``get_previous_base``

            .. seealso:: :func:`get_previous_base`
        '''
        return self.get_previous_base()


    @property
    def previous(self):
        '''
        This is an alias of previous_base property

        .. note::
            This calls internally to ``get_previous_base``

            .. seealso:: :func:`get_previous_base`

        '''
        return self.get_previous_base()


    @property
    def rotation_angle(self):
        '''
        Read only property that returns the rotation angle of this base

        :rtype: Expr

        .. note::
            This calls internally to ``get_rotation_angle``

            .. seealso:: :func:`get_rotation_angle`

        '''
        return self.get_rotation_angle()


    @property
    def rotation_tupla(self):
        '''
        Read only property that returns the rotation tupla of this base

        :rtype: Matrix

        .. note::
            This calls internally to ``get_rotation_tupla``

            .. seealso:: :func:`get_rotation_tupla`
        '''
        return self.get_rotation_tupla()



    @property
    def angular_velocity(self):
        '''
        Read only property that returns the angular velocity of this base

        :rtype: Vector3D

        .. note::

            This calls internally to ``get_angular_velocity

        '''
        return self.get_angular_velocity()


NamedObject.register(Base)
