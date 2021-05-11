from vapoursynth import core
import awsmfunc as awf
import havsfunc as haf

executive_action = core.lsmas.LWLibavSource("Executive.Action1973.1080p.AMZN.WEB-DL.DDP2.0.H.264-ISA.mkv")
executive_action = core.fb.FillBorders(executive_action, left=2, right=2)
executive_action = awf.bbmod(executive_action, left=4, right=4, top=4, thresh=55, blur=8)
executive_action = awf.bbmod(executive_action, bottom=2, thresh=55, blur=20)
executive_action = haf.Deblock_QED(executive_action)

executive_action.set_output()
