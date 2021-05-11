from vapoursynth import core
import awsmfunc as awf
from rekt import rektlvls

deliverance = core.ffms2.Source("Deliverance.40th.Anniversary.Edition.1972.Bluray.Remux.1080p.VC-1.DTS-HD.MA.5.1-HiFi.mkv")
deliverance = core.std.Crop(deliverance, top=140, bottom=140)
deliverance = core.fb.FillBorders(deliverance, left=2)
deliverance = rektlvls(deliverance, colnum=[1916,1918], colval=[2,26])
deliverance = awf.fb(deliverance, right=1)
deliverance = awf.bbmod(deliverance, left=8, right=4, thresh=15, blur=20)

deliverance.set_output()
