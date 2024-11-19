import numpy as np
import cmath

def steadystatevalue_droopSimplified(w, Vo, Io, parasInverter):
    # Parameters
    Rc = parasInverter['Rc']
    Lc = parasInverter['Lc']

    # Calculation
    Vb = Vo - (Rc + 1j*w*Lc)*Io
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
    Po = Vod*Iod + Voq*Ioq
    Qo = Voq*Iod - Vod*Ioq

    # Output
    Theta0 = VoAngle
    Po0 = Po
    Qo0 = Qo
    Iod0 = Iod
    Ioq0 = Ioq
    steadyStateValuesX = np.array([Theta0, Po0, Qo0, Iod0, Ioq0])
    steadyStateValuesU = np.array([VbD, VbQ, w])

    return steadyStateValuesX, steadyStateValuesU

