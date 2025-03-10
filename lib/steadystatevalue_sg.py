import numpy as np

def steadystatevalue_sg(w, Vb, Io, parasSG):
    # Extract parameters from parasSG (assumed to be a dictionary)
    Pset = parasSG['Pset']
    wset = parasSG['wset']
    Rs   = parasSG['Rs']
    Ld   = parasSG['Ld']
    Ld1  = parasSG['Ld1']
    Lq   = parasSG['Lq']
    Ll   = parasSG['Ll']
    D    = parasSG['D']
    Lmd  = Ld - Ll
    Lmq  = Lq - Ll
    Lq1  = parasSG['Lq1']
    Kg   = parasSG['Kg']
    T1   = parasSG['T1']
    T2   = parasSG['T2']
    K2   = parasSG['K2']
    Ke   = parasSG['Ke']
    Ta   = parasSG['Ta']
    Tb   = parasSG['Tb']

    imagUnit = 1j  # Imaginary unit

    # Compute components from the voltage Vb and current Io
    VbD = np.real(Vb)
    VbQ = np.imag(Vb)
    PowerFactorAngle = np.angle(Vb) - np.angle(Io)
    Eq = Vb + (Rs + imagUnit * w * Lq) * Io
    RotorAngle = np.angle(Eq) - np.angle(Vb)
    Vbabs = np.abs(Vb)
    Vbd = Vbabs * np.sin(RotorAngle)
    Vbq = Vbabs * np.cos(RotorAngle)
    Ioabs = np.abs(Io)
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
    P1 = Pd - Kg * (T2 / T1) * dwr
    Pg = Pset - Pd
    Pf = Pg
    P2 = K2 * Pf
    Vr = Efd / Ke
    Ve = Vr
    Vx = Vr - (Ta / Tb) * Ve

    # Define steady-state output variables
    Theta_0 = np.angle(Vb) + RotorAngle - np.pi/2
    wr_0    = w
    Psid_0  = Psid
    Psiq_0  = Psiq
    Eq1_0   = Eq1
    Ed1_0   = Ed1
    Psi1d_0 = Psi1d
    Psi2q_0 = Psi2q
    P1_0    = P1
    Pg_0    = Pg
    Pf_0    = Pf
    P2_0    = P2
    Vx_0    = Vx
    Efd_0   = Efd

    # Create steady-state state and input vectors
    steadyStateValuesX = np.array([
        Theta_0, wr_0, Psid_0, Psiq_0, Eq1_0, Ed1_0,
        Psi1d_0, Psi2q_0, P1_0, Pg_0, Pf_0, P2_0, Vx_0, Efd_0
    ])
    steadyStateValuesU = np.array([VbD, VbQ, w])

    return steadyStateValuesX, steadyStateValuesU
