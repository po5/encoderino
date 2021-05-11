from vapoursynth import core
import havsfunc as haf

revolution = core.d2v.Source("Start The Revolution Without Me.1970.WAC.Shack(Tik)/VTS_01_1.d2v")
revolution = core.vivtc.VFM(revolution, 1)
revolution = core.std.SelectEvery(revolution, cycle=5, offsets=[0, 2, 3, 4])
revolution = haf.Deblock_QED(revolution)

revolution.set_output()
