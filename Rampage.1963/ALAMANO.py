from vapoursynth import core

rampage = core.d2v.Source("Rampage (1963)/VTS_01_1.d2v")
rampage = core.vivtc.VFM(rampage, 1)
rampage = core.std.SelectEvery(rampage, cycle=5, offsets=[0, 2, 3, 4])

rampage.set_output()
