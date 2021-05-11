from vapoursynth import core
import awsmfunc as awf
from rekt import rektlvls

there_was_a_crooked_man = core.lsmas.LWLibavSource("There.Was.a.Crooked.Man.1970.1080p.WEB-DL.DD+2.0.H.264-SbR.mkv")
there_was_a_crooked_man = core.std.SetFrameProp(there_was_a_crooked_man, "_Source", data="There Was a Crooked Man (1970)")
there_was_a_crooked_man = core.std.Crop(there_was_a_crooked_man, left=2, right=4, top=140, bottom=140)
there_was_a_crooked_man = awf.fb(there_was_a_crooked_man, right=1)
there_was_a_crooked_man = rektlvls(there_was_a_crooked_man, colnum=[1913,1914,1915], colval=[-2, -10, -10])

there_was_a_crooked_man.set_output()
