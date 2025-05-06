import sympy as sp
import numpy as np

def ssmodel_vsmPlant(wbase, parasIBR, steadyStateValuesX, steadyStateValuesU, isRef):
    (thetaPlant, epsilonPLLPlant, wPlant, epsilonP, epsilonQ,
     PoPlant, QoPlant, PsetDelay, QsetDelay, theta, Tef, Qof, Vof,
     winv, psif, iid, iiq, vcd, vcq, iod, ioq) = sp.symbols(
        'thetaPlant epsilonPLLPlant wPlant epsilonP epsilonQ PoPlant QoPlant '
        'PsetDelay QsetDelay theta Tef Qof Vof winv psif iid iiq vcd vcq iod ioq',
        real=True)
    (vbD, vbQ, wcom) = sp.symbols('vbD vbQ wcom', real=True)

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
    Pset_expr = KpPlantP * (PrefPlant - PoPlant) + KiPlantP * epsilonP + PsetPlant
    Qset_expr = KpPlantQ * (QrefPlant - QoPlant) + KiPlantQ * epsilonQ + QsetPlant
    vod = vcd + Rd * (iid - iod)
    voq = vcq + Rd * (iiq - ioq)
    vbd = vbD * sp.cos(theta) + vbQ * sp.sin(theta)
    vbq = -vbD * sp.sin(theta) + vbQ * sp.cos(theta)
    vidRef = winv * psif
    viqRef = 0  # zero reference
    ioD = iod * sp.cos(theta) - ioq * sp.sin(theta)
    ioQ = iod * sp.sin(theta) + ioq * sp.cos(theta)

    # Ordinary differential equations
    f1 = wbase * (wpllPlant - wcom)
    f2 = vbqPlant
    f3 = -wcpllPlant * wPlant + wcpllPlant * wpllPlant
    f4 = PrefPlant - PoPlant
    f5 = QrefPlant - QoPlant
    f6 = -wcPlant * PoPlant + wcPlant * (vbD * ioD + vbQ * ioQ)
    f7 = -wcPlant * QoPlant + wcPlant * (vbQ * ioD - vbD * ioQ)
    f8 = (Pset_expr - PsetDelay) / tDelay
    f9 = (Qset_expr - QsetDelay) / tDelay
    f10 = wbase * (winv - wcom)
    f11 = (-Tef + (vod * iod + voq * ioq) / wset) / tauf
    f12 = (-Qof + voq * iod - vod * ioq) / tauf
    f13 = (-Vof + sp.sqrt(vod ** 2 + voq ** 2)) / tauf
    f14 = (PsetDelay / wset - Tef + (wset - winv) / mp) / J
    f15 = (QsetDelay - Qof + (Vset - Vof) / mq) / K
    f16 = wbase * (vidRef - vod - Rt * iid + winv * Lt * iiq) / Lt
    f17 = wbase * (viqRef - voq - Rt * iiq - winv * Lt * iid) / Lt
    f18 = wbase * (iid - iod + winv * Cf * vcq) / Cf
    f19 = wbase * (iiq - ioq - winv * Cf * vcd) / Cf
    f20 = wbase * (vod - vbd - Rc * iod + winv * Lc * ioq) / Lc
    f21 = wbase * (voq - vbq - Rc * ioq - winv * Lc * iod) / Lc
    f = sp.Matrix([f1, f2, f3, f4, f5, f6, f7, f8, f9, f10,
                   f11, f12, f13, f14, f15, f16, f17, f18, f19, f20, f21])
    # Define state and input variables
    stateVariables = ['thetaPlant', 'epsilonPLLPlant', 'wPlant', 'epsilonP', 'epsilonQ',
                      'PoPlant', 'QoPlant', 'PsetDelay', 'QsetDelay', 'theta', 'Tef', 'Qof',
                      'Vof', 'winv', 'psif', 'iid', 'iiq', 'vcd', 'vcq', 'iod', 'ioq']
    x = sp.Matrix([thetaPlant, epsilonPLLPlant, wPlant, epsilonP, epsilonQ,
                   PoPlant, QoPlant, PsetDelay, QsetDelay, theta, Tef, Qof,
                   Vof, winv, psif, iid, iiq, vcd, vcq, iod, ioq])
    u = sp.Matrix([vbD, vbQ, wcom])
    A_sym = f.jacobian(x)
    B_sym = f.jacobian([vbD, vbQ])
    Bw_sym = f.jacobian([wcom])
    C_sym = sp.Matrix([ioD, ioQ]).jacobian(x)
    Cw_sym = sp.Matrix([winv]).jacobian(x)
    subs_dict = dict(zip(list(x) + list(u), np.concatenate((steadyStateValuesX, steadyStateValuesU))))
    A = np.array(A_sym.subs(subs_dict)).astype(np.float64)
    B = np.array(B_sym.subs(subs_dict)).astype(np.float64)
    Bw = np.array(Bw_sym.subs(subs_dict)).astype(np.float64)
    C = np.array(C_sym.subs(subs_dict)).astype(np.float64)
    Cw = np.array(Cw_sym.subs(subs_dict)).astype(np.float64)
    if isRef == 0:
        Cw = np.zeros((1, len(x)))
    stateMatrix = {
        'A': np.array(A).astype(float),
        'B': np.array(B).astype(float),
        'Bw': np.array(Bw).astype(float),
        'C': np.array(C).astype(float),
        'Cw': np.array(Cw).astype(float),
        'ssVariables': stateVariables
    }

    return stateMatrix
