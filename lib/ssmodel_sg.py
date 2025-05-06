import numpy as np
import sympy as sp

def ssmodel_sg(wbase, parasSG, steadyStateValuesX, steadyStateValuesU, isRef):
    # Define symbolic variables
    theta, wr, psid, psiq, Eq1, Ed1, psi1d, psi2q, P1, Pg, Pf, P2, vx, Efd = sp.symbols(
        'theta wr psid psiq Eq1 Ed1 psi1d psi2q P1 Pg Pf P2 vx Efd'
    )
    vbD, vbQ, wcom = sp.symbols('vbD vbQ wcom')
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
    D = parasSG['D']
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
    iod = (-psid + (Ld2 - Ll)/(Ld1 - Ll) * Eq1 + (Ld1 - Ld2)/(Ld1 - Ll) * psi1d) / Ld2
    ioq = (-psiq - (Lq2 - Ll)/(Lq1 - Ll) * Ed1 + (Lq1 - Lq2)/(Lq1 - Ll) * psi2q) / Lq2
    dw = wr - wset
    vAbs = sp.sqrt(vbd**2 + vbq**2)
    vError = Vset - vAbs
    Pm = P2 + K1*Pf
    Tm = Pm/wr
    # System equations
    f = sp.Matrix([
        wbase*(wr - wcom),
        1/(2*H)*(Tm - (psid*ioq - psiq*iod) - D*dw),
        wbase*(Rs*iod + wr*psiq + vbd),
        wbase*(Rs*ioq - wr*psid + vbq),
        1/Tdo1*(-Eq1 - (Ld - Ld1)*(iod - (Ld1 - Ld2)/(Ld1 - Ll)**2*(psi1d + (Ld1 - Ll)*iod - Eq1)) + Efd),
        1/Tqo1*(-Ed1 + (Lq - Lq1)*(ioq - (Lq1 - Lq2)/(Lq1 - Ll)**2*(psi2q + (Lq1 - Ll)*ioq + Ed1))),
        1/Tdo2*(-psi1d + Eq1 - (Ld1 - Ll)*iod),
        1/Tqo2*(-psi2q - Ed1 - (Lq1 - Ll)*ioq),
        1/T1*(-P1 - Kg*T2/T1*dw + Kg*dw),
        1/T3*(-P1 - Kg*T2/T1*dw - Pg + Pset),
        1/T4*(Pg - Pf),
        1/T5*(K2*Pf - P2),
        1/Tb*(-vx - Ta/Tb*vError + vError),
        1/Te*(Ke*vx + Ke*Ta/Tb*vError - Efd)
    ])
    # Output equations
    ioD = iod*sp.cos(theta) - ioq*sp.sin(theta)
    ioQ = iod*sp.sin(theta) + ioq*sp.cos(theta)
    # State and input vectors
    x = sp.Matrix([theta, wr, psid, psiq, Eq1, Ed1, psi1d, psi2q, P1, Pg, Pf, P2, vx, Efd])
    u = sp.Matrix([vbD, vbQ, wcom])
    # Calculate Jacobians
    Asym = f.jacobian(x)
    Bsym = f.jacobian(sp.Matrix([vbD, vbQ]))
    BwSym = f.jacobian(sp.Matrix([wcom]))
    Csym = sp.Matrix([ioD, ioQ]).jacobian(x)
    CwSym = wr.diff(x)
    # Substitute steady-state values
    subs_dict = dict(zip(list(x) + list(u), np.concatenate([steadyStateValuesX, steadyStateValuesU])))
    A = np.array(Asym.subs(subs_dict).evalf()).astype(np.float64)
    B = np.array(Bsym.subs(subs_dict).evalf()).astype(np.float64)
    Bw = np.array(BwSym.subs(subs_dict).evalf()).astype(np.float64)
    C = np.array(Csym.subs(subs_dict).evalf()).astype(np.float64)
    Cw = np.array(CwSym.subs(subs_dict).evalf()).astype(np.float64)
    if not isRef:
        Cw = np.zeros((1, len(x)))
    # State variable labels
    stateVariables = [
        ['theta', ''], ['wr', ''], ['psid', ''], ['psiq', ''],
        ['Eq1', ''], ['Ed1', ''], ['psi1d', ''], ['psi2q', ''],
        ['P1', ''], ['Pg', ''], ['Pf', ''], ['P2', ''],
        ['vx', ''], ['Efd', '']
    ]
    return {
        'A': A,
        'B': B,
        'Bw': Bw,
        'C': C,
        'Cw': Cw,
        'ssVariables': stateVariables
    }