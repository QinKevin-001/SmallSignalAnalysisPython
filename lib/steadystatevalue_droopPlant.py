#DONT TOUCH
import numpy as np
import cmath

def steadystatevalue_droopPlant(w, Vb, Io, parasIBR):
    # Extract parameters
    KiPLLplant = parasIBR['KiPLLplant']
    KiPlantP   = parasIBR['KiPlantP']
    KiPlantQ   = parasIBR['KiPlantQ']
    PsetPlant  = parasIBR['PsetPlant']
    QsetPlant  = parasIBR['QsetPlant']
    wsetPlant  = parasIBR['wsetPlant']
    wset       = parasIBR['wset']
    Vset       = parasIBR['Vset']
    mp         = parasIBR['mp']
    mq         = parasIBR['mq']
    Rt         = parasIBR['Rt']
    Lt         = parasIBR['Lt']
    Rd         = parasIBR['Rd']
    Cf         = parasIBR['Cf']
    Rc         = parasIBR['Rc']
    Lc         = parasIBR['Lc']
    KiV        = parasIBR['KiV']
    KiC        = parasIBR['KiC']

    # Calculate phasor values and power flow quantities
    VbAngle = cmath.phase(Vb)
    VbD = Vb.real
    VbQ = Vb.imag
    IoD = Io.real
    IoQ = Io.imag
    PoPlant = VbD * IoD + VbQ * IoQ
    QoPlant = VbQ * IoD - VbD * IoQ
    Vo = Vb + (Rc + 1j * w * Lc) * Io
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
    Ic = Vo / (Rd + 1/(1j * w * Cf))
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
    Vi = Vo + (Rt + 1j * w * Lt) * Ii
    ViAbs = abs(Vi)
    ViAngle = cmath.phase(Vi)
    Vid = ViAbs * np.cos(ViAngle - VoAngle)
    Viq = ViAbs * np.sin(ViAngle - VoAngle)

    # Steady-state calculations (MATLAB ordering)
    thetaPlant0   = VbAngle
    epsilonPLL0   = (w - wsetPlant) / KiPLLplant
    wPlant0       = w
    epsilonP0     = (Po - (wset - w) / mp - PsetPlant) / KiPlantP
    epsilonQ0     = (Qo - (Vset - VoAbs) / mq - QsetPlant) / KiPlantQ
    PoPlant0      = PoPlant
    QoPlant0      = QoPlant
    # Delay states as per MATLAB:
    PsetDelay0    = Po - (wset - w) / mp
    QsetDelay0    = Qo - (Vset - Vod) / mq
    Theta0        = VoAngle
    Po0           = Po
    Qo0           = Qo
    Phid0         = Iid / KiV
    Phiq0         = Iiq / KiV
    Gammad0       = (Vid + wset * Lt * Iiq) / KiC
    Gammaq0       = (Viq - wset * Lt * Iid) / KiC
    Iid0          = Iid
    Iiq0          = Iiq
    Vcd0          = Vcd
    Vcq0          = Vcq
    Iod0          = Iod
    Ioq0          = Ioq

    steadyStateValuesX = np.array([
        thetaPlant0, epsilonPLL0, wPlant0, epsilonP0, epsilonQ0,
        PoPlant0, QoPlant0, PsetDelay0, QsetDelay0, Theta0,
        Po0, Qo0, Phid0, Phiq0, Gammad0, Gammaq0, Iid0, Iiq0,
        Vcd0, Vcq0, Iod0, Ioq0
    ])
    steadyStateValuesU = np.array([VbD, VbQ, w])

    return steadyStateValuesX, steadyStateValuesU