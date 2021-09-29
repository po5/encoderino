from vapoursynth import core, YUV444P8, YUV, RGBS
import vardefunc as vdf
import awsmfunc as awf
import havsfunc as haf
import lvsfunc as lvf
import vsTAAmbk as taa

digi = core.lsmas.LWLibavSource("[アニメ DVD] -DiGiCharat- デ・ジ・キャラット Vol1 第01話 「でじこが来たにょ」 (XviD 640x480 AC3).avi")

rgbs = core.resize.Bicubic(digi, format=RGBS, matrix_in_s="709", range_in_s="limited")

digi = lvf.deblock.autodb_dpir(rgbs, strs=[45, 55, 75], thrs=[(0.0, 0.0, 0.0), (1.0, 1.2, 1.5), (3.0, 3.8, 4.5)], cuda=False).resize.Bicubic(format=YUV444P8, matrix_s="170m")
digi = taa.TAAmbk(digi, "Eedi3")

dehalo = haf.FineDehalo(digi)
dehalo = core.std.Expr([digi, dehalo], "x y min")

edgefix = core.std.ShufflePlanes([dehalo, awf.fb(dehalo, left=1)], [0, 1, 2], YUV)
edgefix = awf.bbmod(edgefix, left=2, blur=20, thresh=30).std.Merge(edgefix, weight=[0.5, 0.5])

aa = core.std.Merge(lvf.aa.upscaled_sraa(edgefix, rfactor=2.0), edgefix, weight=[0.5, 0.5])

deband = vdf.deband.dumb3kdb(aa, threshold=40)

deband.set_output()
