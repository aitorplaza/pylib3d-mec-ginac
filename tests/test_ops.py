'''
Author: Víctor Ruiz Gómez
Description: This is a test for the arithmetic operations between numbers,
numeric symbols, expressions, matrices, vectors, tensors & wrenches
'''

######## Imports ########

import numpy as np
import pytest
from lib3d_mec_ginac import *
import operator
from inspect import isclass
from itertools import filterfalse, product



######## Fixture ########

@pytest.fixture(scope='module')
def operands(system):
    sys = system
    cte = 2
    symbol = sys.get_symbol('a')
    expr = (symbol ** 2 + 1) / 4
    matrix = Matrix([symbol, expr])
    vector = sys.get_vector('v')
    tensor = sys.get_tensor('q')
    wrench = sys.get_wrench('w')

    return np.array([
        cte,
        symbol,
        expr,
        matrix,
        vector,
        tensor,
        wrench
    ])



######## Auxiliar functions ########


def check_binary_op(op, operands, results):
    '''
    This is a helper function to test a binary operand with the specified operands.
    :param op: Must be a function taking as arguments the operands and performing the binary
        operation.
    :param operands: Must be a non empty array of size 1xn with n > 0.
    :param results: Must be an array of size nxn with n > 0
        The item at the i-th row and j-th column must be:
            * A class. That will indicate the the operation between the i-th and j-th column
                must have a value which is an instance of the given class
            * None: If the operation between the i-th and j-th operands is not supported.
            * Ellipse ( ... ): Means that no check will be performed between the i-th and j-th operands.
    '''

    assert callable(op)
    assert isinstance(operands, np.ndarray) and operands.ndim == 1
    assert isinstance(results, np.ndarray) and results.ndim == 2
    n = len(operands)
    assert results.shape == (n, n)

    try:
        next(filterfalse(lambda result: isclass(result) or result in (None, Ellipsis), results.flat))
        raise AssertionError('Results table is not valid')
    except StopIteration:
        pass

    for i, j in product(range(0, n), range(0, n)):
        a, b = operands[i], operands[j]
        expected = results[i, j]
        if expected is Ellipsis:
            continue

        try:
            got = op(a, b)
            if expected is None:
                raise AssertionError(f'{op.__name__} operation shouldnt be implemented with {type(a).__name__} and {type(b).__name__} as operands')
            elif not isinstance(got, expected):
                raise AssertionError(f'{op.__name__} operation result between {type(a).__name__} and {type(b).__name__} should be {expected.__name__}')
        except AssertionError:
            pass
        except:
            if expected is not None:
                raise AssertionError(f'{op.__name__} operation should be implemented with {type(a).__name__} and {type(b).__name__} as operands')



######## Tests for binary operations ########


def test_sum_subtract(operands):
    '''
    This is a test for the add & sub binary operations between numbers, symbols,
    expressions, matrices, vectors, tensors, wrenches.
    '''
    results = np.array([
        # cte      symbol     expr      matrix      vector,     tensor,     wrench
        [ ...,     Expr,      Expr,     None,       None,       None,       None     ],  # cte
        [ Expr,    Expr,      Expr,     None,       None,       None,       None     ],  # symbol
        [ Expr,    Expr,      Expr,     None,       None,       None,       None     ],  # expr
        [ None,    None,      None,     Matrix,     ...,        ...,        ...      ],  # matrix
        [ None,    None,      None,     ...,        Vector3D,   ...,        ...      ],  # vector
        [ None,    None,      None,     ...,        ...,        Tensor3D,   ...      ],  # tensor
        [ None,    None,      None,     ...,        ...,        ...,        Wrench3D ]   # wrench
    ])
    check_binary_op(operator.add, operands, results)
    check_binary_op(operator.sub, operands, results)



def test_mult(operands):
    '''
    This is a test for the mult binary operation between numbers, symbols,
    expressions, matrices, vectors, tensors, wrenches.
    '''
    results = np.array([
        # cte        symbol     expr      matrix      vector,     tensor,     wrench
        [ ...,       Expr,      Expr,     Matrix,     Vector3D,   Tensor3D,   Wrench3D ],  # cte
        [ Expr,      Expr,      Expr,     Matrix,     Vector3D,   Tensor3D,   Wrench3D ],  # symbol
        [ Expr,      Expr,      Expr,     Matrix,     Vector3D,   Tensor3D,   Wrench3D ],  # expr
        [ Matrix,    Matrix,    Matrix,   ...,        None,       None,       None     ],  # matrix
        [ Vector3D,  Vector3D,  Vector3D, None,       Expr,       None,       None     ],  # vector
        [ Tensor3D,  Tensor3D,  Tensor3D, None,       Vector3D,   Tensor3D,   None     ],  # tensor
        [ Wrench3D,  Wrench3D,  Wrench3D, None,       None,       None,       Wrench3D ]   # wrench
    ])
    check_binary_op(operator.mul, operands, results)


    # Product between matrices are also supported, but shapes of the input operands must match
    a, b, c = Matrix(shape=[3,4]), Matrix(shape=[4, 5]), Matrix(shape=[5, 6])
    d = a * b
    assert isinstance(d, Matrix) and d.get_shape() == (3, 5)
    d = b * c
    assert isinstance(d, Matrix) and d.get_shape() == (4, 6)
    with pytest.raises(TypeError):
        a * c




def test_div(operands):
    '''
    This is a test for the div binary operation between numbers, symbols,
    expressions, matrices, vectors, tensors, wrenches.
    '''
    results = np.array([
        # cte        symbol     expr      matrix      vector,     tensor,     wrench
        [ ...,       Expr,      Expr,     None,       None,       None,       None     ],  # cte
        [ Expr,      Expr,      Expr,     None,       None,       None,       None     ],  # symbol
        [ Expr,      Expr,      Expr,     None,       None,       None,       None     ],  # expr
        [ Matrix,    Matrix,    Matrix,   None,       None,       None,       None     ],  # matrix
        [ Vector3D,  Vector3D,  Vector3D, None,       None,       None,       None     ],  # vector
        [ Tensor3D,  Tensor3D,  Tensor3D, None,       None,       None,       None     ],  # tensor
        [ Wrench3D,  Wrench3D,  Wrench3D, None,       None,       None,       None     ]   # wrench
    ])
    check_binary_op(operator.truediv, operands, results)



def test_pow(operands):
    '''
    This is a test for the power binary operation between numbers, symbols,
    expressions, matrices, vectors, tensors and wrenches
    '''
    results = np.array([
        # cte        symbol     expr      matrix      vector,     tensor,     wrench
        [ ...,       Expr,      Expr,     None,       None,       None,       None     ],  # cte
        [ Expr,      Expr,      Expr,     None,       None,       None,       None     ],  # symbol
        [ Expr,      Expr,      Expr,     None,       None,       None,       None     ],  # expr
        [ None,      None,      None,     None,       None,       None,       None     ],  # matrix
        [ None,      None,      None,     None,       None,       None,       None     ],  # vector
        [ None,      None,      None,     None,       None,       None,       None     ],  # tensor
        [ None,      None,      None,     None,       None,       None,       None     ]   # wrench
    ])
    check_binary_op(operator.pow, operands, results)





def test_unary_ops(system):
    '''
    This is a test to check unary operations with symbols, expressions,
    matrices, vectors, tensors and wrenches
    '''
    sys = system
    vector = sys.get_vector('v')
    tensor = sys.get_tensor('q')
    wrench = sys.get_wrench('w')
    symbol = sys.get_symbol('a')
    expr = (symbol ** 2) + 1
    matrix = Matrix([1, symbol, expr])

    assert -symbol == -1*symbol
    assert -expr == -1*expr
    assert (-matrix).values == (-1*matrix).values
    assert (-vector).values == (-1*vector).values
    assert (-tensor).values == (-1*tensor).values
