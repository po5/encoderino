from vapoursynth import core, YUV444P8, YUV420P8
from rekt import rektlvls
import havsfunc as haf
import awsmfunc as awf
import lvsfunc as lvf
import G41Fun

guilstein = core.d2v.Source("Guilstein/VTS_01_1.d2v")[:163645]
guilstein = guilstein.decross.DeCross().dedot.Dedot().resize.Bicubic(format=YUV444P8, matrix_s="170m")
topline = guilstein.vinverse.Vinverse().std.Crop(top=63, bottom=70, left=6, right=6).std.CropAbs(top=1, width=guilstein.width-12, height=2)
guilstein = core.std.MaskedMerge(guilstein.vinverse.Vinverse().std.Crop(top=66, left=6, right=6), guilstein.std.Crop(top=66, left=6, right=6).nnedi3.nnedi3(1), guilstein.std.Crop(top=66, left=6, right=6).comb.CombMask().morpho.Dilate())
guilstein = guilstein.std.Crop(bottom=70)
guilstein = core.std.StackVertical([topline, guilstein])

guilstein = rektlvls(guilstein, rownum=[0, 1], rowval=[50, 10], colnum=[0, 1, 2, 3, 4], colval=[14, 10, 9, -3, -2], prot_val=[16, 235])
guilstein = awf.bbmod(guilstein, right=4, thresh=7, blur=16)
guilstein = core.std.Expr([guilstein, awf.bbmod(guilstein, bottom=3, thresh=2, blur=16)], "x y > x y ?")
guilstein = core.std.Expr([guilstein, awf.bbmod(guilstein, left=8, thresh=1, blur=8)], "x y > x y ?")
guilstein = lvf.aa.upscaled_sraa(guilstein, rfactor=2.0)
guilstein = guilstein.dfttest.DFTTest(sigma=2.0)
guilstein = guilstein.f3kdb.Deband(range=30, grainy=2, grainc=2)
guilstein = G41Fun.MaskedDHA(guilstein, rx=1.6, ry=1.6, darkstr=0.0, brightstr=0.6, lowsens=120, highsens=10)
guilstein = haf.EdgeCleaner(guilstein, strength=10)

guilstein = guilstein.resize.Bicubic(format=YUV420P8, matrix_s="170m")
guilstein = guilstein.std.FreezeFrames(first=[110471], last=[110483], replacement=[110470])

guilstein.set_output()
