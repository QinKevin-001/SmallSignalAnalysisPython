# Test confirmed

import numpy as np
import cmath


def steadystatevalue_vsmpPlant(w, Vb, Io, parasIBR):
    # Parameters
    PsetPlant = parasIBR['PsetPlant']
    QsetPlant = parasIBR['QsetPlant']
    KiPLLplant = parasIBR['KiPLLplant']
    KiPlantP = parasIBR['KiPlantP']
    KiPlantQ = parasIBR['KiPlantQ']
    wsetPlant = parasIBR['wsetPlant']
    wset = parasIBR['wset']
    Vset = parasIBR['Vset']
    mp = parasIBR['mp']
    mq = parasIBR['mq']
    Rt = parasIBR['Rt']
    Lt = parasIBR['Lt']
    Rd = parasIBR['Rd']
    Cf = parasIBR['Cf']
    Rc = parasIBR['Rc']
    Lc = parasIBR['Lc']

    # Calculation
    imagUnit = 1j  # equivalent to sqrt(-1)

    VbAngle = cmath.phase(Vb)
    VbD = Vb.real
    VbQ = Vb.imag
    IoD = Io.real
    IoQ = Io.imag

    PoPlant = VbD * IoD + VbQ * IoQ
    QoPlant = VbQ * IoD - VbD * IoQ

    Vo = Vb + (Rc + imagUnit * w * Lc) * Io
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
    # Note: cos(ViAngle-ViAngle)=1 and sin(ViAngle-ViAngle)=0
    Vid = ViAbs * np.cos(ViAngle - ViAngle)  # equals ViAbs
    Viq = ViAbs * np.sin(ViAngle - ViAngle)  # equals 0

    Po = Vod * Iod + Voq * Ioq
    Qo = Voq * Iod - Vod * Ioq

    # Output calculations
    thetaPlant0 = VbAngle
    epsilonPLL0 = (w - wsetPlant) / KiPLLplant
    wPlant0 = w
    epsilonP0 = (Po / wset - 1 / mp * (wset - w) - PsetPlant) / KiPlantP
    epsilonQ0 = (Qo - 1 / mq * (Vset - VoAbs) - QsetPlant) / KiPlantQ
    PoPlant0 = PoPlant
    QoPlant0 = QoPlant
    PsetDelay0 = Po - (wset - w) / mp
    QsetDelay0 = Qo - (Vset - VoAbs) / mq
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

    steadyStateValuesX = np.array([
        thetaPlant0, epsilonPLL0, wPlant0, epsilonP0, epsilonQ0,
        PoPlant0, QoPlant0, PsetDelay0, QsetDelay0, Theta0, Tef0,
        Qof0, Vof0, winv0, Psif0, Iid0, Iiq0, Vcd0, Vcq0, Iod0, Ioq0
    ])

    steadyStateValuesU = np.array([VbD, VbQ, w])

    return steadyStateValuesX, steadyStateValuesU
