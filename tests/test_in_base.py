'''
Author: Víctor Ruiz Gómez
Description: Unitary tests for base change operations (in_base) and default symbols
'''

import pytest
from lib3d_mec_ginac import *


def test_vector_in_base():
    '''
    Test vector.in_base() using both string names and Base objects,
    including the exported default base 'xyz'.
    '''
    # Create coordinate theta
    theta = new_coord('theta')[0]

    # Create a new base rotated around Z by angle theta
    b1 = new_base('b1', 'xyz', 0, 0, 1, theta)
    assert b1.name == 'b1'

    # Create unit vector along X in base b1
    v = new_vector('v', 1, 0, 0, b1)
    assert v.base.name == 'b1'

    # 1. in_base using Base object
    v_in_xyz_obj = v.in_base(get_base('xyz'))
    assert v_in_xyz_obj.base.name == 'xyz'

    # 2. in_base using string name
    v_in_xyz_str = v.in_base('xyz')
    assert v_in_xyz_str.base.name == 'xyz'

    # 3. in_base using exported global variable xyz
    v_in_xyz_var = v.in_base(xyz)
    assert v_in_xyz_var.base.name == 'xyz'

    # Verify all results are equal
    diff_str = v_in_xyz_obj - v_in_xyz_str
    diff_var = v_in_xyz_obj - v_in_xyz_var

    # Evaluate at theta = 0 to verify numerical values
    import numpy as np
    assert np.allclose(evaluate(diff_str), 0.0)
    assert np.allclose(evaluate(diff_var), 0.0)

    # Verify back-transformation to b1
    v_back = v_in_xyz_str.in_base('b1')
    assert v_back.base.name == 'b1'
    diff_back = v - v_back
    assert np.allclose(evaluate(diff_back), 0.0)

    # Verify invalid base argument raises appropriate error
    with pytest.raises(TypeError):
        v.in_base(123)

    with pytest.raises(IndexError):
        v.in_base('non_existent_base')


def test_exported_symbols():
    '''
    Test that default system properties xyz, O, and abs are exported and accessible.
    '''
    # xyz must be a Base object with name 'xyz'
    assert isinstance(xyz, Base)
    assert xyz.name == 'xyz'

    # O must be a Point object
    assert isinstance(O, Point)

    # abs must be a Frame object
    assert isinstance(abs, Frame)
