from vapoursynth import core, RGB24
from rekt import rektlvls
import vsTAAmbk as taa
import kagefunc as kgf
import awsmfunc as awf

cunny = core.d2v.Source("Imouto Jiru/DISC2.d2v")
cunny = cunny.vivtc.VFM(1)
cunny = cunny.vivtc.VDecimate()
cunny = cunny[:41832]
cunny = cunny.std.Crop(left=6, right=4)
cunny = awf.fb(cunny, top=1)
cunny = cunny.resize.Bicubic(src_top=1)
cunny = cunny.fb.FillBorders(top=1, bottom=1, mode="fixborders")
cunny = cunny.vinverse.Vinverse()
no_rekt = cunny
black = core.tcm.TColorMask(cunny.std.Minimum(), ["$000000"], tolerance=7, bt601=True, gray=False, lutthr=9)
cunny = rektlvls(cunny, colnum=[1, 709], colval=[-9, 35])
cunny = awf.ReplaceFrames(cunny, no_rekt, "[0 11] [1485 1554] [38678 41831]")
aa = taa.TAAmbk(cunny, "Nnedi3")
sangnom = taa.TAAmbk(cunny, "Nnedi3SangNom")
mask = kgf.retinex_edgemask(cunny).std.Binarize(200).std.Deflate(threshold=250)
cunny = cunny.placebo.Deband(threshold=6, radius=16, grain=4)
cunny = awf.ReplaceFrames(core.std.MaskedMerge(cunny, aa, mask), core.std.MaskedMerge(cunny, sangnom, mask), "[1329 1501] [29378 29568] [31140 31499] [32495 32656]")
no_bbmod = cunny
cunny = awf.bbmod(cunny, right=4, top=4, thresh=2, blur=5)
cunny = awf.bbmod(cunny, left=4, thresh=6, blur=8)
cunny = awf.bbmod(cunny, right=1)
cunny = core.std.MaskedMerge(cunny, no_bbmod, black)
cunny = awf.ReplaceFrames(cunny, no_bbmod, "[0 11] [38678 41831]")
cunny.set_output()
