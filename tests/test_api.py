'''
Author: Víctor Ruiz Gómez
Description:
This file provides test cases to check that all public functions & classes of
the library are avaliable for the user (can be imported from the API)
'''

import pytest
from functools import partial
from operator import attrgetter, concat


######## Helper functions ########


namegetter = attrgetter('__name__')
qualnamegetter = attrgetter('__qualname__')


def propnamegetter(prop):
    assert isinstance(prop, property) or type(prop).__name__ == 'getset_descriptor'
    if isinstance(prop, property):
        return prop.fget.__name__
    return prop.__name__

def propqualnamegetter(prop):
    assert isinstance(prop, property) or type(prop).__name__ == 'getset_descriptor'
    if isinstance(prop, property):
        return prop.fget.__qualname__
    return prop.__qualname__





######## Tests ########


def test_classes(classes):
    '''
    This test checks that the next classes are avaliable:
    SymbolNumeric, Expr, Base, Matrix, Vector3D, Tensor3D, Wrench3D, Drawing3D,
    Point, Frame, Solid, Object, System
    '''
    assert {
        'SymbolNumeric', 'Expr', 'Base', 'Matrix', 'Vector3D', 'Tensor3D', 'Wrench3D',
        'Drawing3D', 'Point', 'Frame', 'Solid', 'Object', 'System'
    }.issubset(set(map(namegetter, classes)))



def test_methods(methods):
    '''
    This test checks that all the methods of the classes in the public API
    are avaliable
    '''
    public_methods = {
        'System': [
            'get_value', 'set_value',
            'get_symbol', 'get_time',
            'get_coordinate', 'get_velocity', 'get_acceleration',
            'get_aux_coordinate', 'get_aux_velocity', 'get_aux_acceleration',
            'get_parameter', 'get_joint_unknown', 'get_input',
            'get_base', 'get_matrix', 'get_vector', 'get_tensor', 'get_point',
            'get_frame', 'get_solid', 'get_wrench', 'get_drawing',

            'has_symbol',
            'has_coordinate', 'has_velocity', 'has_acceleration',
            'has_aux_coordinate', 'has_aux_velocity', 'has_aux_acceleration',
            'has_parameter', 'has_joint_unknown', 'has_input',
            'has_base', 'has_matrix', 'has_vector', 'has_tensor', 'has_point',
            'has_frame', 'has_solid', 'has_wrench', 'has_drawing',

            'get_symbols',
            'get_coordinates', 'get_velocities', 'get_accelerations',
            'get_aux_coordinates', 'get_aux_velocities', 'get_aux_accelerations',
            'get_parameters', 'get_joint_unknowns', 'get_inputs',
            'get_bases', 'get_matrices', 'get_vectors', 'get_tensors',
            'get_points', 'get_frames', 'get_solids', 'get_wrenches', 'get_drawings',

            'get_symbols_matrix',
            'get_coordinates_matrix', 'get_velocities_matrix', 'get_accelerations_matrix',
            'get_aux_coordinates_matrix', 'get_aux_velocities_matrix', 'get_aux_accelerations_matrix',

            'new_coordinate', 'new_aux_coordinate',
            'new_parameter', 'new_joint_unknown', 'new_input',
            'new_base', 'new_matrix', 'new_vector', 'new_tensor',
            'new_point', 'new_frame', 'new_solid', 'new_wrench', 'new_drawing',

            'reduced_base', 'reduced_point', 'pre_point_branch', 'rotation_matrix',
            'position_vector', 'angular_velocity', 'angular_velocity_tensor',
            'velocity_vector', 'angular_acceleration', 'acceleration_vector', 'twist',
            'derivative', 'jacobian', 'diff', 'gravity_wrench', 'inertia_wrench',

            'set_as_default'
        ],

        'SymbolNumeric': [
            '__complex__', '__float__', '__int__',
            'get_owner', 'get_tex_name', 'get_type', 'get_value',
            'set_tex_name', 'set_value',
            '__neg__', '__pos__', '__add__', '__sub__',
            '__mul__', '__truediv__', '__pow__'
        ],

        'Expr': [
            'eval',
            '__neg__', '__pos__', '__add__', '__sub__',
            '__mul__', '__truediv__', '__pow__',
            '__iadd__', '__isub__', '__imul__', '__itruediv__',
            '__eq__'
        ],

        'Base': [
            'get_previous_base', 'has_previous_base', 'get_rotation_angle',
            'get_rotation_tupla'
        ],

        'Matrix': [
            'get_shape', 'get_num_rows', 'get_num_cols', 'get_size', '__len__',
            'get_values', 'get', '__getitem__', 'set', '__setitem__',
            '__iter__', '__reversed__',
            '__pos__', '__neg__', '__add__', '__sub__',
            '__mul__', '__truediv__',
            'subs', 'transpose', 'get_transposed'
        ],

        'Vector3D': [
            'get_module', 'get_skew',
            'in_base', 'dot', 'cross',
            '__pos__', '__neg__', '__add__', '__sub__',
            '__mul__', '__truediv__', '__xor__'
        ],

        'Tensor3D': [
            'in_base',
            '__pos__', '__neg__', '__add__', '__sub__',
            '__mul__', '__truediv__'
        ],

        'Wrench3D': [
            'get_force', 'get_moment', 'get_solid', 'get_type', 'get_point',
            'unatomize', 'at_point',
            '__pos__', '__neg__',
            '__add__', '__sub__', '__mul__', '__truediv__'
        ],

        'Drawing3D': [
            'get_file', 'get_type', 'get_color', 'get_point', 'get_scale', 'get_vector',
            'set_file', 'set_color', 'set_scale', 'set_vector'
        ],

        'Point': [
            'get_position_vector', 'get_position', 'get_previous', 'has_previous'
        ],

        'Frame': [
            'get_point', 'get_scale', 'set_point'
        ],

        'Solid': [
            'get_CM', 'get_IT', 'get_G', 'get_mass'
        ]
    }

    qualnames = frozenset(map(qualnamegetter, methods))

    for class_name, names in public_methods.items():
        for name in names:
            if class_name + '.' + name not in qualnames:
                raise AssertionError(f'Missing method "{name}" in class "{class_name}"')





def test_system_properties(properties):
    '''
    This method checks that all properties defined by any of the API of the classes of this
    library are avaliable
    '''

    public_properties = {
        'System': [
            'symbols',
            'time',
            'coordinates', 'velocities', 'accelerations',
            'aux_coordinates', 'aux_velocities', 'aux_accelerations',
            'parameters', 'joint_unknowns', 'inputs',
            'bases', 'matrices', 'vectors', 'tensors', 'points',
            'frames', 'solids', 'wrenches', 'drawings', 'autogen_latex_names'
        ],

        'SymbolNumeric': [
            'owner', 'tex_name', 'type', 'value'
        ],

        'Base': [
            'previous_base', 'previous', 'rotation_tupla', 'rotation_angle'
        ],

        'Matrix': [
            'shape', 'num_rows', 'num_cols', 'size', 'T', 'transposed', 'values'
        ],

        'Vector3D': [
            'module', 'skew', 'x', 'y', 'z'
        ],

        'Wrench3D': [
            'force', 'moment', 'solid', 'type', 'point'
        ],

        'Drawing3D': [
            'file', 'point', 'scale', 'type', 'vector', 'color'
        ],

        'Point': [
            'position_vector', 'position', 'previous'
        ],

        'Frame': [
            'point', 'scale'
        ],

        'Solid': [
            'CM', 'IT', 'G', 'mass'
        ]
    }

    qualnames = frozenset(map(propqualnamegetter, properties))

    for class_name, names in public_properties.items():
        for name in names:
            if class_name + '.' + name not in qualnames:
                raise AssertionError(f'Missing property "{name}" in class "{class_name}"')




def test_global_functions(global_functions):
    '''
    This test checks that all global functions in the public API are avaliable in the
    library
    '''
    public_global_functions = [
        'get_default_system', 'set_default_system',
        'set_atomization_state', 'enable_atomization', 'disable_atomization',
        'get_atomization_state',
        'set_gravity_direction', 'set_gravity_up', 'set_gravity_down',
        'get_gravity_direction',
        'unatomize', 'subs',
        'dot', 'cross'
    ]

    names = frozenset(map(namegetter, global_functions))
    for name in public_global_functions:
        if name not in names:
            raise AssertionError(f'Missing global function "{name}"')
