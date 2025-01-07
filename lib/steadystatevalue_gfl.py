

import numpy as np
import cmath

def steadystatevalue_gfl(w, Vo, Io, parasInverter):
    # Parameters
    wset = parasInverter['wset']
    Rt = parasInverter['Rt']
    Lt = parasInverter['Lt']
    Rd = parasInverter['Rd']
    Cf = parasInverter['Cf']
    Rc = parasInverter['Rc']
    Lc = parasInverter['Lc']
    KiL = parasInverter['KiL']
    KiS = parasInverter['KiS']
    KiC = parasInverter['KiC']

    # Calculation
    imagUnit = 1j
    Vb = Vo - (Rc + imagUnit * w * Lc) * Io
    VbD = Vb.real
    VbQ = Vb.imag
    VoAbs = abs(Vo)
    VoAngle = cmath.phase(Vo)
    Vod = VoAbs
    Voq = 0
    IoAbs = abs(Io)
    IoAngle = cmath.phase(Io)
    Iod = IoAbs * np.cos(IoAngle - VoAngle)
    Ioq = IoAbs * np.sin(IoAngle - VoAngle)
    Po = Vod * Iod + Voq * Ioq
    Qo = Voq * Iod - Vod * Ioq
    Ic = Vo / (Rd + 1 / (imagUnit * w * Cf))
    Vc = Vo - Rd * Ic
    VcAbs = abs(Vc)
    VcAngle = cmath.phase(Vc)
    Vcd = VcAbs * np.cos(VcAngle - VoAngle)
    Vcq = VcAbs * np.sin(VcAngle - VoAngle)
    Ii = Ic + Io
    IiAbs = abs(Ii)
    IiAngle = cmath.phase(Ii)
    Iid = IiAbs * np.cos(IiAngle - VoAngle)
    Iiq = IiAbs * np.sin(IiAngle - VoAngle)
    Vi = Vo + (Rt + imagUnit * w * Lt) * Ii
    ViAbs = abs(Vi)
    ViAngle = cmath.phase(Vi)
    Vid = ViAbs * np.cos(ViAngle - VoAngle)
    Viq = ViAbs * np.sin(ViAngle - VoAngle)

    # Output
    Theta0 = VoAngle
    EpsilonL0 = (w - wset) / KiL
    wf0 = w
    Po0 = Po
    Qo0 = Qo
    Phid0 = Iid / KiS
    Phiq0 = Iiq / KiS
    Gammad0 = (Vid + wset * Lt * Iiq) / KiC
    Gammaq0 = (Viq - wset * Lt * Iid) / KiC
    Iid0 = Iid
    Iiq0 = Iiq
    Vcd0 = Vcd
    Vcq0 = Vcq
    Iod0 = Iod
    Ioq0 = Ioq

    steadyStateValuesX = np.array([
        Theta0, EpsilonL0, wf0, Po0, Qo0, Phid0, Phiq0, Gammad0, Gammaq0,
        Iid0, Iiq0, Vcd0, Vcq0, Iod0, Ioq0
    ])
    steadyStateValuesU = np.array([VbD, VbQ, w])

    return steadyStateValuesX, steadyStateValuesU
