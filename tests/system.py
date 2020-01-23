
######## Imports ########

from lib3d_mec_ginac import *
from math import floor
from itertools import product
import pytest



######## Fixtures ########


@pytest.fixture(scope='session')
def system():
    '''
    This fixture creates a system with a few objects ( vectors, tensors, wrenches, ... )
    for testing purposes ( it is used in the tests below )
    The return system instance will have the next objects ( sorted by type ):
    - symbols:
        * parameters:      a, b
        * inputs:          c
        * joint_unknowns:  d
        * coordinates:     (x, dx, ddx)
        * aux_coordinates: (y, dy, ddy)

    - bases:    bs
    - vectors:  v
    - points:   p
    - tensors:  q
    - solids:   s
    - wrenches: w
    - frames:   f
    '''
    sys = System()

    # Fill system with symbols
    sys.new_parameter('a')
    sys.new_parameter('b')
    sys.new_input('c')
    sys.new_joint_unknown('d')
    sys.new_coordinate('x')
    sys.new_aux_coordinate('y')

    # Fill system with geometric objects
    sys.new_base('bs')
    sys.new_vector('v')
    sys.new_vector('r')
    sys.new_point('p', 'O', 'v')
    sys.new_tensor('q')
    sys.new_solid('s', 'p', 'bs', 'a', 'v', 'q')
    sys.new_frame('f', 'p', 'bs')
    sys.new_wrench('w', 'v', 'r', 'p', 's', 'Constraint')

    return sys





######## Tests ########


def test_symbol_value_setget(invalid_numeric_values, non_strings, system):
    '''
    This function is a test for the methods ``get_value`` and ``set_value`` in the
    class System
    '''
    sys = system
    a, b = sys.get_symbol('a'), sys.get_symbol('b')


    # Set the value of a symbol ( specify the symbol as an instance of the class SymbolNumeric )
    sys.set_value(a, 2)
    sys.set_value(b, 3)
    assert floor(sys.get_value(a)) == 2 and floor(sys.get_value(b)) == 3

    # Set the value of a symbol ( specify the symbol with its name )
    sys.set_value('a', 3)
    sys.set_value('b', 2)
    assert floor(sys.get_value('a') == 3) and floor(sys.get_value('b')) == 2

    # set_value and get_value raises IndexError if the first argument is a string and its
    # not the name of any symbol in the system
    with pytest.raises(IndexError):
        sys.set_value('foo', 1)

    with pytest.raises(IndexError):
        sys.get_value('bar')

    # set_value raises TypeError if the numeric value is not float nor int
    for x in invalid_numeric_values:
        with pytest.raises(TypeError):
            sys.set_value(a, x)

    # Raises TypeError if the first argument of get_value or set_value is not a SymbolNumeric
    # nor string
    for x in non_strings:
        with pytest.raises(TypeError):
            sys.set_value(x, 1)

        with pytest.raises(TypeError):
            sys.get_value(x)



######## Tests for getter methods ########


def test_get_symbol(non_strings, system):
    '''
    This function is a test for the method ``get_symbol`` in the class System
    '''
    sys = system

    # get_symbol returns SymbolNumeric instances
    for name in ('a', 'b', 'c', 'd'):
        assert isinstance(sys.get_symbol(name), SymbolNumeric)

    # get_symbol raises TypeError if the input argument is not string
    for x in non_strings:
        with pytest.raises(TypeError):
            sys.get_symbol(x)

    # get_symbol raises IndexError if the input argument is not the name of
    # an already existing symbol in the system
    with pytest.raises(IndexError):
        sys.get_symbol('foo')




def test_has_symbol(non_strings, system):
    '''
    This function is a test for the method ``has_symbol`` in the class System
    '''
    sys = system

    # has_symbol returns True if a symbol with the given name exists, False otherwise
    assert sys.has_symbol('a') and sys.has_symbol('b')
    assert not sys.has_symbol('foo') and not sys.has_symbol('bar')

    # has_symbol raises TypeError if the input argument is not a string
    for x in non_strings:
        with pytest.raises(TypeError):
            sys.has_symbol(x)




def test_get_base(non_strings, system):
    '''
    This function is a test for the method ``get_base`` in the class System
    '''
    sys = system

    assert isinstance(sys.get_base('bs'), Base)

    with pytest.raises(IndexError):
        sys.get_base('foo')

    for x in non_strings:
        with pytest.raises(TypeError):
            sys.get_base(x)



def test_get_vector(non_strings, system):
    '''
    This function is a test for the method ``get_vector`` in the class System
    '''
    sys = system
    assert isinstance(sys.get_vector('v'), Vector3D)

    with pytest.raises(IndexError):
        sys.get_vector('foo')

    for x in non_strings:
        with pytest.raises(TypeError):
            sys.get_vector(x)




def test_get_tensor(non_strings, system):
    '''
    This function is a test for the method ``get_tensor`` in the class System
    '''
    sys = system

    assert isinstance(sys.get_tensor('q'), Tensor3D)

    with pytest.raises(IndexError):
        sys.get_tensor('foo')

    for x in non_strings:
        with pytest.raises(TypeError):
            sys.get_tensor(x)





def test_get_point(non_strings, system):
    '''
    This function is a test for the method ``get_point`` in the class System
    '''
    sys = system

    assert isinstance(sys.get_point('p'), Point)

    with pytest.raises(IndexError):
        sys.get_point('foo')

    for x in non_strings:
        with pytest.raises(TypeError):
            sys.get_point(x)




def test_get_solid(non_strings, system):
    '''
    This function is a test for the method ``get_solid`` in the class System
    '''
    sys = system

    assert isinstance(system.get_solid('s'), Solid)

    with pytest.raises(IndexError):
        sys.get_solid('foo')

    for x in non_strings:
        with pytest.raises(TypeError):
            sys.get_solid(x)



def test_get_wrench(non_strings, system):
    '''
    This function is a test for the method ``get_wrench`` in the class System
    '''
    sys = system

    assert isinstance(sys.get_wrench('w'), Wrench3D)

    with pytest.raises(IndexError):
        sys.get_wrench('foo')

    for x in non_strings:
        with pytest.raises(TypeError):
            sys.get_wrench(x)




def test_get_frame(non_strings, system):
    '''
    This function is a test for the method ``get_frame`` in the class System
    '''
    sys = system

    assert isinstance(sys.get_frame('f'), Frame)

    with pytest.raises(IndexError):
        sys.get_wrench('foo')

    for x in non_strings:
        with pytest.raises(TypeError):
            sys.get_wrench(x)







######## Tests for construction methods ########


def test_new_param_unknown_input(non_strings, invalid_object_names, invalid_numeric_values):
    '''
    This function is a test for the methods ``new_parameter``,
    ``new_joint_unknown``, ``new_input`` in the class System
    '''
    # We can create a param passing only its name ( param value will be 0 )
    sys = System()
    symbols = [sys.new_parameter('a'), sys.new_joint_unknown('b'), sys.new_input('c')]
    for symbol in symbols:
        assert isinstance(symbol, SymbolNumeric)
        assert floor(sys.get_value(symbol)) == 0
    assert symbols[0].get_type() == 'parameter'
    assert symbols[1].get_type() == 'joint_unknown'
    assert symbols[2].get_type() == 'input'

    # We can create a param passing the name & value
    sys = System()
    symbols = [sys.new_parameter('a', 1), sys.new_joint_unknown('b', 1), sys.new_input('c', 1)]
    for symbol in symbols:
        assert isinstance(symbol, SymbolNumeric)
        assert floor(sys.get_value(symbol)) == 1

    # name should be a string ( also a valid python identifier )
    for x in non_strings:
        with pytest.raises(TypeError):
            sys.new_parameter(x)

    for x in invalid_object_names:
        with pytest.raises(ValueError):
            sys.new_parameter(x)

    # value should be a number ( float or int )
    for x in invalid_numeric_values:
        with pytest.raises(TypeError):
            sys.new_parameter('foo', value=x)




def test_new_coordinate():
    '''
    Test for the method ``new_coordinate`` in the class System
    '''
    # We can create a coordinate by only indicating its name ( numeric values of
    # the coordinate and its derivatives will be zero )
    sys = System()
    a, da, dda = sys.new_aux_coordinate('a')
    assert isinstance(a, SymbolNumeric) and isinstance(da, SymbolNumeric) and isinstance(dda, SymbolNumeric)
    assert floor(sys.get_value(a)) == 0 and floor(sys.get_value(da)) == 0 and floor(sys.get_value(dda)) == 0
    assert a.get_name() == 'a' and da.get_name() == 'da' and dda.get_name() == 'dda'

    # We can create the coordinate by indicating the name + one, two or three numeric values
    sys = System()
    a, da, dda = sys.new_aux_coordinate('a', 1)
    assert floor(sys.get_value(a)) == 1 and floor(sys.get_value(da)) == 0 and floor(sys.get_value(dda)) == 0

    b, db, ddb = sys.new_aux_coordinate('b', 1, 2)
    assert floor(sys.get_value(b)) == 1 and floor(sys.get_value(db)) == 2 and floor(sys.get_value(ddb)) == 0

    c, dc, ddc = sys.new_aux_coordinate('c', 1, 2, 3)
    assert floor(sys.get_value(c)) == 1 and floor(sys.get_value(dc)) == 2 and floor(sys.get_value(ddc)) == 3

    # Names can also be specified for the derivative components of the coordiante
    sys = System()
    a, da, dda = sys.new_aux_coordinate('a', 'b', 'c')
    assert a.get_name() == 'a' and da.get_name() == 'b' and dda.get_name() == 'c'

    # Names of the derivatives & numeric values can also be specified
    sys = System()
    a, da, dda = sys.new_aux_coordinate('a', 'b', 'c', 1, 2, 3)
    assert a.get_name() == 'a' and da.get_name() == 'b' and dda.get_name() == 'c'
    assert floor(sys.get_value(a)) == 1 and floor(sys.get_value(da)) == 2 and floor(sys.get_value(dda)) == 3




def test_new_aux_coordinate():
    '''
    Test for the method ``new_aux_coordinate`` in the class System
    '''
    # We can create a coordinate by only indicating its name ( numeric values of
    # the coordinate and its derivatives will be zero )
    sys = System()
    a, da, dda = sys.new_coordinate('a')
    assert isinstance(a, SymbolNumeric) and isinstance(da, SymbolNumeric) and isinstance(dda, SymbolNumeric)
    assert floor(sys.get_value(a)) == 0 and floor(sys.get_value(da)) == 0 and floor(sys.get_value(dda)) == 0
    assert a.get_name() == 'a' and da.get_name() == 'da' and dda.get_name() == 'dda'

    # We can create the coordinate by indicating the name + one, two or three numeric values
    sys = System()
    a, da, dda = sys.new_coordinate('a', 1)
    assert floor(sys.get_value(a)) == 1 and floor(sys.get_value(da)) == 0 and floor(sys.get_value(dda)) == 0

    b, db, ddb = sys.new_coordinate('b', 1, 2)
    assert floor(sys.get_value(b)) == 1 and floor(sys.get_value(db)) == 2 and floor(sys.get_value(ddb)) == 0

    c, dc, ddc = sys.new_coordinate('c', 1, 2, 3)
    assert floor(sys.get_value(c)) == 1 and floor(sys.get_value(dc)) == 2 and floor(sys.get_value(ddc)) == 3

    # Names can also be specified for the derivative components of the coordiante
    sys = System()
    a, da, dda = sys.new_coordinate('a', 'b', 'c')
    assert a.get_name() == 'a' and da.get_name() == 'b' and dda.get_name() == 'c'

    # Names of the derivatives & numeric values can also be specified
    sys = System()
    a, da, dda = sys.new_coordinate('a', 'b', 'c', 1, 2, 3)
    assert a.get_name() == 'a' and da.get_name() == 'b' and dda.get_name() == 'c'
    assert floor(sys.get_value(a)) == 1 and floor(sys.get_value(da)) == 2 and floor(sys.get_value(dda)) == 3





def test_new_base():
    pass


def test_new_matrix():
    pass


def test_new_vector():
    pass


def test_new_tensor():
    pass


def test_new_point():
    pass


def test_new_solid():
    pass


def test_new_wrench():
    pass


def test_new_frame():
    pass



######## Tests for symbolic computation methods ########



def test_derivative():
    '''
    Test to check the function ``derivative`` in the class System
    '''
    sys = System()

    # We can pass an expression, matrix or vector as the first argument
    # The type of result will be the same as the input type.
    v = sys.new_vector('v')
    b = sys.get_base('xyz')
    f = sys.get_frame('abs')
    m = Matrix(shape=[2, 2])
    assert isinstance(sys.derivative(Expr(1)), Expr)
    assert isinstance(sys.derivative(v), Vector3D)
    assert isinstance(sys.derivative(m), Matrix)

    # base argument can only be specified if the first argument is a vector
    assert isinstance(sys.derivative(v, base=b), Vector3D)
    assert isinstance(sys.derivative(v, base='xyz'), Vector3D)

    with pytest.raises(TypeError):
        sys.derivative(Expr(1), base=b)

    with pytest.raises(TypeError):
        sys.derivative(m, base=b)

    # frame argument can only be specified if the first argument is a vector

    assert isinstance(sys.derivative(v, frame=f), Vector3D)
    assert isinstance(sys.derivative(v, frame='abs'), Vector3D)

    with pytest.raises(TypeError):
        sys.derivative(Expr(1), frame=f)

    with pytest.raises(TypeError):
        sys.derivative(m, frame=f)


    # base & frame arguments cannot be specified at the same time
    with pytest.raises(TypeError):
        sys.derivative(v, base=b, frame=f)

    # If the first argument is a matrix, the resulting matrix should have the same size
    assert m.shape == sys.derivative(m).shape





def test_diff(system):
    '''
    Test to check the function ``diff`` in the class System
    '''
    sys = system
    a, b = sys.get_symbol('a'), sys.get_symbol('b')
    w = sys.get_wrench('w')
    m = Matrix(shape=[2, 2])



    # diff can take an expressions, matrix or wrenches as first argument
    # the type of the result will be the same as the first argument
    # the second argument must always be a numeric symbol
    assert isinstance(sys.diff(Expr(1), a), Expr)
    assert isinstance(sys.diff(m, a), Matrix)
    assert isinstance(sys.diff(Expr(1), 'a'), Expr)
    assert isinstance(sys.diff(m, 'a'), Matrix)
    assert isinstance(sys.diff(w, a), Wrench3D)
    assert isinstance(sys.diff(w, 'a'), Wrench3D)


    # If the first argument is a matrix, the resulting matrix should have the same size
    assert m.shape == sys.diff(m, a).shape





def test_jacobian(system):
    '''
    Test to check the function ``jacobian`` in the class System
    '''
    sys = system
    a, b = sys.get_symbol('a'), sys.get_symbol('b')
    m, q, r = Matrix([[a, b], [b, a]]), Matrix([a, b]), Matrix([b, a]).transpose()

    # method jacobian takes either two matrices ( a row matrix and a columnd matrix ) or a matrix and a symbol
    assert isinstance(sys.jacobian(q, r), Matrix)
    assert isinstance(sys.jacobian(q, a), Matrix)


    # ValueError is raised if two matrices are passed but the first one is not a matrix
    # row or the second one is not a column row

    with pytest.raises(ValueError):
        sys.jacobian(m, r)

    with pytest.raises(ValueError):
        sys.jacobian(q, m)

    with pytest.raises(ValueError):
        sys.jacobian(m, m)


    # If the second matrix specified has symbolic expressions which are not convertible
    # to "symbols" ( expressions composed only by one symbol ), ValueError is raised

    p = Matrix([ a**2, b**2 ]).transpose()
    with pytest.raises(ValueError):
        sys.jacobian(q, p)

    # Given two matrices with shapes 1xn and mx1, the resulting matrix should be nxm
    q = Matrix([ a ** 2, b ** 2, a + b ])
    p = Matrix([ a, b ]).transpose()

    assert sys.jacobian(q, p).shape == (3, 2)

    # Given a matrix with shape 1xn and a symbol, the resulting matrix should be a column
    # matrix with n items

    assert sys.jacobian(q, a).shape == (3, 1)





######## Tests for cinematic methods ########
