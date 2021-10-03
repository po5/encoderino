from vapoursynth import core, YUV444P16, YUV420P10, YUV, RGBS
import awsmfunc as awf
import havsfunc as haf
import lvsfunc as lvf
import debandshit
from vsutil import depth
from rekt import rektlvls

core.max_cache_size = 2448

ep = core.lsmas.LWLibavSource("uloz/Di Gi Charat (complete)/Di Gi Charat/[アニメ DVD] -DiGiCharat- デ・ジ・キャラット Vol1 第01話 「でじこが来たにょ」 (XviD 640x480 AC3).avi")

epfix = depth(ep, 16)
epfix = epfix.std.Levels(min_in=0, max_in=235 << 8, min_out=16 << 8, max_out=235 << 8, planes=0)

epfix = epfix.resize.Bicubic(format=YUV444P16, matrix_in_s="170m", range_in_s="limited", dither_type="error_diffusion")
edgefix = core.std.ShufflePlanes([epfix, awf.fb(epfix, left=1)], [0, 1, 2], YUV)
epfix = awf.bbmod(edgefix, left=2, blur=20, thresh=30).std.Merge(edgefix, weight=[0.6, 0.4])
epfix = rektlvls(epfix, colnum=[638], colval=[8], prot_val=[70, 191])

epfix = epfix.resize.Bicubic(format=RGBS, matrix_in_s="170m", range_in_s="limited")
dpir = lvf.deblock.autodb_dpir(epfix, strs=[45, 55, 75], thrs=[(0.0, 0.0, 0.0), (1.0, 1.2, 1.5), (3.0, 3.8, 4.5)], cuda=False).resize.Bicubic(format=YUV444P16, matrix_s="170m", dither_type="error_diffusion")

dpir = haf.FineDehalo(dpir, rx=2, ry=2, brightstr=1.8, darkstr=0.2)
dpir = core.std.Merge(haf.FineDehalo(dpir, rx=1.8, ry=1.8, brightstr=1.8, darkstr=0), dpir, weight=[0.4, 0.6])

aa = core.std.Expr([lvf.aa.upscaled_sraa(dpir, rfactor=1.8), dpir], "x y min")
aa = core.std.Merge(lvf.aa.upscaled_sraa(aa, rfactor=2.2), aa, weight=[0.9, 0.1])

dpir = debandshit.dumb3kdb(aa.resize.Bicubic(format=YUV420P10, matrix_s="170m", dither_type="error_diffusion"), threshold=40, output_depth=10)

# freeze framing to frame +1
dpir = awf.ReplaceFrames(dpir, dpir[1:], "1154 1262 1341 1441 1522 1573 1609 1835 2357 2405 2477 2525 2530 2633 2688 3235 3283 3499 3978 4170 4174 4176 4207 4363 4425 4477 4645 4764 4773 4812 4849 5124 5143 5233 5285") # 3978 is questionable
# freeze framing to frame +2
dpir = awf.ReplaceFrames(dpir, dpir[2:], "1153 1261 1608 1834 2356 2404 2476 2524 2632 3234 3282 3498 4169 4173 4206 4362 4476 4644 4848 5142 5232")
# freeze framing to frame -1
dpir = awf.ReplaceFrames(dpir, dpir[0]+dpir, "1338 1340 1606 1976 2402 2475 2523 2631 2687 3281 3497 3904 4204 4360 4421 4474 4762 4846 4913 5146")
# freeze framing to frame -2
dpir = awf.ReplaceFrames(dpir, dpir[:2]+dpir, "1607 1977 2403 3905 4205 4361 4475 4763 4847 5147")
# apartment guide
dpir = awf.ReplaceFrames(dpir, dpir[2000]*2038, "[1982 2037]")

title = core.imwri.Read("title/01textless3.png").resize.Bicubic(format=YUV420P10, matrix_s="170m", dither_type="error_diffusion")
title = debandshit.dumb3kdb(title, threshold=40, output_depth=10) # just in case
title = title.std.AssumeFPS(dpir)
dpir = awf.ReplaceFrames(dpir, title*1153, "[1081 1152]")

dpir[1081:].set_output(0)
