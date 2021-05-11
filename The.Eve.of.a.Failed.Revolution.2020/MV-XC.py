from vapoursynth import core, YUV420P8, RGB24
import fvsfunc as fvf
import vsTAAmbk as taa
import awsmfunc as awf
import havsfunc as haf
import muvsfunc as muf
from glob import glob
from natsort import natsorted

av1 = core.lsmas.LWLibavSource(source="不革命前夜 - NEE [Dm2O_W6Rrss]-av1/不革命前夜 - NEE [Dm2O_W6Rrss].mkv") # for whatever reason ffms2 skipped frames
av1 = core.std.Crop(av1, top=132, bottom=132)
vp9 = core.ffms2.Source(source="不革命前夜 - NEE [Dm2O_W6Rrss]-vp9/不革命前夜 - NEE [Dm2O_W6Rrss].mkv")
vp9 = core.std.Crop(vp9, top=132, bottom=132)
h264 = core.lsmas.LWLibavSource(source="不革命前夜 - NEE [Dm2O_W6Rrss]-h264/不革命前夜 - NEE [Dm2O_W6Rrss].mkv")
h264 = core.std.Crop(h264, top=132, bottom=132)

grain = core.imwri.Read("grain_5301_5335_av1.png").resize.Bicubic(format=YUV420P8, matrix_s="709")
grain2 = vp9[3049]
grain3 = core.ffms2.Source("stitchdiff_final2.png").resize.Bicubic(format=YUV420P8, matrix_s="709")
bg = core.std.BlankClip(grain, color=[25, 30, 28], format=RGB24).resize.Bicubic(format=YUV420P8, matrix_s="709")

diff = core.std.MakeDiff(bg, grain, planes=[0,1,2])
diff2 = core.std.MakeDiff(bg, grain2, planes=[0,1,2])

av2 = core.std.MergeDiff(av1, diff2, planes=[0,1,2])
av1 = core.std.MergeDiff(av1, diff, planes=[0,1,2])
vp9 = core.std.MergeDiff(vp9, diff, planes=[0,1,2])
h264 = core.std.MergeDiff(h264, diff, planes=[0,1,2])

av1 = fvf.ReplaceFrames(av1, av1[17]*20, "[15 18]")
av1 = fvf.ReplaceFrames(av1, av1[21]*25, "[20 24]")
av1 = fvf.ReplaceFrames(av1, av1[26]*30, "[25 29]")
av1 = fvf.ReplaceFrames(av1, av1[51]*55, "[50 54]")
av1 = fvf.ReplaceFrames(av1, av1[66]*70, "[65 69]")
av1 = fvf.ReplaceFrames(av1, av1[81]*81, "80")
av1 = fvf.ReplaceFrames(av1, av1[86]*86, "85")
av1 = fvf.ReplaceFrames(av1, av1[212]*212, "211")
av1 = fvf.ReplaceFrames(av1, av1[294]*295, "[287 294]")
av1 = fvf.ReplaceFrames(av1, av1[411]*412, "410")
av1 = fvf.ReplaceFrames(av1, av1[1459]*1465, "[1460 1464]")
av1 = fvf.ReplaceFrames(av1, av1[4803]*4805, "[4801 4804]")
av1 = fvf.ReplaceFrames(av1, av1[4814]*4815, "4813")
av1 = fvf.ReplaceFrames(av1, av1[7755]*7756, "[7734 7754]")
av1 = fvf.ReplaceFrames(av1, av1[3893]*3896, "[3894 3895]")
av1 = fvf.ReplaceFrames(av1, av1[3900]*3901, "[3896 3900]")
av1 = fvf.ReplaceFrames(av1, av1[1:], "5 1428 1449 3886 3901 3922 3926 3962 4770 4780 4818 5888 6005 4786 4790 4795 3678 4891 4586 4601 4606 4616 5131")
av1 = fvf.ReplaceFrames(av1, av1[2:], "4785")
av1 = fvf.ReplaceFrames(av1, av1[0]+av1, "4784 4794 4799")
av2 = fvf.ReplaceFrames(av2, av2[5362]*5364, "5363")
av1 = fvf.ReplaceFrames(av1, vp9[6579]*6581, "6580")
av1 = fvf.ReplaceFrames(av1, vp9[6701]*6703, "[6701 6702]")
av1 = fvf.ReplaceFrames(av1, vp9[803]*808, "[804 807]")
av1 = fvf.ReplaceFrames(av1, vp9[275]*281, "[276 280]")
vp9 = fvf.ReplaceFrames(vp9, vp9[3]*5, "4")
vp9 = fvf.ReplaceFrames(vp9, vp9[1:], "13 1770 6012")
vp9 = fvf.ReplaceFrames(vp9, vp9[46]*50, "[45 49]")
vp9 = fvf.ReplaceFrames(vp9, vp9[202]*207, "[203 206]")
vp9 = fvf.ReplaceFrames(vp9, vp9[300]*301, "[295 300]")
vp9 = fvf.ReplaceFrames(vp9, vp9[1443]*1445, "1444")
vp9 = fvf.ReplaceFrames(vp9, vp9[0]+vp9, "[720 850] 1358 1359 1859 [2219 2225] 2500 4844 [5702 5704] [6061 6068] 6499 6546 4612 [2236 2239] [3648 3661] 3950 3961 3271 6500")
vp9 = fvf.ReplaceFrames(vp9, vp9[1:], "6062 6067")
vp9 = fvf.ReplaceFrames(vp9, vp9[2:], "6066")
h264 = fvf.ReplaceFrames(h264, h264[1:], "281 1748 1753 3951 4571 4566 4576 4581 6005 6402 6414 6505")
h264 = fvf.ReplaceFrames(h264, h264[0]+h264, "3671 6038 6043")
h264 = fvf.ReplaceFrames(h264, h264[3662]*3669, "[3663 3668]")

out = av1

out = fvf.ReplaceFrames(out, vp9, "[0 4] [10 14] [45 49] [70 74] [202 206] [223 232] [275 280] [295 311] [420 424] [573 577] [582 585] [596 601] [607 611] [613 622] [626 627] [633 636] [641 642] 645 [648 651] [656 666] [720 814] [979 981] [1003 1004] [1340 1342] [1358 1362] 1360 [1370 1374] [1380 1383] [1394 1398] [1404 1412] [1433 1434] [1441 1448] [1454 1458] [1465 1467] [1479 1482] [1491 1514] [1528 1530] [1554 1559] [1633 1634] [1651 1655] [1660 1664] [1674 1675] [1729 1730] [1760 1765] [1781 1794] [1810 1813] 1859 1938 [1985 1988] [1996 2000] [2006 2010] [2021 2025] 2184 [2195 2198] [2214 2225] [2236 2239] 2258 [2445 2478] [2483 2485] [2490 2493] [2499 2500] [2840 2842] [3258 3263] [3270 3271] [3289 3307] [3507 3531] [3648 3661] [3825 3833] [3838 3842] [3849 3871] [3946 3950] [3956 3961] [4288 4289] [4509 4513] [4611 4612] [4838 4850] [4863 4869] [5040 5043] [5053 5055] [5284 5285] [5406 5407] [5607 5609] [5692 5704] [5890 5895] [6005 6018] [6062 6068] [6477 6504] [6584 6585] 6613 [6638 6640] [6774 6780] 6705 [6779 6804] [6810 6817] [7089 7090] [7230 7234] [7264 7281] [7690 7691] [7731 7733]")
out = fvf.ReplaceFrames(out, av2, "[5286 5405] [6194 6273]")
out = fvf.ReplaceFrames(out, h264, "[281 286] [1731 1734] [1739 1759] [2183 2213] [2250 2253] [2453 2455] [2464 2467] [2480 2482] [2486 2489] [2494 2495] [2646 2747] [3662 3671] [3951 3955] [4563 4583] [6025 6049] [6056 6061] [6069 6109] [6367 6416] [6580 6583] [6586 6598] [6560 6612] [6629 6637] [6641 6643] [6651 6657] [6698 6700] 6735 [6835 6878] [7197 7198]")
out = fvf.ReplaceFrames(out, core.std.MaskedMerge(h264, av1, av1.std.Binarize(46)), "[3951 3955]")
out = fvf.ReplaceFrames(out, haf.YAHR(core.std.MaskedMerge(muf.abcxyz(out), out, out.std.Binarize(100))), "[1790 1794] [2266 2279]")
out = fvf.ReplaceFrames(out, taa.TAAmbk(out, 2), "[357 409] [761 850] [1785 1804] [2224 2252] [2258 2343] [2346 2430] [2436 2444] [2501 2588] [2646 3047] [3068 3249] [3472 3574] [3575 3671] [3575 3660] [3775 3824] [4355 4362] [4529 4539] [4770 4877] [4891 4995] [6417 6476] [7197 7204] [7795 7921]")
out = fvf.ReplaceFrames(out, core.placebo.Deband(out, iterations=2, threshold=10, radius=20), "[3672 3677]")

deband_s = core.placebo.Deband(av1, iterations=2, threshold=18, radius=9, dither=False)

sky_mask = out.std.Binarize(69) # nice
out = fvf.ReplaceFrames(out, core.std.MaskedMerge(out, deband_s, sky_mask), "[3886 4279]")

hair_mask = out.std.Binarize(48)
out = fvf.ReplaceFrames(out, core.std.MaskedMerge(h264, out, hair_mask), "[1760 1780]")

fix = awf.bbmod(out, top=12, bottom=8, thresh=2, blur=20)
fix_top = awf.bbmod(out, top=12, thresh=2, blur=20)
fix_bottom = awf.bbmod(out, bottom=8, thresh=2, blur=20)
fix_top_strong = awf.bbmod(out, top=12, thresh=90, blur=70)
fix_top_strong_bottom = awf.bbmod(fix_top_strong, bottom=8, thresh=2, blur=20)
fix_bottom_strong = awf.bbmod(out, bottom=8, thresh=90, blur=70)
fix_bottom_strong_top = awf.bbmod(fix_bottom_strong, top=12, thresh=2, blur=20)
fix_strong = awf.bbmod(out, top=12, bottom=8, thresh=90, blur=70)
fix_top_stronger = awf.bbmod(out, top=20, thresh=90, blur=70)
fix_stronger = awf.bbmod(out, top=20, bottom=8, thresh=90, blur=70)
fix_stronger = awf.bbmod(out, top=20, thresh=90, blur=70)
fix_strongest = awf.bbmod(out, top=34, bottom=8, thresh=90, blur=70)

fix = fvf.ReplaceFrames(fix, out, "[233 311] [668 760] [1465 1527] [1805 1809] [1896 1930] [1996 2034] [2095 2222] [2254 2257] [2589 2597] [2646 2747] [3048 3249] [3270 3307] [3463 3471] [3775 3885] [4280 4287] [5183 5510] [5739 5910] [6012 6134] [6142 6169] [6477 6499] [6774 6778] [6976 6987] [7731 7755] [7768 7781] [7922 8023]")
fix = fvf.ReplaceFrames(fix, fix_bottom, "[615 621] [1023 1227] [1299 1329] [1417 1427] [3672 3677] [4563 4769] [4878 4890] [5040 5075] [5134 5182] [6779 6802]")
fix = fvf.ReplaceFrames(fix, fix_top, "[1228 1270] [1384 1416] [1428 1464] [1844 1895] [5510 5606] [7795 7921]")
fix = fvf.ReplaceFrames(fix, fix_top_strong, "[851 953] [3678 3774]")
fix = fvf.ReplaceFrames(fix, fix_bottom_strong, "[3886 3929] [4290 4392] [4442 4479]")
fix = fvf.ReplaceFrames(fix, fix_bottom_strong_top, "[1330 1383] [2258 2265] [2275 2282] [4393 4442] [4489 4519] [4891 4995]")
fix = fvf.ReplaceFrames(fix, fix_top_strong_bottom, "[1790 1794] [6803 6812]")
fix = fvf.ReplaceFrames(fix, fix_strong, "[5 29] [4480 4483] [5661 5691] [6170 6193]")
fix = fvf.ReplaceFrames(fix, fix_stronger, "[5099 5117] [5126 5128] [5131 5133]")
fix = fvf.ReplaceFrames(fix, fix_top_stronger, "5118")
fix = fvf.ReplaceFrames(fix, fix_strongest, "[2035 2094]")

couch = core.imwri.Read("couch.png").resize.Bicubic(format=YUV420P8, matrix_s="709")
fix = fvf.ReplaceFrames(fix, couch*1665, "[1663 1664]")

gun_6648 = core.imwri.Read("gun_6648.png").resize.Bicubic(format=YUV420P8, matrix_s="709")
gun_6649 = core.imwri.Read("gun_6649.png").resize.Bicubic(format=YUV420P8, matrix_s="709")
gun_6650 = core.imwri.Read("gun_6650.png").resize.Bicubic(format=YUV420P8, matrix_s="709")
gun_6651 = core.imwri.Read("gun_6651.png").resize.Bicubic(format=YUV420P8, matrix_s="709")
fix = fvf.ReplaceFrames(fix, gun_6648*6649 + gun_6649 + gun_6650 + gun_6651*2, "[6648 6652]")

pool_3273 = core.imwri.Read("pool_3273.png").resize.Bicubic(format=YUV420P8, matrix_s="709")
pool_3277 = core.imwri.Read("pool_3277.png").resize.Bicubic(format=YUV420P8, matrix_s="709")
pool_3282 = core.imwri.Read("pool_3282.png").resize.Bicubic(format=YUV420P8, matrix_s="709")
pool_3306 = core.imwri.Read("pool_3306.png").resize.Bicubic(format=YUV420P8, matrix_s="709")
fix = fvf.ReplaceFrames(fix, pool_3273*3277, "[3272 3276]")
fix = fvf.ReplaceFrames(fix, pool_3277*3282, "[3277 3281]")
fix = fvf.ReplaceFrames(fix, pool_3282*3289, "[3282 3288]")
fix = fvf.ReplaceFrames(fix, pool_3306*3308, "[3297 3307]")

for file in natsorted(glob("umbrella_*.png")):
    frame = int(file.replace("umbrella_", "").replace(".png", ""))
    umbrella = core.imwri.Read(file).resize.Bicubic(format=YUV420P8, matrix_s="709")
    fix = fvf.ReplaceFrames(fix, umbrella*4626, f"[{frame} 4625]")

for file in natsorted(glob("cat_*.png")):
    frame = int(file.replace("cat_", "").replace(".png", ""))
    umbrella = core.imwri.Read(file).resize.Bicubic(format=YUV420P8, matrix_s="709")
    fix = fvf.ReplaceFrames(fix, umbrella*5131, f"[{frame} 5130]")

fix = fvf.ReplaceFrames(fix, taa.TAAmbk(fix, 2), "[5109 5182]")

frames = 1479-1465
stack = core.ffms2.Source("stitchlegsfinal2.png").resize.Bicubic(format=YUV420P8, matrix_s="709")
h = stack.height
def _push(n: int):
    return stack.resize.Spline36(height=h, src_top=(816 - h) * n / (frames - 1), src_height=h)
pushed = core.std.Crop(core.std.FrameEval(core.std.BlankClip(stack, length=frames), _push), top=h-816)

frames2 = 1491-1479
stack2 = core.ffms2.Source("stitchtummy_final3.png").resize.Bicubic(format=YUV420P8, matrix_s="709")
h2 = stack2.height
def _push2(n: int):
    return stack2.resize.Spline36(height=h2, src_top=(816 - h2) * n / (frames2 - 1), src_height=h2)
pushed = pushed + core.std.Crop(core.std.FrameEval(core.std.BlankClip(stack2, length=frames2), _push2), top=h2-816)

frames3 = 1528-1491
stack3 = core.ffms2.Source("stitchface_final.png")
h3 = stack3.height
def _push3(n: int):
    return stack3.resize.Spline36(height=h3, src_top=(816 - h3) * n / (frames3 - 1), src_height=h3)
pushed = pushed + core.std.Crop(core.std.FrameEval(core.std.BlankClip(stack3, length=frames3), _push3), top=h3-816).resize.Bicubic(format=YUV420P8, matrix_s="709")

pushed = core.std.MergeDiff(pushed, grain3, planes=[0,1,2])

image, image_mask = core.imwri.Read("lyrics_overlay_final.png", alpha=True)
image = image.resize.Bicubic(format=YUV420P8, matrix_s="709")
pushed = core.std.MaskedMerge(pushed, image, image_mask)

fix = fvf.ReplaceFrames(fix, core.std.AssumeFPS(fix[:1465] + pushed, fpsnum=fix.fps), "[1465 1527]")

fix.set_output()
