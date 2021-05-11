from vapoursynth import core, RGB24
from rekt import rektlvls
import vsTAAmbk as taa
import kagefunc as kgf
import awsmfunc as awf

cunny = core.d2v.Source("Imouto Jiru/DISC1.d2v")
cunny = cunny.vivtc.VFM(1)
cunny = cunny.vivtc.VDecimate()
cunny = cunny[:44972]
cunny = cunny.std.Crop(left=6, right=4)
cunny = awf.fb(cunny, top=1)
cunny = cunny.resize.Bicubic(src_top=1)
cunny = cunny.fb.FillBorders(top=1, bottom=1, mode="fixborders")
cunny = cunny.vinverse.Vinverse()
black = core.tcm.TColorMask(cunny.std.Minimum(), ["$000000"], tolerance=7, bt601=True, gray=False, lutthr=9)
cunny = rektlvls(cunny, colnum=[1, 709], colval=[-9, 35])
aa = taa.TAAmbk(cunny, "Nnedi3")
sangnom = taa.TAAmbk(cunny, "Nnedi3SangNom")
mask = kgf.retinex_edgemask(cunny).std.Binarize(200).std.Deflate(threshold=250)
cunny = cunny.placebo.Deband(threshold=6, radius=16, grain=4)
cunny = awf.ReplaceFrames(core.std.MaskedMerge(cunny, aa, mask), core.std.MaskedMerge(cunny, sangnom, mask), "[4708 4850] [5290 5421] [5542 5698] [5770 5803]")
no_bbmod = cunny
censor = cunny.fb.FillBorders(top=2, mode="fixborders")
censor = awf.bbmod(censor, top=4, thresh=200, blur=10)
censor = awf.bbmod(censor, right=4, thresh=2, blur=5)
censor = awf.bbmod(censor, left=4, thresh=6, blur=8)
censor = awf.bbmod(censor, right=1)
cunny = awf.bbmod(cunny, right=4, top=4, thresh=2, blur=5)
cunny = awf.bbmod(cunny, left=4, thresh=6, blur=8)
cunny = awf.bbmod(cunny, right=1)
cunny = core.std.MaskedMerge(cunny, no_bbmod, black)
cunny = awf.ReplaceFrames(cunny, no_bbmod, "[0 15] [42581 44935]")
cunny = awf.ReplaceFrames(cunny, censor, "[38311 38485]")
cunny.set_output()
