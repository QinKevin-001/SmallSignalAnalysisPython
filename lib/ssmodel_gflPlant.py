#DONT TOUCH
import numpy as np
import sympy as sp

def ssmodel_gflPlant(wbase, parasIBR, steadyStateValuesX, steadyStateValuesU, isRef):
    # Define symbolic variables (note the added PsetDelay and QsetDelay)
    thetaPlant, epsilonPLLPlant, wPlant, epsilonP, epsilonQ, \
    PoPlant, QoPlant, PsetDelay, QsetDelay, \
    theta, epsilonPLL, wf, Po, Qo, \
    phid, phiq, gammad, gammaq, iid, iiq, \
    vcd, vcq, iod, ioq = sp.symbols(
        'thetaPlant epsilonPLLPlant wPlant epsilonP epsilonQ PoPlant QoPlant PsetDelay QsetDelay '
        'theta epsilonPLL wf Po Qo phid phiq gammad gammaq iid iiq vcd vcq iod ioq')

    vbD, vbQ, wcom = sp.symbols('vbD vbQ wcom')

    # Parameters
    PsetPlant  = parasIBR['PsetPlant']
    QsetPlant  = parasIBR['QsetPlant']
    wsetPlant  = parasIBR['wsetPlant']
    VsetPlant  = parasIBR['VsetPlant']
    mpPlant    = parasIBR['mpPlant']
    mqPlant    = parasIBR['mqPlant']
    KpPLLplant = parasIBR['KpPLLplant']
    KiPLLplant = parasIBR['KiPLLplant']
    KpPlantP   = parasIBR['KpPlantP']
    KiPlantP   = parasIBR['KiPlantP']
    KpPlantQ   = parasIBR['KpPlantQ']
    KiPlantQ   = parasIBR['KiPlantQ']
    wcpllPlant = parasIBR['wcpllPlant']
    wcPlant    = parasIBR['wcPlant']
    tDelay     = parasIBR['tDelay']
    wset       = parasIBR['wset']
    Vset       = parasIBR['Vset']
    Rt         = parasIBR['Rt']
    Lt         = parasIBR['Lt']
    Rd         = parasIBR['Rd']
    Cf         = parasIBR['Cf']
    Rc         = parasIBR['Rc']
    Lc         = parasIBR['Lc']
    mp         = parasIBR['mp']
    mq         = parasIBR['mq']
    KpL        = parasIBR['KpL']
    KiL        = parasIBR['KiL']
    KpS        = parasIBR['KpS']
    KiS        = parasIBR['KiS']
    KpC        = parasIBR['KpC']
    KiC        = parasIBR['KiC']
    wcpll      = parasIBR['wcpll']
    wc         = parasIBR['wc']

    # Algebraic equations
    vbqPlant   = -vbD * sp.sin(thetaPlant) + vbQ * sp.cos(thetaPlant)
    wpllPlant  = KpPLLplant * vbqPlant + KiPLLplant * epsilonPLLPlant + wsetPlant
    VabsPlant  = sp.sqrt(vbD**2 + vbQ**2)
    PrefPlant  = (wsetPlant - wPlant) / mpPlant + PsetPlant
    QrefPlant  = (VsetPlant - VabsPlant) / mqPlant + QsetPlant
    Pset       = KpPlantP * (PrefPlant - PoPlant) + KiPlantP * epsilonP + PsetPlant
    Qset       = KpPlantQ * (QrefPlant - QoPlant) + KiPlantQ * epsilonQ + QsetPlant
    vod        = vcd + Rd * (iid - iod)
    voq        = vcq + Rd * (iiq - ioq)
    winv       = KpL * voq + KiL * epsilonPLL + wset
    # Use the delay states here, as in the MATLAB model
    Pref       = (wset - wf) / mp + PsetDelay
    Qref       = (Vset - sp.sqrt(vod**2 + voq**2)) / mq + QsetDelay
    vbd        = vbD * sp.cos(theta) + vbQ * sp.sin(theta)
    vbq        = -vbD * sp.sin(theta) + vbQ * sp.cos(theta)
    iidRef     = KpS * (Pref - Po) + KiS * phid
    iiqRef     = KpS * (Qo - Qref) + KiS * phiq
    vidRef     = KpC * (iidRef - iid) + KiC * gammad - wset * Lt * iiq
    viqRef     = KpC * (iiqRef - iiq) + KiC * gammaq + wset * Lt * iid
    ioD        = iod * sp.cos(theta) - ioq * sp.sin(theta)
    ioQ        = iod * sp.sin(theta) + ioq * sp.cos(theta)

    # Ordinary differential equations (24 equations)
    f = sp.Matrix([
        wbase * (wpllPlant - wcom),                                 # Equation 1
        vbqPlant,                                                  # Equation 2
        -wcpllPlant * wPlant + wcpllPlant * wpllPlant,             # Equation 3
        PrefPlant - PoPlant,                                       # Equation 4
        QrefPlant - QoPlant,                                       # Equation 5
        -wcPlant * PoPlant + wcPlant * (vbD * ioD + vbQ * ioQ),     # Equation 6
        -wcPlant * QoPlant + wcPlant * (vbQ * ioD - vbD * ioQ),     # Equation 7
        1/tDelay * (Pset - PsetDelay),                             # Equation 8 (delay dynamics for Pset)
        1/tDelay * (Qset - QsetDelay),                             # Equation 9 (delay dynamics for Qset)
        wbase * (winv - wcom),                                     # Equation 10
        voq,                                                       # Equation 11
        -wcpll * wf + wcpll * winv,                                # Equation 12
        -wc * Po + wc * (vod * iod + voq * ioq),                   # Equation 13
        -wc * Qo + wc * (voq * iod - vod * ioq),                   # Equation 14
        Pref - Po,                                                 # Equation 15
        Qo - Qref,                                                 # Equation 16
        iidRef - iid,                                              # Equation 17
        iiqRef - iiq,                                              # Equation 18
        wbase * (vidRef - vod - Rt * iid + winv * Lt * iiq) / Lt,    # Equation 19
        wbase * (viqRef - voq - Rt * iiq - winv * Lt * iid) / Lt,    # Equation 20
        wbase * (iid - iod + winv * Cf * vcq) / Cf,                  # Equation 21
        wbase * (iiq - ioq - winv * Cf * vcd) / Cf,                  # Equation 22
        wbase * (vod - vbd - Rc * iod + winv * Lc * ioq) / Lc,       # Equation 23
        wbase * (voq - vbq - Rc * ioq - winv * Lc * iod) / Lc        # Equation 24
    ])

    # State-space matrices
    stateVariables = [
        'thetaPlant', 'epsilonPLLPlant', 'wPlant', 'epsilonP', 'epsilonQ',
        'PoPlant', 'QoPlant', 'PsetDelay', 'QsetDelay', 'theta', 'epsilonPLL',
        'wf', 'Po', 'Qo', 'phid', 'phiq', 'gammad', 'gammaq', 'iid', 'iiq',
        'vcd', 'vcq', 'iod', 'ioq'
    ]
    x = sp.Matrix([
        thetaPlant, epsilonPLLPlant, wPlant, epsilonP, epsilonQ,
        PoPlant, QoPlant, PsetDelay, QsetDelay, theta, epsilonPLL, wf,
        Po, Qo, phid, phiq, gammad, gammaq, iid, iiq, vcd, vcq, iod, ioq
    ])
    u = sp.Matrix([vbD, vbQ, wcom])

    # Jacobians of the system equations with respect to state and input variables
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
        'A': A,
        'B': B,
        'Bw': Bw,
        'C': C,
        'Cw': Cw,
        'ssVariables': stateVariables
    }

    return stateMatrix