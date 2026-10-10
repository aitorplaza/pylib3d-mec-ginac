'''
Author: Víctor Ruiz Gómez
Description: This is a unitary test for the class NumericFunction
'''


######## Imports ########

from lib3d_mec_ginac import *
import pytest
import numpy as np
from functools import partial


######## Fixtures ########



######## Tests ########

def test_numeric_func_atomization_enabled():
    '''
    This test checks that the numeric function can be created and evaluated numerically
    with atomization enabled
    '''
    sys = System()
    # Test numeric function evaluation with atomization enabled
    set_atomization_state('on')
    a, b = sys.new_parameter('a', 2), sys.new_input('b', 3)
    m = Matrix([a, a ** 2 + 1, (a - b) / 4, a * b], shape=[2, 2])
    func = sys.compile_numeric_function(m)
    output = evaluate(func)
    assert isinstance(output, np.ndarray) and output.dtype == np.float64
    assert output.shape == m.shape
    assert list(map(pytest.approx, output.flat)) == [ 2, 5, -0.25, 6 ]



def test_numeric_func_atomization_disabled():
    '''
    This test checks that the numeric function can be created and evaluated numerically
    with atomization disabled
    '''
    sys = System()
    # Test numeric function evaluation with atomization disabled
    set_atomization_state('off')
    a, b = sys.new_parameter('a', 2), sys.new_input('b', 3)
    m = Matrix([a, a ** 2 + 1, (a - b) / 4, a * b], shape=[2, 2])
    func = sys.compile_numeric_function(m)
    output = evaluate(func)
    assert isinstance(output, np.ndarray) and output.dtype == np.float64
    assert output.shape == m.shape
    assert list(map(pytest.approx, output.flat)) == [ 2, 5, -0.25, 6 ]



def test_no_numpy_matrix_pending_deprecation_warning():
    '''
    Verifies that compile_numeric_function and evaluate do not emit
    PendingDeprecationWarning (from deprecated np.matrix in NumPy 2.x).
    '''
    import warnings
    sys = System()
    a, b = sys.new_parameter('a', 3), sys.new_parameter('b', 4)
    v = sys.new_vector('v', a, b, 0)

    with warnings.catch_warnings():
        warnings.simplefilter('error', PendingDeprecationWarning)
        func = sys.compile_numeric_function(v)
        res = sys.evaluate(v)
        assert isinstance(res, np.ndarray)
        assert res.shape == (3, 1)
        assert list(map(pytest.approx, res.flat)) == [3.0, 4.0, 0.0]

        # Also test direct execution of compiled func
        res_func = func()
        assert isinstance(res_func, np.ndarray)
        assert list(map(pytest.approx, res_func.flat)) == [3.0, 4.0, 0.0]
