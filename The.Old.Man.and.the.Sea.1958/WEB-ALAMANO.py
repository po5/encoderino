from vapoursynth import core
import awsmfunc as awf
import havsfunc as haf

old_man_and_the_sea = core.lsmas.LWLibavSource("The.Old.Man.and.the.Sea.1958.1080p.AMZN.WEB-DL.DDP2.0.H.264-ISA.mkv")
old_man_and_the_sea = core.fb.FillBorders(old_man_and_the_sea, left=2)
old_man_and_the_sea = awf.fb(old_man_and_the_sea, right=1)
old_man_and_the_sea = awf.bbmod(old_man_and_the_sea, right=4, thresh=505, blur=15)
old_man_and_the_sea = awf.bbmod(old_man_and_the_sea, left=4, thresh=500, blur=3)
old_man_and_the_sea = haf.Deblock_QED(old_man_and_the_sea)

old_man_and_the_sea.set_output()
