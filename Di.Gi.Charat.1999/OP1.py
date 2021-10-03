from vapoursynth import core, YUV444P16, YUV420P10, YUV, RGBS, GRAY16
import awsmfunc as awf
import havsfunc as haf
import lvsfunc as lvf
import rvsfunc as rvf
import debandshit
import G41Fun
from vsutil import depth
from rekt import rektlvls

core.max_cache_size = 2248

op = core.lsmas.LWLibavSource("uloz/Di Gi Charat (complete)/Di Gi Charat/[アニメ DVD] -DiGiCharat- デ・ジ・キャラット Vol1 第01話 「でじこが来たにょ」 (XviD 640x480 AC3).avi")

opfix = depth(op, 16)
opfix = opfix.std.Levels(min_in=0, max_in=235 << 8, min_out=16 << 8, max_out=235 << 8, planes=0)

opfix = opfix.resize.Bicubic(format=YUV444P16, matrix_in_s="170m", range_in_s="limited", dither_type="error_diffusion")
edgefix = core.std.ShufflePlanes([opfix, awf.fb(opfix, left=1)], [0, 1, 2], YUV)
opfix = awf.bbmod(edgefix, left=2, blur=20, thresh=30).std.Merge(edgefix, weight=[0.6, 0.4])
opfix = rektlvls(opfix, colnum=[638], colval=[8], prot_val=[60, 190]) # 692 957 805

opfix = opfix.resize.Bicubic(format=RGBS, matrix_in_s="170m", range_in_s="limited")
dpir = lvf.deblock.autodb_dpir(opfix, strs=[55, 65, 115], thrs=[(0.0, 0.0, 0.0), (1.0, 1.2, 1.5), (3.0, 3.8, 4.5)], cuda=False).resize.Bicubic(format=YUV444P16, matrix_s="170m", dither_type="error_diffusion")

dpir = haf.FineDehalo(dpir, rx=2, ry=2, brightstr=1.8, darkstr=0.2)
#dpir = core.std.Merge(haf.FineDehalo(dpir, rx=1.8, ry=1.8, brightstr=1.8, darkstr=0), dpir, weight=[0.4, 0.6])

# >
opfix = core.std.Expr([opfix.resize.Bicubic(format=YUV444P16, matrix_s="170m", dither_type="error_diffusion"), dpir], "x y min")
opfix = lvf.deblock.vsdpir(opfix, strength=10, matrix=opfix.get_frame(0).props["_Matrix"], cuda=False)

mask = rvf.masking.fineline_mask(G41Fun.Hysteria(opfix, lthr=180, hthr=1, lcap=255), thresh=30).std.Maximum().std.BoxBlur().resize.Spline36(format=GRAY16)
opfix = core.std.MaskedMerge(dpir, core.std.Merge(opfix, dpir, weight=[0.6, 0.4]), mask)
# <

aa = core.std.Expr([lvf.aa.upscaled_sraa(opfix, rfactor=1.8), opfix], "x y min")
aa = core.std.Merge(lvf.aa.upscaled_sraa(aa, rfactor=2.2), aa, weight=[0.9, 0.1])

dpir = debandshit.dumb3kdb(aa.resize.Bicubic(format=YUV420P10, matrix_s="170m", dither_type="error_diffusion"), threshold=40, output_depth=10)

# freeze framing to frame +1
dpir = awf.ReplaceFrames(dpir, dpir[1:], "312 382 405 446 463 484 486 488 521 523 525 527 529 551 554 556 558 560 562 639 641 643 647 649 651 655 657 659 700 702 704 706 708 1059") # 312 is questionable
# freeze framing to frame +2
dpir = awf.ReplaceFrames(dpir, dpir[2:], "311 381 445 483 520 550") # 311 is questionable
# freeze framing to frame -1
dpir = awf.ReplaceFrames(dpir, dpir[0]+dpir, "249 267 310 316 342 410 549") # 316 is questionable
# freeze framing to frame -2
dpir = awf.ReplaceFrames(dpir, dpir[:2]+dpir, "343")

title = core.imwri.Read("title/final-digi-op1_268-fix.png").resize.Bicubic(format=YUV420P10, matrix_s="170m", dither_type="error_diffusion")
title = title.std.AssumeFPS(dpir)
dpir = awf.ReplaceFrames(dpir, title*269, "268")

dpir[:1081].set_output(0)
