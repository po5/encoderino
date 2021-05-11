from vapoursynth import core
import awsmfunc as awf

firecreek = core.lsmas.LWLibavSource("Firecreek.1968.1080p.WEB-DL.DD+2.0.H.264-SbR.mkv")
firecreek = awf.fb(firecreek, right=1)
firecreek = awf.bbmod(firecreek, right=4, thresh=8, blur=30)

firecreek.set_output()
