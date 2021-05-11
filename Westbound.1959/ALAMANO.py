from vapoursynth import core
import havsfunc as haf
from rekt import rektlvls

westbound = core.d2v.Source("Westbound/VTS_01_1.d2v")
westbound = core.vivtc.VFM(westbound, 1)
westbound = core.std.SelectEvery(westbound, cycle=5, offsets=[0, 1, 2, 3])
westbound = rektlvls(westbound, colnum=[719], colval=[20])
westbound = haf.Deblock_QED(westbound)

westbound.set_output()
