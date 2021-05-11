from vapoursynth import core
import havsfunc as haf
import awsmfunc as awf
from rekt import rektlvls
import mvsfunc

executive_action_tv = core.lsmas.LWLibavSource("Executive Action.mkv")
executive_action_tv = core.std.Crop(executive_action_tv, top=6, bottom=2)
executive_action_tv = rektlvls(executive_action_tv, colnum=[2,1917], colval=[20,12])
executive_action_tv = core.fb.FillBorders(executive_action_tv, left=2, right=2)
executive_action_tv = awf.fb(executive_action_tv, bottom=1)
executive_action_tv = awf.bbmod(executive_action_tv, left=6, top=4, bottom=6, thresh=15, blur=20)
executive_action_tv = awf.bbmod(executive_action_tv, right=6, thresh=5, blur=20)

executive_action_tv = core.resize.Bicubic(executive_action_tv, format=YUV444P8)

executive_action_ntsc = core.d2v.Source("Executive.Action.1973.NTSC.DVD5/VTS_01_1.d2v")[83:]
executive_action_ntsc = core.vivtc.VFM(executive_action_ntsc, 1)
executive_action_ntsc = core.std.SelectEvery(executive_action_ntsc, cycle=5, offsets=[0, 2, 3, 4])

executive_action_ntsc = executive_action_ntsc[928:]
executive_action_ntsc = mvsfunc.BM3D(executive_action_ntsc)
executive_action_ntsc = core.resize.Bicubic(executive_action_ntsc, format=YUV444P8)
executive_action_ntsc = haf.Padding(executive_action_ntsc, 3, 4, 4, 1)
executive_action_ntsc = core.resize.Spline36(executive_action_ntsc, executive_action_tv.width, executive_action_tv.height)

executive_action_mask = core.imwri.Read("executiveaction2.png", alpha=True)
executive_action_mask = core.std.ShufflePlanes(clips=executive_action_mask[0], planes=0, colorfamily=GRAY)
executive_action = core.std.MaskedMerge(executive_action_tv, executive_action_ntsc, executive_action_mask)

executive_action.set_output()
