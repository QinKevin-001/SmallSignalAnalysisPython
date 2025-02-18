#Test confirmed

import numpy as np
import sympy as sp

def ssmodel_vsmPlant(wbase, parasIBR, steadyStateValuesX, steadyStateValuesU, isRef):
    # Define symbolic variables
    thetaPlant, epsilonPLLPlant, wPlant, epsilonP, epsilonQ, PoPlant, QoPlant, PsetDelay, QsetDelay, theta, Tef, Qof, Vof, winv, psif, iid, iiq, vcd, vcq, iod, ioq = sp.symbols(
        'thetaPlant epsilonPLLPlant wPlant epsilonP epsilonQ PoPlant QoPlant PsetDelay QsetDelay theta Tef Qof Vof winv psif iid iiq vcd vcq iod ioq'
    )
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
    tDelay = parasIBR['tDelay']
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
    J = parasIBR['J']
    K = parasIBR['K']
    tauf = parasIBR['tauf']

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
    vbd = vbD*sp.cos(theta) + vbQ*sp.sin(theta)
    vbq = -vbD*sp.sin(theta) + vbQ*sp.cos(theta)
    vidRef = winv*psif
    viqRef = 0
    ioD = iod*sp.cos(theta) - ioq*sp.sin(theta)
    ioQ = iod*sp.sin(theta) + ioq*sp.cos(theta)

    # Ordinary differential equations (f is a 21x1 column vector)
    f = sp.Matrix([
        wbase*(wpllPlant - wcom),                                   # f1
        vbqPlant,                                                 # f2
        -wcpllPlant*wPlant + wcpllPlant*wpllPlant,                # f3
        PrefPlant - PoPlant,                                      # f4
        QrefPlant - QoPlant,                                      # f5
        -wcPlant*PoPlant + wcPlant*(vbD*ioD + vbQ*ioQ),           # f6
        -wcPlant*QoPlant + wcPlant*(vbQ*ioD - vbD*ioQ),           # f7
        (1/tDelay)*(Pset - PsetDelay),                            # f8
        (1/tDelay)*(Qset - QsetDelay),                            # f9
        wbase*(winv - wcom),                                      # f10
        (1/tauf)*(-Tef + (vod*iod + voq*ioq)/wset),               # f11
        (1/tauf)*(-Qof + voq*iod - vod*ioq),                      # f12
        (1/tauf)*(-Vof + sp.sqrt(vod**2 + voq**2)),                 # f13
        1/J*(PsetDelay/wset - Tef + 1/mp*(wset - winv)),           # f14
        1/K*(QsetDelay - Qof + 1/mq*(Vset - Vof)),                 # f15
        wbase*(vidRef - vod - Rt*iid + winv*Lt*iiq)/Lt,           # f16
        wbase*(viqRef - voq - Rt*iiq - winv*Lt*iid)/Lt,           # f17
        wbase*(iid - iod + winv*Cf*vcq)/Cf,                        # f18
        wbase*(iiq - ioq - winv*Cf*vcd)/Cf,                        # f19
        wbase*(vod - vbd - Rc*iod + winv*Lc*ioq)/Lc,               # f20
        wbase*(voq - vbq - Rc*ioq - winv*Lc*iod)/Lc                # f21
    ])

    # Define state vector (x) and input vector (u)
    stateVariables = ['thetaPlant', 'epsilonPLLPlant', 'wPlant', 'epsilonP', 'epsilonQ', 'PoPlant', 'QoPlant',
                      'PsetDelay', 'QsetDelay', 'theta', 'Tef', 'Qof', 'Vof', 'winv', 'psif', 'iid', 'iiq', 'vcd', 'vcq', 'iod', 'ioq']
    x = sp.Matrix([thetaPlant, epsilonPLLPlant, wPlant, epsilonP, epsilonQ, PoPlant, QoPlant,
                   PsetDelay, QsetDelay, theta, Tef, Qof, Vof, winv, psif, iid, iiq, vcd, vcq, iod, ioq])
    u = sp.Matrix([vbD, vbQ, wcom])

    # Compute Jacobians
    Asym = f.jacobian(x)
    Bsym = f.jacobian([vbD, vbQ])
    BwSym = f.jacobian(sp.Matrix([wcom]))
    Csym = sp.Matrix([ioD, ioQ]).jacobian(x)
    CwSym = sp.Matrix([winv]).jacobian(x)

    # Ensure steadyStateValuesX and steadyStateValuesU are 1D arrays
    steadyStateValuesX = np.array(steadyStateValuesX).flatten()
    steadyStateValuesU = np.array(steadyStateValuesU).flatten()

    # Create substitution dictionary mapping symbols in x and u to numerical steady-state values
    subs_dict = dict(zip(list(x) + list(u), np.concatenate((steadyStateValuesX, steadyStateValuesU)).tolist()))

    # Substitute steady-state values into the Jacobians and evaluate numerically
    A_sym = Asym.subs(subs_dict).evalf()
    B_sym = Bsym.subs(subs_dict).evalf()
    Bw_sym = BwSym.subs(subs_dict).evalf()
    C_sym = Csym.subs(subs_dict).evalf()
    Cw_sym = CwSym.subs(subs_dict).evalf()

    # Convert symbolic matrices to numerical NumPy arrays
    A = np.array(A_sym.tolist()).astype(float)
    B = np.array(B_sym.tolist()).astype(float)
    Bw = np.array(Bw_sym.tolist()).astype(float)
    C = np.array(C_sym.tolist()).astype(float)
    Cw = np.array(Cw_sym.tolist()).astype(float)

    # If isRef == 0, set Cw to a zero row vector with the appropriate dimension
    if isRef == 0:
        Cw = np.zeros((1, len(x)))

    # Construct stateMatrix dictionary for output
    stateMatrix = {
        'A': A,
        'B': B,
        'Bw': Bw,
        'C': C,
        'Cw': Cw,
        'ssVariables': stateVariables
    }

    return stateMatrix
