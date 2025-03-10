import numpy as np
import sympy as sp


def ssmodel_sg(wbase, parasSG, steadyStateValuesX, steadyStateValuesU, isRef):
    # Define symbolic variables
    theta, wr, psid, psiq, Eq1, Ed1, psi1d, psi2q, P1, Pg, Pf, P2, vx, Efd = sp.symbols(
        'theta wr psid psiq Eq1 Ed1 psi1d psi2q P1 Pg Pf P2 vx Efd'
    )
    vbD, vbQ, wcom = sp.symbols('vbD vbQ wcom')

    # Extract parameters from parasSG (assumed to be a dictionary)
    wset = parasSG['wset']
    Pset = parasSG['Pset']
    Vset = parasSG['Vset']
    Rs = parasSG['Rs']
    Ld = parasSG['Ld']
    Ld1 = parasSG['Ld1']
    Ld2 = parasSG['Ld2']
    Lq = parasSG['Lq']
    Lq1 = parasSG['Lq1']
    Lq2 = parasSG['Lq2']
    Ll = parasSG['Ll']
    Tdo1 = parasSG['Tdo1']
    Tqo1 = parasSG['Tqo1']
    Tdo2 = parasSG['Tdo2']
    Tqo2 = parasSG['Tqo2']
    H = parasSG['H']
    D_param = parasSG['D']
    Kg = parasSG['Kg']
    T1 = parasSG['T1']
    T2 = parasSG['T2']
    T3 = parasSG['T3']
    T4 = parasSG['T4']
    T5 = parasSG['T5']
    K1 = parasSG['K1']
    K2 = parasSG['K2']
    Ta = parasSG['Ta']
    Tb = parasSG['Tb']
    Ke = parasSG['Ke']
    Te = parasSG['Te']

    # Algebraic equations
    vbd = vbD * sp.cos(theta) + vbQ * sp.sin(theta)
    vbq = -vbD * sp.sin(theta) + vbQ * sp.cos(theta)
    iod = (-psid + (Ld2 - Ll) / (Ld1 - Ll) * Eq1 + (Ld1 - Ld2) / (Ld1 - Ll) * psi1d) / Ld2
    ioq = (-psiq - (Lq2 - Ll) / (Lq1 - Ll) * Ed1 + (Lq1 - Lq2) / (Lq1 - Ll) * psi2q) / Lq2
    dw = wr - wset
    vAbs = sp.sqrt(vbd ** 2 + vbq ** 2)
    vError = Vset - vAbs
    Pm = P2 + K1 * Pf
    Tm = Pm / wr

    # Define the vector f of ODEs (14 equations)
    f1 = wbase * (wr - wcom)
    f2 = 1 / (2 * H) * (Tm - (psid * ioq - psiq * iod) - D_param * dw)
    f3 = wbase * (Rs * iod + wr * psiq + vbd)
    f4 = wbase * (Rs * ioq - wr * psid + vbq)
    f5 = 1 / Tdo1 * (
                -Eq1 - (Ld - Ld1) * (iod - (((Ld1 - Ld2) / (Ld1 - Ll)) ** 2) * (psi1d + (Ld1 - Ll) * iod - Eq1)) + Efd)
    f6 = 1 / Tqo1 * (-Ed1 + (Lq - Lq1) * (ioq - (((Lq1 - Lq2) / (Lq1 - Ll)) ** 2) * (psi2q + (Lq1 - Ll) * ioq + Ed1)))
    f7 = 1 / Tdo2 * (-psi1d + Eq1 - (Ld1 - Ll) * iod)
    f8 = 1 / Tqo2 * (-psi2q - Ed1 - (Lq1 - Ll) * ioq)
    f9 = 1 / T1 * (-P1 - Kg * T2 / T1 * dw + Kg * dw)
    f10 = 1 / T3 * (-P1 - Kg * T2 / T1 * dw - Pg + Pset)
    f11 = 1 / T4 * (Pg - Pf)
    f12 = 1 / T5 * (K2 * Pf - P2)
    f13 = 1 / Tb * (-vx - Ta / Tb * vError + vError)
    f14 = 1 / Te * (Ke * vx + Ke * Ta / Tb * vError - Efd)

    f = sp.Matrix([f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13, f14])

    # Additional algebraic outputs
    ioD = iod * sp.cos(theta) - ioq * sp.sin(theta)
    ioQ = iod * sp.sin(theta) + ioq * sp.cos(theta)

    # Define state vector and input vector
    x_sym = sp.Matrix([theta, wr, psid, psiq, Eq1, Ed1, psi1d, psi2q, P1, Pg, Pf, P2, vx, Efd])
    u_sym = sp.Matrix([vbD, vbQ, wcom])

    # Compute Jacobians
    Asym = f.jacobian(x_sym)
    Bsym = f.jacobian(sp.Matrix([vbD, vbQ]))
    BwSym = f.jacobian(sp.Matrix([wcom]))
    Csym = sp.Matrix([ioD, ioQ]).jacobian(x_sym)
    CwSym = sp.Matrix([wr]).jacobian(x_sym)

    # Create substitution dictionary for steady state values
    subs_dict = {}
    x_symbols = list(x_sym)
    for i, sym in enumerate(x_symbols):
        subs_dict[sym] = steadyStateValuesX[i]
    u_symbols = list(u_sym)
    for i, sym in enumerate(u_symbols):
        subs_dict[sym] = steadyStateValuesU[i]

    # Substitute steady state values and convert to numeric arrays
    A_sym = Asym.subs(subs_dict)
    B_sym = Bsym.subs(subs_dict)
    Bw_sym = BwSym.subs(subs_dict)
    C_sym = Csym.subs(subs_dict)
    Cw_sym = CwSym.subs(subs_dict)

    A = np.array(A_sym.tolist()).astype(np.float64)
    B = np.array(B_sym.tolist()).astype(np.float64)
    Bw = np.array(Bw_sym.tolist()).astype(np.float64)
    C = np.array(C_sym.tolist()).astype(np.float64)
    Cw = np.array(Cw_sym.tolist()).astype(np.float64)

    if isRef == 0:
        Cw = np.zeros((1, len(x_symbols)))

    # Define state variable labels
    stateVariables = ['theta', 'wr', 'psid', 'psiq', 'Eq1', 'Ed1', 'psi1d', 'psi2q', 'P1', 'Pg', 'Pf', 'P2', 'vx',
                      'Efd']

    stateMatrix = {
        'A': A,
        'B': B,
        'Bw': Bw,
        'C': C,
        'Cw': Cw,
        'ssVariables': stateVariables
    }
    return stateMatrix