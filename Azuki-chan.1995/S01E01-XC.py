from vapoursynth import core
import havsfunc as haf
import vsTAAmbk as taa
import awsmfunc as awf
import fvsfunc as fvf
import kagefunc as kgf

a = core.ffms2.Source("azuki-chan episode 1.mkv")
a = a.vinverse.Vinverse()
a = a.std.Crop(left=4, right=8, top=2)
a = a.fb.FillBorders(right=1)
a = a.fb.FillBorders(left=1, mode="fixborders")
a = awf.bbmod(a, top=4, thresh=60, blur=10)
a = awf.bbmod(a, left=4, thresh=3, blur=500)
a = awf.bbmod(a, right=1, thresh=90, blur=40)
a = awf.bbmod(a, right=6, thresh=2, blur=100)
a = haf.FineDehalo(a)
a = taa.TAAmbk(a, "Nnedi3")
a = fvf.GradFun3(a, thr=0.35, radius=12, elast=8.0, mode=3, ampo=1, ampn=0, pat=32, dyn=False, staticnoise=False, thr_det=2 + round(max(1 - 0.35, 0) / 0.3), debug=False, thrc=1, radiusc=12, planes=list(range(a.format.num_planes)), ref=a, bits=a.format.bits_per_sample)
a = kgf.adaptive_grain(a, strength=.25, static=True, luma_scaling=12, show_mask=False)

a.set_output(0)
