import numpy as np
import sympy as sp

def ssmodel_gflPlant(wbase, parasIBR, steadyStateValuesX, steadyStateValuesU, isRef):
    # Define symbolic variables
    thetaPlant, epsilonPLLPlant, wPlant, epsilonP, epsilonQ, PoPlant, QoPlant, theta, epsilonPLL, wf, Po, Qo, phid, phiq, gammad, gammaq, iid, iiq, vcd, vcq, iod, ioq = sp.symbols(
        'thetaPlant epsilonPLLPlant wPlant epsilonP epsilonQ PoPlant QoPlant theta epsilonPLL wf Po Qo phid phiq gammad gammaq iid iiq vcd vcq iod ioq')
    vbD, vbQ, wcom = sp.symbols('vbD vbQ wcom')

    # Parameters
    PsetPlant = parasIBR['PsetPlant']
    QsetPlant = parasIBR['QsetPlant']
    wsetPlant = parasIBR['wsetPlant']
    VsetPlant = parasIBR['VsetPlant']
    mpPlant = parasIBR['mpPlant']
    mqPlant = parasIBR['mqPlant']
    KpPLLplant = parasIBR['KpPLLplant']
    KiPLLplant = parasIBR['KiPLLplant']
    KpPlantP = parasIBR['KpPlantP']
    KiPlantP = parasIBR['KiPlantP']
    KpPlantQ = parasIBR['KpPlantQ']
    KiPlantQ = parasIBR['KiPlantQ']
    wcpllPlant = parasIBR['wcpllPlant']
    wcPlant = parasIBR['wcPlant']
    wset = parasIBR['wset']
    Vset = parasIBR['Vset']
    Rt = parasIBR['Rt']
    Lt = parasIBR['Lt']
    Rd = parasIBR['Rd']
    Cf = parasIBR['Cf']
    Rc = parasIBR['Rc']
    Lc = parasIBR['Lc']
    mp = parasIBR['mp']
    mq = parasIBR['mq']
    KpL = parasIBR['KpL']
    KiL = parasIBR['KiL']
    KpS = parasIBR['KpS']
    KiS = parasIBR['KiS']
    KpC = parasIBR['KpC']
    KiC = parasIBR['KiC']
    wcpll = parasIBR['wcpll']
    wc = parasIBR['wc']

    # Algebraic equations
    vbqPlant = -vbD * sp.sin(thetaPlant) + vbQ * sp.cos(thetaPlant)
    wpllPlant = KpPLLplant * vbqPlant + KiPLLplant * epsilonPLLPlant + wsetPlant
    VabsPlant = sp.sqrt(vbD**2 + vbQ**2)
    PrefPlant = (wsetPlant - wPlant) / mpPlant + PsetPlant
    QrefPlant = (VsetPlant - VabsPlant) / mqPlant + QsetPlant
    Pset = KpPlantP * (PrefPlant - PoPlant) + KiPlantP * epsilonP + PsetPlant
    Qset = KpPlantQ * (QrefPlant - QoPlant) + KiPlantQ * epsilonQ + QsetPlant
    vod = vcd + Rd * (iid - iod)
    voq = vcq + Rd * (iiq - ioq)
    winv = KpL * voq + KiL * epsilonPLL + wset
    Pref = (wset - wf) / mp + Pset
    Qref = (Vset - sp.sqrt(vod**2 + voq**2)) / mq + Qset
    vbd = vbD * sp.cos(theta) + vbQ * sp.sin(theta)
    vbq = -vbD * sp.sin(theta) + vbQ * sp.cos(theta)
    iidRef = KpS * (Pref - Po) + KiS * phid
    iiqRef = KpS * (Qo - Qref) + KiS * phiq
    vidRef = KpC * (iidRef - iid) + KiC * gammad - wset * Lt * iiq
    viqRef = KpC * (iiqRef - iiq) + KiC * gammaq + wset * Lt * iid
    ioD = iod * sp.cos(theta) - ioq * sp.sin(theta)
    ioQ = iod * sp.sin(theta) + ioq * sp.cos(theta)

    # Ordinary differential equations
    f = sp.Matrix([
        wbase * (wpllPlant - wcom),
        vbqPlant,
        -wcpllPlant * wPlant + wcpllPlant * wpllPlant,
        PrefPlant - PoPlant,
        QrefPlant - QoPlant,
        -wcPlant * PoPlant + wcPlant * (vbD * ioD + vbQ * ioQ),
        -wcPlant * QoPlant + wcPlant * (vbQ * ioD - vbD * ioQ),
        wbase * (winv - wcom),
        voq,
        -wcpll * wf + wcpll * winv,
        -wc * Po + wc * (vod * iod + voq * ioq),
        -wc * Qo + wc * (voq * iod - vod * ioq),
        Pref - Po,
        Qo - Qref,
        iidRef - iid,
        iiqRef - iiq,
        wbase * (vidRef - vod - Rt * iid + winv * Lt * iiq) / Lt,
        wbase * (viqRef - voq - Rt * iiq - winv * Lt * iid) / Lt,
        wbase * (iid - iod + winv * Cf * vcq) / Cf,
        wbase * (iiq - ioq - winv * Cf * vcd) / Cf,
        wbase * (vod - vbd - Rc * iod + winv * Lc * ioq) / Lc,
        wbase * (voq - vbq - Rc * ioq - winv * Lc * iod) / Lc
    ])

    # State-space matrices
    stateVariables = [
        'thetaPlant', 'epsilonPLLPlant', 'wPlant', 'epsilonP', 'epsilonQ',
        'PoPlant', 'QoPlant', 'theta', 'epsilonPLL', 'wf', 'Po', 'Qo',
        'phid', 'phiq', 'gammad', 'gammaq', 'iid', 'iiq', 'vcd', 'vcq', 'iod', 'ioq'
    ]
    x = sp.Matrix([
        thetaPlant, epsilonPLLPlant, wPlant, epsilonP, epsilonQ, PoPlant,
        QoPlant, theta, epsilonPLL, wf, Po, Qo, phid, phiq, gammad, gammaq,
        iid, iiq, vcd, vcq, iod, ioq
    ])
    u = sp.Matrix([vbD, vbQ, wcom])

    # Jacobians
    Asym = f.jacobian(x)
    Bsym = f.jacobian(sp.Matrix([vbD, vbQ]))
    BwSym = f.jacobian(sp.Matrix([wcom]))
    Csym = sp.Matrix([ioD, ioQ]).jacobian(x)
    CwSym = sp.Matrix([winv]).jacobian(x)

    # Substitute steady-state values
    substitutions = {**dict(zip(x, steadyStateValuesX)), **dict(zip(u, steadyStateValuesU))}
    A = np.array(Asym.subs(substitutions)).astype(float)
    B = np.array(Bsym.subs(substitutions)).astype(float)
    Bw = np.array(BwSym.subs(substitutions)).astype(float)
    C = np.array(Csym.subs(substitutions)).astype(float)
    Cw = np.array(CwSym.subs(substitutions)).astype(float)

    if isRef == 0:
        Cw = np.zeros((1, len(stateVariables)))

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
