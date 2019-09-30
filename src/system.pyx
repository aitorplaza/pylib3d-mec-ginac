'''
Author: Víctor Ruiz Gómez
Description: This module defines the interface between Python and C++ for the
class System
'''


######## Helper variables & methods ########

cdef void outError(const char* msg):
    # Redefinition of outError function (to suppress error messages)
    pass




######## Class System ########


## Class which acts like a bridge between Python and C++ System class
cdef class _System:


    ######## C Attributes ########

    cdef c_System* _c_handler



    ######## Constructor & Destructor ########


    def __cinit__(self):
        # Initialize C++ System object
        self._c_handler = new c_System(outError)


    def __dealloc__(self):
        del self._c_handler




    ######## C Getters ########

    cdef void* _get_c_object(self, c_string name, c_string kind):
        '''
        Get the object with the given name & type defined within this system
        :param string name: Name of the symbol
        :param string kind: Type of object ('parameter', 'vector', 'matrix', ...)
        :returns: A generic C pointer to the object or NULL if not object with such
            name or type exists
        :rtype: void*
        '''
        if kind == b'coordinate':
            return <void*>self._c_handler.get_Coordinate(name)
        if kind == b'velocity':
            return <void*>self._c_handler.get_Velocity(name)
        if kind == b'acceleration':
            return <void*>self._c_handler.get_Acceleration(name)
        if kind == b'aux_coordinate':
            return <void*>self._c_handler.get_AuxCoordinate(name)
        if kind == b'aux_velocity':
            return <void*>self._c_handler.get_AuxVelocity(name)
        if kind == b'aux_acceleration':
            return <void*>self._c_handler.get_Acceleration(name)

        if kind == b'parameter':
            return <void*>self._c_handler.get_Parameter(name)
        if kind == b'joint_unknown':
            return <void*>self._c_handler.get_Unknown(name)
        if kind == b'input':
            return <void*>self._c_handler.get_Input(name)

        if kind == b'base':
            return <void*>self._c_handler.get_Base(name)
        if kind == b'matrix':
            return <void*>self._c_handler.get_Matrix(name)
        if kind == b'vector':
            return <void*>self._c_handler.get_Vector3D(name)
        return NULL



    cdef bint _has_c_object(self, c_string name, c_string kind):
        '''
        Check if an object with the given name & type exists within this system
        :param string name: Name of the symbol
        :param string kind: Type of the object ('parameter', 'vector', 'matrix', ...)
        :returns: 1 if the object exists. 0 otherwise
        :rtype: bint
        '''
        return self._get_c_object(name, kind) != NULL



    cdef c_symbol_numeric_list _get_c_symbols(self, c_string kind):
        '''
        Get all symbols of the given type defined within this system
        :param kind: Kind of symbols to retrieve. e.g: 'parameter'
        :type kind: std::string
        :rtype: std::vector[symbol_numeric*]
        '''
        if kind == b'coordinate':
            return self._c_handler.get_Coordinates()
        if kind == b'velocity':
            return self._c_handler.get_Velocities()
        if kind == b'acceleration':
            return self._c_handler.get_Accelerations()
        if kind == b'aux_coordinate':
            return self._c_handler.get_AuxCoordinates()
        if kind == b'aux_velocity':
            return self._c_handler.get_AuxVelocities()
        if kind == b'aux_acceleration':
            return self._c_handler.get_AuxAccelerations()
        if kind == b'parameter':
            return self._c_handler.get_Parameters()
        if kind == b'input':
            return self._c_handler.get_Inputs()
        if kind == b'joint_unknown':
            return self._c_handler.get_Joint_Unknowns()



    cdef c_Matrix _get_c_symbols_matrix(self, c_string kind):
        '''
        Get the matrix for the symbols of the given type.
        :param string kind: Must be the type of symbols to include in the resulting matrix
        :rtype: Matrix
        '''
        if kind == b'coordinate':
            return self._c_handler.Coordinates()
        if kind == b'velocity':
            return self._c_handler.Velocities()
        if kind == b'acceleration':
            return self._c_handler.Accelerations()
        if kind == b'aux_coordinate':
            return self._c_handler.Aux_Coordinates()
        if kind == b'aux_velocity':
            return self._c_handler.Aux_Velocities()
        if kind == b'aux_acceleration':
            return self._c_handler.Aux_Accelerations()
        if kind == b'parameter':
            return self._c_handler.Parameters()
        if kind == b'input':
            return self._c_handler.Inputs()
        if kind == b'joint_unknown':
            return self._c_handler.Joint_Unknowns()




    cdef c_symbol_numeric_list _get_all_c_symbols(self):
        '''
        Get all symbols within this system
        :rtype: std::vector[symbol_numeric*]
        '''
        cdef c_vector[c_symbol_numeric_list] containers
        containers.push_back(self._c_handler.get_Coordinates())
        containers.push_back(self._c_handler.get_Velocities())
        containers.push_back(self._c_handler.get_Accelerations())
        containers.push_back(self._c_handler.get_AuxCoordinates())
        containers.push_back(self._c_handler.get_AuxVelocities())
        containers.push_back(self._c_handler.get_AuxAccelerations())
        containers.push_back(self._c_handler.get_Parameters())
        containers.push_back(self._c_handler.get_Inputs())
        containers.push_back(self._c_handler.get_Joint_Unknowns())

        cdef c_symbol_numeric_list symbols
        cdef size_t num_symbols = 0

        for container in containers:
            num_symbols += container.size()
        symbols.reserve(num_symbols)

        for container in containers:
            symbols.insert(symbols.end(), container.begin(), container.end())

        return symbols



    cdef c_vector[c_Base*] _get_c_bases(self):
        '''
        Get all bases defined within this system
        :rtype: std::vector[Base*]
        '''
        return self._c_handler.get_Bases()


    cdef c_vector[c_Matrix*] _get_c_matrices(self):
        '''
        Get all matrices defined within this system
        :rtype: std::vector[Matrix*]
        '''
        return self._c_handler.get_Matrixs()


    cdef c_vector[c_Vector3D*] _get_c_vectors(self):
        '''
        Get all vectors defined within this system
        :rtype: std::vector[Vector3D*]
        '''
        return self._c_handler.get_Vectors()





    ######## Getters ########


    cpdef _get_symbol(self, name, kind=None):
        cdef c_symbol_numeric *c_symbol
        cdef c_symbol_numeric *x
        cdef c_symbol_numeric_list c_symbols

        name = _parse_name(name)
        if kind is not None:
            kind = _parse_symbol_type(kind)
            c_symbol = <c_symbol_numeric*>self._get_c_object(name, kind)
        else:
            c_symbols = self._get_all_c_symbols()
            c_symbol = NULL
            for x in c_symbols:
                if x.get_name() == <c_string>name:
                    c_symbol = x

        if c_symbol != NULL:
            return SymbolNumeric(<Py_ssize_t>c_symbol)

        if kind is None:
            raise IndexError(f'Symbol "{name.decode()}" not created yet')
        kind_title = kind.decode().replace("_", " ")
        if self._has_symbol(name):
            raise IndexError(f'Symbol "{name.decode()}" is not a {kind_title}')
        raise IndexError(f'{kind_title} "{name.decode()}" not created yet')



    cpdef _has_symbol(self, name, kind=None):
        cdef c_symbol_numeric_list c_symbols
        cdef c_symbol_numeric* x

        name = _parse_name(name)
        if kind is not None:
            kind = _parse_symbol_type(kind)
            return self._has_c_object(name, kind)

        c_symbols = self._get_all_c_symbols()
        for x in c_symbols:
            if x.get_name() == <c_string>name:
                return True
        return False


    cpdef _get_symbols_matrix(self, kind):
        cdef c_Matrix c_matrix = self._get_c_symbols_matrix(_parse_symbol_type(kind))
        return _matrix_from_c_value(c_matrix)



    cpdef _get_time(self):
        return SymbolNumeric(<Py_ssize_t>&self._c_handler.t)



    cpdef _get_base(self, name):
        name = _parse_name(name)
        cdef c_Base* c_base = <c_Base*>self._get_c_object(name, b'base')
        if c_base == NULL:
            raise IndexError(f'Base "{name.decode()}" doesnt exist')
        return Base(<Py_ssize_t>c_base)


    cpdef _get_matrix(self, name):
        name = _parse_name(name)
        cdef c_Matrix* c_matrix = <c_Matrix*>self._get_c_object(name, b'matrix')
        if c_matrix == NULL:
            raise IndexError(f'Matrix "{name.decode()}" doesnt exist')
        return _matrix_from_c(c_matrix)


    cpdef _get_vector(self, name):
        name = _parse_name(name)
        cdef c_Vector3D* c_vector = <c_Vector3D*>self._get_c_object(name, b'vector')
        if c_vector == NULL:
            raise IndexError(f'Vector "{name.decode()}" doesnt exist')
        return _vector_from_c(c_vector)


    cpdef _has_base(self, name):
        return self._has_c_object(_parse_name(name), b'base')

    cpdef _has_matrix(self, name):
        return self._has_c_object(_parse_name(name), b'matrix')

    cpdef _has_vector(self, name):
        return self._has_c_object(_parse_name(name), b'vector')


    cpdef _has_object(self, name):
        name = _parse_name(name)
        return self._has_symbol(name) or self._has_base(name) or self._has_matrix(name) or self._has_vector(name)




    ######## Container getters ########


    cpdef _get_all_symbols(self):
        cdef c_symbol_numeric_list c_symbols = self._get_all_c_symbols()
        symbols = [SymbolNumeric(<Py_ssize_t>c_symbol) for c_symbol in c_symbols]
        return symbols


    cpdef _get_symbols(self, kind=None):
        if kind is None:
            return self._get_all_symbols()
        cdef c_symbol_numeric_list c_symbols = self._get_c_symbols(_parse_symbol_type(kind))
        symbols = [SymbolNumeric(<Py_ssize_t>c_symbol) for c_symbol in c_symbols]
        return symbols


    cpdef _get_bases(self):
        cdef c_vector[c_Base*] c_bases = self._c_handler.get_Bases()
        return [Base(<Py_ssize_t>c_base) for c_base in c_bases]

    cpdef _get_matrices(self):
        cdef c_vector[c_Matrix*] c_matrices = self._c_handler.get_Matrixs()
        return [_matrix_from_c(c_matrix) for c_matrix in c_matrices]

    cpdef _get_vectors(self):
        cdef c_vector[c_Vector3D*] c_vectors = self._c_handler.get_Vectors()
        return [_vector_from_c(c_vector) for c_vector in c_vectors]





    ######## C Constructors ########


    cdef c_symbol_numeric* _new_c_parameter(self, c_string name, c_string tex_name, double value):
        return self._c_handler.new_Parameter(name, tex_name, c_numeric(value))


    cdef c_symbol_numeric* _new_c_input(self, c_string name, c_string tex_name, double value):
        return self._c_handler.new_Input(name, tex_name, c_numeric(value))


    cdef c_symbol_numeric* _new_c_joint_unknown(self, c_string name, c_string tex_name, double value):
        return self._c_handler.new_Joint_Unknown(name, tex_name, c_numeric(value))


    cdef c_symbol_numeric* _new_c_aux_coordinate(self,
        c_string name,     c_string vel_name,     c_string acc_name,
        c_string tex_name, c_string vel_tex_name, c_string acc_tex_name,
        double   value,    double   vel_value,    double   acc_value):
        return self._c_handler.new_AuxCoordinate(
            name, vel_name, acc_name,
            tex_name, vel_tex_name, acc_tex_name,
            c_numeric(value), c_numeric(vel_value), c_numeric(acc_value))


    cdef c_symbol_numeric* _new_c_coordinate(self,
        c_string name,     c_string vel_name,     c_string acc_name,
        c_string tex_name, c_string vel_tex_name, c_string acc_tex_name,
        double   value,    double   vel_value,    double   acc_value):
        return self._c_handler.new_Coordinate(
            name, vel_name, acc_name,
            tex_name, vel_tex_name, acc_tex_name,
            c_numeric(value), c_numeric(vel_value), c_numeric(acc_value))




    ######## Constructors ########


    cpdef _new_symbol(self, kind, args, kwargs):
        # Validate & parse input arguments
        args = list(args)
        kind = _parse_symbol_type(kind)
        if kind in _derivable_symbol_types:
            raise ValueError(f'You cant create a {kind.decode().replace("_", " ")} symbol by hand')

        cdef c_symbol_numeric* c_symbol
        cdef c_symbol_numeric* vel_c_symbol
        cdef c_symbol_numeric* acc_c_symbol


        # Signature of the method depends on the type of symbol
        if kind in (b'parameter', b'input', b'joint_unknown'):
            # Parse optional arguments
            if not kwargs and len(args) == 2:
                if not isinstance(args[-1], (str, bytes)):
                    kwargs['value'] = args.pop()

            name, tex_name, value = _apply_signature(
                ['name', 'tex_name', 'value'],
                {'tex_name': b'', 'value': 0.0},
                args, kwargs
            )
            name, tex_name, value = _parse_name(name), _parse_tex_name(tex_name), _parse_numeric_value(value)

            # Check if a symbol with the name specified already exists
            if self._has_object(name):
                raise IndexError(f'Name "{name.decode()}" its already in use')

            # Apply a different constructor for each symbol type
            if kind == b'parameter':
                c_symbol = self._new_c_parameter(name, tex_name, value)
            elif kind == b'input':
                c_symbol = self._new_c_input(name, tex_name, value)
            elif kind == b'joint_unknown':
                c_symbol = self._new_c_joint_unknown(name, tex_name, value)

            return SymbolNumeric(<Py_ssize_t>c_symbol)


        elif kind.endswith(b'coordinate'):
            # Parse optional arguments
            if not kwargs and len(args) in range(1, 10):
                kwargs['name'] = args.pop(0)

                params = ['vel_name', 'acc_name', 'tex_name', 'vel_tex_name', 'acc_tex_name']
                while args and params and isinstance(args[0], (str, bytes)):
                    kwargs[params.pop(0)] = args.pop(0)

                params = ['value', 'vel_value', 'acc_value']
                while args and params:
                    kwargs[params.pop(0)] = args.pop(0)

            bounded_args = _apply_signature(
                ['name', 'vel_name', 'acc_name', 'tex_name', 'vel_tex_name', 'acc_tex_name', 'value', 'vel_value', 'acc_value'],
                {'vel_name': None, 'acc_name': None, 'tex_name': None, 'vel_tex_name': None, 'acc_tex_name': None,
                'value': 0.0, 'vel_value': 0.0, 'acc_value': 0.0},
                args, kwargs
            )

            names = [_parse_name(arg) if arg is not None else None for arg in bounded_args[:3]]
            tex_names = [_parse_tex_name(arg) if arg is not None else None for arg in bounded_args[3:6]]
            values = [_parse_numeric_value(arg) for arg in bounded_args[6:9]]

            names[1:] = [name or b'd'*k + names[0] for k, name in enumerate(names[1:], 1)]
            if tex_names[0]:
                tex_names[1:] = [tex_name or b'\\' + b'd'*k + b'ot{' + tex_names[0] + b'}' for k, tex_name in enumerate(tex_names[1:], 1)]
            else:
                tex_names = [tex_name or b'' for tex_name in tex_names]


            # Check if the name of the coordinate or its components is already in use by other symbol
            for name in names:
                if self._has_object(name):
                    raise IndexError(f'Name "{name.decode()}" its already in use')

            # Apply a different constructor for each symbol type
            if kind.startswith(b'aux_'):
                c_symbol = self._new_c_aux_coordinate(names[0], names[1], names[2], tex_names[0], tex_names[1], tex_names[2], values[0], values[1], values[2])
                vel_c_symbol, acc_c_symbol = self._c_handler.get_AuxVelocity(names[1]), self._c_handler.get_AuxAcceleration(names[2])
            else:
                c_symbol = self._new_c_coordinate(names[0], names[1], names[2], tex_names[0], tex_names[1], tex_names[2], values[0], values[1], values[2])
                vel_c_symbol, acc_c_symbol = self._c_handler.get_Velocity(names[1]), self._c_handler.get_Acceleration(names[2])

            return SymbolNumeric(<Py_ssize_t>c_symbol), SymbolNumeric(<Py_ssize_t>vel_c_symbol), SymbolNumeric(<Py_ssize_t>acc_c_symbol)

        else:
            raise RuntimeError




    cpdef _new_base(self, name, args, kwargs):
        # Validate & parse base name
        name = _parse_name(name)

        # Check if a base with the given name already exists
        if self._has_object(name):
            raise IndexError(f'Name "{name.decode()}" its already in use')

        # Validate & parse previous base, rotation tupla and angle arguments
        args = list(args)

        if args:
            new_args = []
            if not isinstance(args[0], (str, bytes, Base)):
                new_args.append(None)
            else:
                new_args.append(args.pop(0))

            if len(args) > 2:
                rotation_tupla = args[:3]
                args = args[3:]
                new_args.append(rotation_tupla)
            new_args.extend(args)
            args = new_args

        previous, rotation_tupla, rotation_angle = _apply_signature(
            ['previous', 'rotation_tupla', 'rotation_angle'],
            {'previous': None, 'rotation_tupla': (0, 0, 0), 'rotation_angle': 0},
            args, kwargs
        )

        if previous is not None:
            if not isinstance(previous, Base):
                try:
                    previous = self._get_base(previous)
                except IndexError as e:
                    raise ValueError(*e.args)
        else:
            previous = self._get_base(b'xyz')

        if not isinstance(rotation_tupla, (Iterable, Matrix)):
            raise TypeError(f'Rotation tupla must be an iterable or a Matrix object')

        if len(rotation_tupla) != 3:
            raise ValueError(f'Rotation tupla must have exactly three components')

        rotation_tupla = tuple(rotation_tupla)
        rotation_tupla = tuple(map(Expr, rotation_tupla))
        rotation_angle = Expr(rotation_angle)

        # Finally create the base
        cdef c_ex a, b, c, d
        cdef c_Base* c_prev_base

        c_prev_base = (<Base>previous)._c_handler
        a = (<Expr>rotation_tupla[0])._c_handler
        b = (<Expr>rotation_tupla[1])._c_handler
        c = (<Expr>rotation_tupla[2])._c_handler
        d = (<Expr>rotation_angle)._c_handler

        return Base(<Py_ssize_t>self._c_handler.new_Base(name, c_prev_base.get_name(), a, b, c, d))



    cpdef _new_matrix(self, name, args, kwargs):
        # Validate & parse name argument
        name = _parse_name(name)

        # Check if a matrix with the same name already exists
        if self._has_object(name):
            raise IndexError(f'Name "{name.decode()}" its already in use')

        # Create the matrix
        matrix = Matrix(*args, **kwargs)

        # Register the matrix with the given name in the system
        cdef c_Matrix* c_matrix = matrix._get_c_handler()
        c_matrix.set_name(name)
        self._c_handler.new_Matrix(c_matrix)
        (<Matrix>matrix)._owns_c_handler = False

        return matrix



    cpdef _new_vector(self, name, args, kwargs):
        # Validate & parse name argument
        name = _parse_name(name)

        # Check if a matrix with the same name already exists
        if self._has_object(name):
            raise IndexError(f'Name "{name.decode()}" its already in use')

        # Create the vector
        kwargs['system'] = self
        vector = Vector3D(*args, **kwargs)

        # Register the matrix with the given name in the system
        cdef c_Vector3D* c_vector = <c_Vector3D*>vector._get_c_handler()
        c_vector.set_name(name)
        self._c_handler.new_Vector3D(c_vector)
        (<Vector3D>vector)._owns_c_handler = False

        return vector
