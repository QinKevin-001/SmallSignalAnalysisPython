import numpy as np
import sympy as sp

def ssmodel_droop(wbase, parasInverter, steadyStateValuesX, steadyStateValuesU, isRef):
    # Define symbolic variables
    theta, Po, Qo, phid, phiq, gammad, gammaq, iid, iiq, vcd, vcq, iod, ioq = sp.symbols('theta Po Qo phid phiq gammad gammaq iid iiq vcd vcq iod ioq')
    vbD, vbQ, wcom = sp.symbols('vbD vbQ wcom')

    # Parameters
    Pset = parasInverter['Pset']
    Qset = parasInverter['Qset']
    wset = parasInverter['wset']
    Vset = parasInverter['Vset']
    Rt = parasInverter['Rt']
    Lt = parasInverter['Lt']
    Rd = parasInverter['Rd']
    Cf = parasInverter['Cf']
    Rc = parasInverter['Rc']
    Lc = parasInverter['Lc']
    mp = parasInverter['mp']
    mq = parasInverter['mq']
    KpV = parasInverter['KpV']
    KiV = parasInverter['KiV']
    KpC = parasInverter['KpC']
    KiC = parasInverter['KiC']
    wc = parasInverter['wc']

    # Algebraic equations
    vod = vcd + Rd * (iid - iod)
    voq = vcq + Rd * (iiq - ioq)
    winv = wset - mp * (Po - Pset)
    vodRef = Vset - mq * (Qo - Qset)
    voqRef = 0
    vbd = vbD * sp.cos(theta) + vbQ * sp.sin(theta)
    vbq = -vbD * sp.sin(theta) + vbQ * sp.cos(theta)
    iidRef = KpV * (vodRef - vod) + KiV * phid
    iiqRef = KpV * (voqRef - voq) + KiV * phiq
    vidRef = KpC * (iidRef - iid) + KiC * gammad - wset * Lt * iiq
    viqRef = KpC * (iiqRef - iiq) + KiC * gammaq + wset * Lt * iid

    # Ordinary differential equations
    f = sp.Matrix([
        wbase * (winv - wcom),
        -wc * Po + wc * (vod * iod + voq * ioq),
        -wc * Qo + wc * (voq * iod - vod * ioq),
        vodRef - vod,
        voqRef - voq,
        iidRef - iid,
        iiqRef - iiq,
        wbase * (vidRef - vod - Rt * iid + winv * Lt * iiq) / Lt,
        wbase * (viqRef - voq - Rt * iiq - winv * Lt * iid) / Lt,
        wbase * (iid - iod + winv * Cf * vcq) / Cf,
        wbase * (iiq - ioq - winv * Cf * vcd) / Cf,
        wbase * (vod - vbd - Rc * iod + winv * Lc * ioq) / Lc,
        wbase * (voq - vbq - Rc * ioq - winv * Lc * iod) / Lc
    ])

    ioD = iod * sp.cos(theta) - ioq * sp.sin(theta)
    ioQ = iod * sp.sin(theta) + ioq * sp.cos(theta)

    # State-Space Matrices
    stateVariables = ['theta', 'Po', 'Qo', 'phid', 'phiq', 'gammad', 'gammaq', 'iid', 'iiq', 'vcd', 'vcq', 'iod', 'ioq']
    x = sp.Matrix([theta, Po, Qo, phid, phiq, gammad, gammaq, iid, iiq, vcd, vcq, iod, ioq])
    u = sp.Matrix([vbD, vbQ, wcom])

    Asym = f.jacobian(x)
    Bsym = f.jacobian(sp.Matrix([vbD, vbQ]))
    BwSym = f.jacobian([wcom])
    Csym = sp.Matrix([ioD, ioQ]).jacobian(x)
    CwSym = winv.diff(x)

    # Ensure steadyStateValuesX and steadyStateValuesU are 1D arrays
    steadyStateValuesX = steadyStateValuesX.flatten()
    steadyStateValuesU = steadyStateValuesU.flatten()

    # Substitute steady-state values
    subs_dict = dict(zip(list(x) + list(u), np.concatenate((steadyStateValuesX, steadyStateValuesU))))
    A = Asym.subs(subs_dict).evalf()
    B = Bsym.subs(subs_dict).evalf()
    Bw = BwSym.subs(subs_dict).evalf()
    C = Csym.subs(subs_dict).evalf()
    Cw = CwSym.subs(subs_dict).evalf()

    if isRef == 0:
        Cw = sp.zeros(1, 13)

    # Output
    stateMatrix = {
        'A': np.array(A).astype(float),
        'B': np.array(B).astype(float),
        'Bw': np.array(Bw).astype(float),
        'C': np.array(C).astype(float),
        'Cw': np.array(Cw).astype(float),
        'ssVariables': stateVariables
    }

    return stateMatrix