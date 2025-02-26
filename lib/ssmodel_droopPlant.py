import numpy as np
import sympy as sp

def ssmodel_droopPlant(wbase, parasIBR, steadyStateValuesX, steadyStateValuesU, isRef):
    # Define symbolic variables for 22 states (the ordering follows MATLAB)
    (thetaPlant, epsilonPLLPlant, wPlant, epsilonP, epsilonQ,
     PoPlant, QoPlant, PsetDelay, QsetDelay, theta, Po, Qo,
     phid, phiq, gammad, gammaq, iid, iiq, vcd, vcq, iod, ioq) = sp.symbols(
         'thetaPlant epsilonPLLPlant wPlant epsilonP epsilonQ PoPlant QoPlant PsetDelay QsetDelay theta Po Qo phid phiq gammad gammaq iid iiq vcd vcq iod ioq'
    )
    vbD, vbQ, wcom = sp.symbols('vbD vbQ wcom')

    # Parameter extraction
    PsetPlant   = parasIBR['PsetPlant']
    QsetPlant   = parasIBR['QsetPlant']
    wsetPlant   = parasIBR['wsetPlant']
    VsetPlant   = parasIBR['VsetPlant']
    mpPlant     = parasIBR['mpPlant']
    mqPlant     = parasIBR['mqPlant']
    KpPLLplant  = parasIBR['KpPLLplant']
    KiPLLplant  = parasIBR['KiPLLplant']
    KpPlantP    = parasIBR['KpPlantP']
    KiPlantP    = parasIBR['KiPlantP']
    KpPlantQ    = parasIBR['KpPlantQ']
    KiPlantQ    = parasIBR['KiPlantQ']
    wcpllPlant  = parasIBR['wcpllPlant']
    wcPlant     = parasIBR['wcPlant']
    tDelay      = parasIBR['tDelay']
    wset        = parasIBR['wset']
    Vset        = parasIBR['Vset']
    Rt          = parasIBR['Rt']
    Lt          = parasIBR['Lt']
    Rd          = parasIBR['Rd']
    Cf          = parasIBR['Cf']
    Rc          = parasIBR['Rc']
    Lc          = parasIBR['Lc']
    mp          = parasIBR['mp']
    mq          = parasIBR['mq']
    KpV         = parasIBR['KpV']
    KiV         = parasIBR['KiV']
    KpC         = parasIBR['KpC']
    KiC         = parasIBR['KiC']
    wc          = parasIBR['wc']

    # Algebraic equations (mirror MATLAB)
    vbqPlant = -vbD * sp.sin(thetaPlant) + vbQ * sp.cos(thetaPlant)
    wpllPlant = KpPLLplant * vbqPlant + KiPLLplant * epsilonPLLPlant + wsetPlant
    VabsPlant = sp.sqrt(vbD**2 + vbQ**2)
    PrefPlant = (wsetPlant - wPlant) / mpPlant + PsetPlant
    QrefPlant = (VsetPlant - VabsPlant) / mqPlant + QsetPlant
    Pset = KpPlantP * (PrefPlant - PoPlant) + KiPlantP * epsilonP + PsetPlant
    Qset = KpPlantQ * (QrefPlant - QoPlant) + KiPlantQ * epsilonQ + QsetPlant

    vod = vcd + Rd * (iid - iod)
    voq = vcq + Rd * (iiq - ioq)
    # IMPORTANT: Use the delay states in winv and vodRef expressions:
    winv = wset - mp * (Po - PsetDelay)
    vodRef = Vset - mq * (Qo - QsetDelay)
    voqRef = 0
    vbd = vbD * sp.cos(theta) + vbQ * sp.sin(theta)
    vbq = -vbD * sp.sin(theta) + vbQ * sp.cos(theta)
    iidRef = KpV * (vodRef - vod) + KiV * phid
    iiqRef = KpV * (voqRef - voq) + KiV * phiq
    vidRef = KpC * (iidRef - iid) + KiC * gammad - wset * Lt * iiq
    viqRef = KpC * (iiqRef - iiq) + KiC * gammaq + wset * Lt * iid
    ioD = (iod * sp.cos(theta) - ioq * sp.sin(theta))
    ioQ = (iod * sp.sin(theta) + ioq * sp.cos(theta))

    # Define 22 differential equations (in the same order as MATLAB)
    f = sp.Matrix([
        wbase * (wpllPlant - wcom),                                   # 1
        vbqPlant,                                                     # 2
        wcpllPlant * (wpllPlant - wPlant),                            # 3
        PrefPlant - PoPlant,                                            # 4
        QrefPlant - QoPlant,                                            # 5
        -wcPlant * PoPlant + wcPlant * (vbD * ioD + vbQ * ioQ),         # 6
        -wcPlant * QoPlant + wcPlant * (vbQ * ioD - vbD * ioQ),         # 7
        1/tDelay * (Pset - PsetDelay),                                  # 8
        1/tDelay * (Qset - QsetDelay),                                  # 9
        wbase * (winv - wcom),                                          # 10
        -wc * Po + wc * (vod * iod + voq * ioq),                        # 11
        -wc * Qo + wc * (voq * iod - vod * ioq),                        # 12
        vodRef - vod,                                                 # 13
        voqRef - voq,                                                 # 14
        iidRef - iid,                                                 # 15
        iiqRef - iiq,                                                 # 16
        wbase * (vidRef - vod - Rt * iid + winv * Lt * iiq) / Lt,         # 17
        wbase * (viqRef - voq - Rt * iiq - winv * Lt * iid) / Lt,         # 18
        wbase * (iid - iod + winv * Cf * vcq) / Cf,                       # 19
        wbase * (iiq - ioq - winv * Cf * vcd) / Cf,                       # 20
        wbase * (vod - vbd - Rc * iod + winv * Lc * ioq) / Lc,            # 21
        wbase * (voq - vbq - Rc * ioq - winv * Lc * iod) / Lc             # 22
    ])

    # Create state and input vectors matching the 22 states
    x = sp.Matrix([thetaPlant, epsilonPLLPlant, wPlant, epsilonP, epsilonQ,
                   PoPlant, QoPlant, PsetDelay, QsetDelay, theta, Po, Qo,
                   phid, phiq, gammad, gammaq, iid, iiq, vcd, vcq, iod, ioq])
    u = sp.Matrix([vbD, vbQ, wcom])

    # Calculate Jacobians with respect to x and u
    Asym = f.jacobian(x)
    Bsym = f.jacobian(sp.Matrix([vbD, vbQ]))
    BwSym = f.jacobian(sp.Matrix([wcom]))
    Csym = sp.Matrix([ioD, ioQ]).jacobian(x)
    CwSym = sp.Matrix([winv]).jacobian(x)

    # Substitute the steady-state values into the symbolic expressions
    subs_dict = dict(zip(list(x) + list(u),
                           np.concatenate((steadyStateValuesX.flatten(),
                                           steadyStateValuesU.flatten()))))
    A = Asym.subs(subs_dict).evalf()
    B = Bsym.subs(subs_dict).evalf()
    Bw = BwSym.subs(subs_dict).evalf()
    C = Csym.subs(subs_dict).evalf()
    Cw = CwSym.subs(subs_dict).evalf()

    if isRef == 0:
        Cw = sp.zeros(1, len(x))

    stateMatrix = {
        'A': np.array(A).astype(float),
        'B': np.array(B).astype(float),
        'Bw': np.array(Bw).astype(float),
        'C': np.array(C).astype(float),
        'Cw': np.array(Cw).astype(float),
        'ssVariables': ['thetaPlant', 'epsilonPLLPlant', 'wPlant', 'epsilonP', 'epsilonQ',
                         'PoPlant', 'QoPlant', 'PsetDelay', 'QsetDelay', 'theta', 'Po', 'Qo',
                         'phid', 'phiq', 'gammad', 'gammaq', 'iid', 'iiq', 'vcd', 'vcq', 'iod', 'ioq']
    }
    return stateMatrix