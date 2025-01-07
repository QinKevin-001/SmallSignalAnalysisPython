#Test confirmed

import numpy as np
import sympy as sp

def ssmodel_droopPlant(wbase, parasIBR, steadyStateValuesX, steadyStateValuesU, isRef):
    # Define symbolic variables
    thetaPlant, epsilonPLLPlant, wPlant, epsilonP, epsilonQ, PoPlant, QoPlant, theta, Po, Qo, phid, phiq, gammad, gammaq, iid, iiq, vcd, vcq, iod, ioq = sp.symbols('thetaPlant epsilonPLLPlant wPlant epsilonP epsilonQ PoPlant QoPlant theta Po Qo phid phiq gammad gammaq iid iiq vcd vcq iod ioq')
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
    KpV = parasIBR['KpV']
    KiV = parasIBR['KiV']
    KpC = parasIBR['KpC']
    KiC = parasIBR['KiC']
    wc = parasIBR['wc']

    # Algebraic equations
    vbqPlant = -vbD*sp.sin(thetaPlant) + vbQ*sp.cos(thetaPlant)
    wpllPlant = KpPLLplant*vbqPlant + KiPLLplant*epsilonPLLPlant + wsetPlant
    VabsPlant = sp.sqrt(vbD**2 + vbQ**2)
    PrefPlant = (wsetPlant - wPlant)/mpPlant + PsetPlant
    QrefPlant = (VsetPlant - VabsPlant)/mqPlant + QsetPlant
    Pset = KpPlantP*(PrefPlant - PoPlant) + KiPlantP*epsilonP + PsetPlant
    Qset = KpPlantQ*(QrefPlant - QoPlant) + KiPlantQ*epsilonQ + QsetPlant
    vod = vcd + Rd*(iid - iod)
    voq = vcq + Rd*(iiq - ioq)
    winv = wset - mp*(Po - Pset)
    vodRef = Vset - mq*(Qo - Qset)
    voqRef = 0
    vbd = vbD*sp.cos(theta) + vbQ*sp.sin(theta)
    vbq = -vbD*sp.sin(theta) + vbQ*sp.cos(theta)
    iidRef = KpV*(vodRef - vod) + KiV*phid
    iiqRef = KpV*(voqRef - voq) + KiV*phiq
    vidRef = KpC*(iidRef - iid) + KiC*gammad - wset*Lt*iiq
    viqRef = KpC*(iiqRef - iiq) + KiC*gammaq + wset*Lt*iid
    ioD = (iod*sp.cos(theta) - ioq*sp.sin(theta))
    ioQ = (iod*sp.sin(theta) + ioq*sp.cos(theta))

    # Ordinary differential equations
    f = sp.Matrix([
        wbase*(wpllPlant - wcom),
        vbqPlant - 0,
        -wcpllPlant*wPlant + wcpllPlant*wpllPlant,
        PrefPlant - PoPlant,
        QrefPlant - QoPlant,
        -wcPlant*PoPlant + wcPlant*(vbD*ioD + vbQ*ioQ),
        -wcPlant*QoPlant + wcPlant*(vbQ*ioD - vbD*ioQ),
        wbase*(winv - wcom),
        -wc*Po + wc*(vod*iod + voq*ioq),
        -wc*Qo + wc*(voq*iod - vod*ioq),
        vodRef - vod,
        voqRef - voq,
        iidRef - iid,
        iiqRef - iiq,
        wbase*(vidRef - vod - Rt*iid + winv*Lt*iiq)/Lt,
        wbase*(viqRef - voq - Rt*iiq - winv*Lt*iid)/Lt,
        wbase*(iid - iod + winv*Cf*vcq)/Cf,
        wbase*(iiq - ioq - winv*Cf*vcd)/Cf,
        wbase*(vod - vbd - Rc*iod + winv*Lc*ioq)/Lc,
        wbase*(voq - vbq - Rc*ioq - winv*Lc*iod)/Lc
    ])

    # State-Space Matrices
    stateVariables = ['thetaPlant', 'epsilonPLLPlant', 'wPlant', 'epsilonP', 'epsilonQ', 'PoPlant', 'QoPlant', 'theta', 'Po', 'Qo', 'phid', 'phiq', 'gammad', 'gammaq', 'iid', 'iiq', 'vcd', 'vcq', 'iod', 'ioq']
    x = sp.Matrix([thetaPlant, epsilonPLLPlant, wPlant, epsilonP, epsilonQ, PoPlant, QoPlant, theta, Po, Qo, phid, phiq, gammad, gammaq, iid, iiq, vcd, vcq, iod, ioq])
    u = sp.Matrix([vbD, vbQ, wcom])

    # Calculate Jacobians
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
        Cw = sp.zeros(1, 20)

    # Convert symbolic matrices to numerical arrays
    stateMatrix = {
        'A': np.array(A).astype(float),
        'B': np.array(B).astype(float),
        'Bw': np.array(Bw).astype(float),
        'C': np.array(C).astype(float),
        'Cw': np.array(Cw).astype(float),
        'ssVariables': stateVariables
    }

    return stateMatrix

