import numpy as np
import cmath

def steadystatevalue_sg(w, Vb, Io, parasSG):
    # parameters
    Pset = parasSG['Pset']
    wset = parasSG['wset']
    Rs = parasSG['Rs']
    Ld = parasSG['Ld']
    Ld1 = parasSG['Ld1']
    Lq = parasSG['Lq']
    Ll = parasSG['Ll']
    D = parasSG['D']
    Lmd = Ld - Ll
    Lmq = Lq - Ll
    Lq1 = parasSG['Lq1']
    Kg = parasSG['Kg']
    T1 = parasSG['T1']
    T2 = parasSG['T2']
    K2 = parasSG['K2']
    Ke = parasSG['Ke']
    Ta = parasSG['Ta']
    Tb = parasSG['Tb']

    VbD = Vb.real
    VbQ = Vb.imag
    PowerFactorAngle = cmath.phase(Vb) - cmath.phase(Io)
    Eq = Vb + (Rs + 1j * w * Lq) * Io
    RotorAngle = cmath.phase(Eq) - cmath.phase(Vb)
    Vbabs = abs(Vb)
    Vbd = Vbabs * np.sin(RotorAngle)
    Vbq = Vbabs * np.cos(RotorAngle)
    Ioabs = abs(Io)
    Iod = Ioabs * np.sin(RotorAngle + PowerFactorAngle)
    Ioq = Ioabs * np.cos(RotorAngle + PowerFactorAngle)
    Psid = (Rs * Ioq + Vbq) / w
    Psiq = -(Rs * Iod + Vbd) / w
    Ifd = (Psid + Ld * Iod) / Lmd
    Psi1d = -Lmd * Iod + Lmd * Ifd
    Psi2q = -Lmq * Ioq
    Eq1 = Psi1d + (Ld1 - Ll) * Iod
    Ed1 = -Psi2q - (Lq1 - Ll) * Ioq
    Efd = Lmd * Ifd
    dwr = w - wset
    Pd = Kg * dwr
    P1 = Pd - Kg * T2/T1 * dwr
    Pg = Pset - Pd
    Pf = Pg
    P2 = K2 * Pf
    Vr = Efd / Ke
    Ve = Vr
    Vx = Vr - Ta/Tb * Ve

    Theta_0 = cmath.phase(Vb) + RotorAngle - np.pi/2
    steadyStateValuesX = np.array([
        Theta_0, w,      # Mechanical states
        Psid, Psiq,      # Flux states
        Eq1, Ed1,        # Voltage states
        Psi1d, Psi2q,    # Additional flux states
        P1, Pg, Pf, P2,  # Power states
        Vx, Efd          # Control states
    ])

    steadyStateValuesU = np.array([VbD, VbQ, w])

    return steadyStateValuesX, steadyStateValuesU