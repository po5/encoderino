from vapoursynth import core
import awsmfunc as awf

eighty_days = core.lsmas.LWLibavSource("Around.the.World.in.Eighty.Days.1956.1080p.AMZN.WEB-DL.DD+2.0.x264-ABM.mkv")
eighty_days = awf.fb(eighty_days, left=1, right=1, bottom=1)

eighty_days.set_output()
