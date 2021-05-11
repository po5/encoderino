from vapoursynth import core
from rekt import rektlvls
import awsmfunc as awf
import havsfunc
import fvsfunc as fvf
import kagefunc as kgf
import lvsfunc
#from acsuite import eztrim

ep1 = core.ffms2.Source("Sukeban.Deka.S01.480p.AMZN.WEB-DL.DDP2.0.H.264-ARiN/Sukeban.Deka.S01E01.480p.AMZN.WEB-DL.DDP2.0.H.264-ARiN.mkv")

#eztrim(ep1, [(24,36876)], 'Sukeban.Deka.S01E01.480p.AMZN.WEB-DL.DDP2.0.H.264-ARiN.track_2.ac3')

ep1 = ep1[24:36876]
ep1 = havsfunc.Deblock_QED(ep1)
ep1 = awf.bbmod(ep1, left=3, thresh=5, blur=4)
ep1 = core.fb.FillBorders(ep1, right=2)
ep1 = rektlvls(ep1, colnum=[2,638], colval=[-20,-17])
ep1 = awf.bbmod(ep1, right=4, thresh=40, blur=40)
ep1 = core.resize.Bicubic(ep1, src_left=-1)

ep1 = rektlvls(ep1, colnum=[0,4,5], colval=[-40,-30,-10])
ep1 = rektlvls(ep1, colnum=[0,1,3,4,5], colval=[20,-10,20,30,10])
ep1 = awf.bbmod(ep1, right=6, thresh=10, blur=10)
ep1 = awf.bbmod(ep1, left=7, thresh=10, blur=90)

ep1 = lvsfunc.misc.fix_cr_tint(ep1)

ep1 = fvf.GradFun3(ep1, thr=0.35, radius=12, elast=8.0, mode=3, ampo=1, ampn=0, pat=32, dyn=False, staticnoise=False, thr_det=2 + round(max(1 - 0.35, 0) / 0.3), debug=False, thrc=1, radiusc=12, planes=list(range(ep1.format.num_planes)), ref=ep1, bits=ep1.format.bits_per_sample)
ep1 = kgf.adaptive_grain(ep1, strength=.25, static=True, luma_scaling=12, show_mask=False)

ep1 = havsfunc.FineDehalo(ep1)

ep1.set_output(0)
