import numpy as np
import sympy as sp

def ssmodel_droopSimplified(wbase, paras_inverter, steady_state_values_x, steady_state_values_u, is_ref):
    # Define symbolic variables
    theta, Po, Qo, iod, ioq = sp.symbols('theta Po Qo iod ioq')
    vbD, vbQ, wcom = sp.symbols('vbD vbQ wcom')

    # Parameters
    Pset = paras_inverter['Pset']
    Qset = paras_inverter['Qset']
    wset = paras_inverter['wset']
    Vset = paras_inverter['Vset']
    Rc = paras_inverter['Rc']
    Lc = paras_inverter['Lc']
    mp = paras_inverter['mp']
    mq = paras_inverter['mq']
    wc = paras_inverter['wc']

    # Algebraic equations
    winv = wset - mp*(Po - Pset)
    vodRef = Vset - mq*(Qo - Qset)
    voqRef = 0
    vbd = vbD*sp.cos(theta) + vbQ*sp.sin(theta)
    vbq = -vbD*sp.sin(theta) + vbQ*sp.cos(theta)

    # Ordinary differential equations
    f = sp.Matrix([
        wbase*(winv - wcom),
        -wc*Po + wc*(vodRef*iod + voqRef*ioq),
        -wc*Qo + wc*(voqRef*iod - vodRef*ioq),
        wbase*(vodRef - vbd - Rc*iod + winv*Lc*ioq)/Lc,
        wbase*(voqRef - vbq - Rc*ioq - winv*Lc*iod)/Lc
    ])

    ioD = iod*sp.cos(theta) - ioq*sp.sin(theta)
    ioQ = iod*sp.sin(theta) + ioq*sp.cos(theta)

    # State-Space Matrices
    state_variables = ['theta', 'Po', 'Qo', 'iod', 'ioq']
    x = sp.Matrix([theta, Po, Qo, iod, ioq])
    u = sp.Matrix([vbD, vbQ, wcom])

    Asym = f.jacobian(x)
    Bsym = f.jacobian(sp.Matrix([vbD, vbQ]))
    BwSym = f.jacobian(wcom)
    Csym = sp.Matrix([ioD, ioQ]).jacobian(x)
    CwSym = sp.diff(winv, x)

    # Substitute steady-state values
    subs_dict = dict(zip(list(x) + list(u), steady_state_values_x + steady_state_values_u))
    A = Asym.subs(subs_dict).evalf()
    B = Bsym.subs(subs_dict).evalf()
    Bw = BwSym.subs(subs_dict).evalf()
    C = Csym.subs(subs_dict).evalf()
    Cw = CwSym.subs(subs_dict).evalf()

    if not is_ref:
        Cw = sp.zeros(1, 5)

    # Output
    state_matrix = {
        'A': np.array(A).astype(np.float64),
        'B': np.array(B).astype(np.float64),
        'Bw': np.array(Bw).astype(np.float64),
        'C': np.array(C).astype(np.float64),
        'Cw': np.array(Cw).astype(np.float64),
        'ss_variables': state_variables
    }

    return state_matrix

