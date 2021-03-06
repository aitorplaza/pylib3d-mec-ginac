'''
Author: Víctor Ruiz Gómez
Description: Benchmark to evaluate the performance of numeric functions evaluation.
'''

from lib3d_mec_ginac import *
import timeit
from tabulate import tabulate
from itertools import count
from operator import methodcaller


# The next code is used to define a symbolic matrix for the benchmark

theta1, dtheta1, ddtheta1 = new_coord('theta1', -pi/6, 0)
theta2, dtheta2, ddtheta2 = new_coord('theta2', -2*pi/6, 0)
theta3, dtheta3, ddtheta3 = new_coord('theta3', -3*pi/6, 0)
l1, l2 = new_param('l1', 0.4), new_param('l2', 2.0)
l3, l4 = new_param('l3', 1.2), new_param('l4', 1.6)
new_base('Barm1', 'xyz', [0, 1, 0], theta1)
new_base('Barm2', 'Barm1', 0, 1, 0, theta2)
new_base('Barm3', 'Barm2', rotation_tupla=[0, 1, 0], rotation_angle=theta3)
new_vector('OA', l1, 0, 0, 'Barm1')
new_vector('AB', l2, 0, 0, 'Barm2')
new_vector('BC', [l3, 0, 0], 'Barm3')
new_vector('OO2', values=[l4, 0, 0], base='xyz')
new_point('A',  'O', 'OA')
new_point('B',  'A', 'AB')
new_point('C',  'B', 'BC')
new_point('O2', 'O', 'OO2')
m1, m2, m3 = new_param('m1', 1), new_param('m2', 1), new_param('m3', 1)
cg1x, cg1z = new_param('cg1x', 0.2), new_param('cg1z', 0.1)
cg2x, cg2z = new_param('cg2x', 1),   new_param('cg2z', 0.1)
cg3x, cg3z = new_param('cg3x', 0.6), new_param('cg3z', 0.1)
new_vector('OArm1_GArm1', cg1x, 0, cg1z, 'Barm1')
new_vector('OArm2_GArm2', cg2x, 0, cg2z, 'Barm2')
new_vector('OArm3_GArm3', cg3x, 0, cg3z, 'Barm3')
I1yy, I2yy, I3yy = [new_param(name, 1) for name in ('I1yy', 'I2yy', 'I3yy')]
I_Arm1 = new_tensor('Iarm1', base='Barm1')
I_Arm2 = new_tensor('Iarm2', base='Barm2')
I_Arm3 = new_tensor('Iarm3', base='Barm3')
I_Arm1[1, 1], I_Arm2[1, 1], I_Arm3[1, 1] = I1yy, I2yy, I3yy
new_frame('FArm1',    'O',  'Barm1')
new_frame('FArm2',    'A',  'Barm2')
new_frame('FArm3',    'B',  'Barm3')
new_frame('Fra_ABS2', 'O2', 'xyz')
new_solid('Arm1', 'O', 'Barm1', 'm1', 'OArm1_GArm1', 'Iarm1')
new_solid('Arm2', 'A', 'Barm2', 'm2', 'OArm2_GArm2', 'Iarm2')
new_solid('Arm3', 'B', 'Barm3', 'm3', 'OArm3_GArm3', 'Iarm3')
new_unknown('lambda1')
new_unknown('lambda2')
Fx2, Fz2 = new_input('Fx2'), new_input('Fz2')
Fx3, Fz3 = new_input('Fx3'), new_input('Fz3')
My2, My3 = new_input('My2'), new_input('My3')
new_vector('Fext2', Fx2, 0,   Fz2, 'xyz')
new_vector('Fext3', Fx3, 0,   Fz3, 'xyz')
new_vector('Mext2', 0,   My2, 0,   'xyz')
new_vector('Mext3', 0,   My3, 0,   'xyz')
K   = new_param('k',     50)
l2x = new_param('l2x',    1)
l3x = new_param('l3x',  0.5)
l3z = new_param('l3z',  0.1)
new_vector('OArm2_L2',  l2x, 0, 0,   'Barm2')
new_vector('OArm3_L3',  l3x, 0, l3z, 'Barm3')
new_point('OL2', 'A', 'OArm2_L2')
new_point('OL3', 'B', 'OArm3_L3')
OL2_OL3 = position_vector('OL2', 'OL3')
FK = K * OL2_OL3
MK = new_vector('MK_GroundPend1', 0, 0, 0, 'xyz')
Gravity_Arm1 = gravity_wrench('Arm1')
Gravity_Arm2 = gravity_wrench('Arm2')
Gravity_Arm3 = gravity_wrench('Arm3')
Inertia_Arm1 = inertia_wrench('Arm1')
Inertia_Arm2 = inertia_wrench('Arm2')
Inertia_Arm3 = inertia_wrench('Arm3')
SpringA = new_wrench('SpringA', FK,   MK, 'OL2', 'Arm2', 'Constitutive')
SpringR = new_wrench('SpringR', -FK, -MK, 'OL3', 'Arm3', 'Constitutive')
FMext2 = new_wrench('FMext2', 'Fext2', 'Mext2', 'A', 'Arm2', 'External')
FMext3 = new_wrench('FMext3', 'Fext3', 'Mext3', 'B', 'Arm3', 'External')
Sum_Wrenches_Arm1 = Inertia_Arm1 + Gravity_Arm1
Sum_Wrenches_Arm2 = Inertia_Arm2 + Gravity_Arm2 + SpringA - FMext2
Sum_Wrenches_Arm3 = Inertia_Arm3 + Gravity_Arm3 - SpringA + FMext3
Twist_Arm1, Twist_Arm2, Twist_Arm3 = twist('Arm1'), twist('Arm2'), twist('Arm3')
q,   q_aux   = get_coords_matrix(),        get_aux_coords_matrix()
dq,  dq_aux  = get_velocities_matrix(),    get_aux_velocities_matrix()
ddq, ddq_aux = get_accelerations_matrix(), get_aux_accelerations_matrix()
epsilon      = get_unknowns_matrix()
param        = get_params_matrix()
input        = get_inputs_matrix()
O2C = position_vector('O2', 'C')
e_x = new_vector('e_x', 1, 0, 0, 'xyz')
e_z = new_vector('e_z', 0, 0, 1, 'xyz')
Phi = Matrix(shape=[2, 1])
Phi[0] = O2C * e_x
Phi[1] = O2C * e_z
dPhi = derivative(Phi)
ddPhi = derivative(dPhi)
beta = -dPhi
beta = subs(beta, dq, 0)
beta = subs(beta, dq_aux, 0)
Phi_q = jacobian(Phi.transpose(), Matrix.block(2, 1, q, q_aux))
dPhi_dq = jacobian(dPhi.transpose(), Matrix.block(2, 1, dq, dq_aux))
gamma = -ddPhi
gamma = subs(gamma, ddq, 0)
gamma = subs(gamma, ddq_aux, 0)
Phi_init = Matrix([theta1 + pi / 2])
dPhi_init = Matrix([dtheta1 + pi / 2])



# Now we create the numeric function to measure its evaluation performance (optimized and unoptimized version)
print("Generating numeric functions...")
func = compile_numeric_function(gamma, c_optimized=False)
func_optimized = compile_numeric_function(gamma, c_optimized=True)




# Print atomization state on/off and python debug mode
print(f"Atomization is {'enabled' if get_atomization_state() == 1 else 'disabled'}")
print(f"Python debug mode is {'enabled' if __debug__ else 'disabled'}")
print()

# Start benchmark & print time metrics
print("Starting benchmark...")
n = 10000
result = min(timeit.repeat(lambda: func.evaluate(), repeat=10, number=n)) / n
print("Average evaluation time (unoptimized): {:5f} milliseconds".format(result*1000))
result = min(timeit.repeat(lambda: func_optimized.evaluate(), repeat=10, number=n)) / n
print("Average evaluation time (optimized): {:5f} milliseconds".format(result*1000))
