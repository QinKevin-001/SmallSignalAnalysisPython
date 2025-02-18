import numpy as np
import sympy as sp

def ssmodel_vsmPlant(wbase, parasIBR, steadyStateValuesX, steadyStateValuesU, isRef):
    # Define symbolic variables
    thetaPlant, epsilonPLLPlant, wPlant, epsilonP, epsilonQ, PoPlant, QoPlant, PsetDelay, QsetDelay = sp.symbols(
        'thetaPlant epsilonPLLPlant wPlant epsilonP epsilonQ PoPlant QoPlant PsetDelay QsetDelay'
    )
    theta, Tef, Qof, Vof, winv, psif, Iid, Iiq, Vcd, Vcq, Iod, Ioq = sp.symbols(
        'theta Tef Qof Vof winv psif Iid Iiq Vcd Vcq Iod Ioq'
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
    vbqPlant = -vbD * sp.sin(thetaPlant) + vbQ * sp.cos(thetaPlant)
    wpllPlant = KpPLLplant * vbqPlant + KiPLLplant * epsilonPLLPlant + wsetPlant
    VabsPlant = sp.sqrt(vbD ** 2 + vbQ ** 2)
    PrefPlant = (wsetPlant - wPlant) / mpPlant + PsetPlant
    QrefPlant = (VsetPlant - VabsPlant) / mqPlant + QsetPlant
    Pset = KpPlantP * (PrefPlant - PoPlant) + KiPlantP * epsilonP + PsetPlant
    Qset = KpPlantQ * (QrefPlant - QoPlant) + KiPlantQ * epsilonQ + QsetPlant

    vod = Vcd + Rd * (Iid - Iod)
    voq = Vcq + Rd * (Iiq - Ioq)
    vbd = vbD * sp.cos(theta) + vbQ * sp.sin(theta)
    vbq = -vbD * sp.sin(theta) + vbQ * sp.cos(theta)
    vidRef = winv * psif
    viqRef = 0

    ioD = Iod * sp.cos(theta) - Ioq * sp.sin(theta)
    ioQ = Iod * sp.sin(theta) + Ioq * sp.cos(theta)

    # Ordinary differential equations
    f = sp.Matrix([
        wbase * (wpllPlant - wcom),
        vbqPlant,
        -wcpllPlant * wPlant + wcpllPlant * wpllPlant,
        PrefPlant - PoPlant,
        QrefPlant - QoPlant,
        -wcPlant * PoPlant + wcPlant * (vbD * ioD + vbQ * ioQ),
        -wcPlant * QoPlant + wcPlant * (vbQ * ioD - vbD * ioQ),
        (Pset - PsetDelay) / tDelay,
        (Qset - QsetDelay) / tDelay,
        wbase * (winv - wcom),
        (-(Tef - (vod * Iod + voq * Ioq) / wset)) / tauf,
        (-(Qof - (voq * Iod - vod * Ioq))) / tauf,
        (-(Vof - sp.sqrt(vod ** 2 + voq ** 2))) / tauf,
        (PsetDelay / wset - Tef + (wset - winv) / mp) / J,
        (QsetDelay - Qof + (Vset - Vof) / mq) / K,
        wbase * (vidRef - vod - Rt * Iid + winv * Lt * Iiq) / Lt,
        wbase * (viqRef - voq - Rt * Iiq - winv * Lt * Iid) / Lt,
        wbase * (Iid - Iod + winv * Cf * Vcq) / Cf,
        wbase * (Iiq - Ioq - winv * Cf * Vcd) / Cf,
        wbase * (vod - vbd - Rc * Iod + winv * Lc * Ioq) / Lc,
        wbase * (voq - vbq - Rc * Ioq - winv * Lc * Iod) / Lc
    ])

    # State-Space Matrices
    stateVariables = [
        'thetaPlant', 'epsilonPLLPlant', 'wPlant', 'epsilonP', 'epsilonQ',
        'PoPlant', 'QoPlant', 'PsetDelay', 'QsetDelay',
        'theta', 'Tef', 'Qof', 'Vof', 'winv', 'psif',
        'Iid', 'Iiq', 'Vcd', 'Vcq', 'Iod', 'Ioq'
    ]

    x = sp.Matrix([
        thetaPlant, epsilonPLLPlant, wPlant, epsilonP, epsilonQ, PoPlant, QoPlant,
        PsetDelay, QsetDelay, theta, Tef, Qof, Vof, winv, psif, Iid, Iiq, Vcd, Vcq, Iod, Ioq
    ])
    u = sp.Matrix([vbD, vbQ, wcom])

    # Calculate Jacobians
    Asym = f.jacobian(x)
    Bsym = f.jacobian(sp.Matrix([vbD, vbQ]))
    BwSym = f.jacobian(sp.Matrix([wcom]))
    Csym = sp.Matrix([ioD, ioQ]).jacobian(x)
    CwSym = winv.diff(x)

    # Ensure steadyStateValuesX and steadyStateValuesU are 1D arrays
    steadyStateValuesX = np.array(steadyStateValuesX).flatten()
    steadyStateValuesU = np.array(steadyStateValuesU).flatten()

    # Substitute steady-state values
    subs_dict = dict(zip(list(x) + list(u), np.concatenate((steadyStateValuesX, steadyStateValuesU))))
    A = Asym.subs(subs_dict).evalf()
    B = Bsym.subs(subs_dict).evalf()
    Bw = BwSym.subs(subs_dict).evalf()
    C = Csym.subs(subs_dict).evalf()
    Cw = CwSym.subs(subs_dict).evalf()

    if isRef == 0:
        Cw = sp.zeros(1, len(stateVariables))

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
