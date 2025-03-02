#DONT TOUCH
import numpy as np
import cmath

def steadystatevalue_vsm(w, Vo, Io, parasInverter):
    # Parameters
    wset = parasInverter['wset']
    Rt = parasInverter['Rt']
    Lt = parasInverter['Lt']
    Rd = parasInverter['Rd']
    Cf = parasInverter['Cf']
    Rc = parasInverter['Rc']
    Lc = parasInverter['Lc']

    # Calculation
    imagUnit = 1j
    Vb = Vo - (Rc + imagUnit * w * Lc) * Io
    VbD = Vb.real
    VbQ = Vb.imag

    VoAbs = abs(Vo)
    VoAngle = cmath.phase(Vo)
    IoAbs = abs(Io)
    IoAngle = cmath.phase(Io)

    Ic = Vo / (Rd + 1 / (imagUnit * w * Cf))
    Vc = Vo - Rd * Ic
    VcAbs = abs(Vc)
    VcAngle = cmath.phase(Vc)

    Ii = Ic + Io
    IiAbs = abs(Ii)
    IiAngle = cmath.phase(Ii)

    Vi = Vo + (Rt + imagUnit * w * Lt) * Ii
    ViAbs = abs(Vi)
    ViAngle = cmath.phase(Vi)

    Vod = VoAbs * np.cos(VoAngle - ViAngle)
    Voq = VoAbs * np.sin(VoAngle - ViAngle)
    Iod = IoAbs * np.cos(IoAngle - ViAngle)
    Ioq = IoAbs * np.sin(IoAngle - ViAngle)
    Vcd = VcAbs * np.cos(VcAngle - ViAngle)
    Vcq = VcAbs * np.sin(VcAngle - ViAngle)
    Iid = IiAbs * np.cos(IiAngle - ViAngle)
    Iiq = IiAbs * np.sin(IiAngle - ViAngle)
    Vid = ViAbs * np.cos(ViAngle - ViAngle)
    Viq = ViAbs * np.sin(ViAngle - ViAngle)

    Po = Vod * Iod + Voq * Ioq
    Qo = Voq * Iod - Vod * Ioq

    # Output
    Theta0 = ViAngle
    Tef0 = Po / wset
    Qof0 = Qo
    Vof0 = VoAbs
    winv0 = w
    Psif0 = Vid / w
    Iid0 = Iid
    Iiq0 = Iiq
    Vcd0 = Vcd
    Vcq0 = Vcq
    Iod0 = Iod
    Ioq0 = Ioq

    steadyStateValuesX = np.array([Theta0, Tef0, Qof0, Vof0, winv0, Psif0, Iid0, Iiq0, Vcd0, Vcq0, Iod0, Ioq0])
    steadyStateValuesU = np.array([VbD, VbQ, w])

    return steadyStateValuesX, steadyStateValuesU
