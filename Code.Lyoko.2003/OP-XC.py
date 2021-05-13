from vapoursynth import core
import awsmfunc as awf
import fvsfunc as fvf
import lvsfunc as lvf
import G41Fun

lyokos = []

for ep in [3, 11, 12, 13, 14, 15, 17, 18, 19, 21, 22, 23, 24, 25, 26]:
    src = core.lsmas.LWLibavSource(f"Code.Lyoko.S01E{ep:02}.DVD.Remux.Multi-Odd_HD.mkv")[:1130]
    src = src.std.AssumeFPS(fpsnum=25)
    lyokos.append(fvf.Depth(awf.bbmod(fvf.AutoDeblock(src.vinverse.Vinverse(), adb1=0.2, adb2=0.8, adb1d=0.1, adb2d=1.4), top=6, bottom=4, thresh=4, blur=6), 16))

average = core.average.Mean(lyokos)
average = average.std.Crop(top=2, bottom=2, left=2, right=2)

lyoko = lvf.aa.upscaled_sraa(average, rfactor=2.0, rep=True)

deband = lyoko.f3kdb.Deband(range=2, grainy=16, grainc=16)

deband = awf.ReplaceFrames(deband, lyoko.f3kdb.Deband(range=15, grainy=32, grainc=32), "[417 425]")
deband = awf.ReplaceFrames(deband, lyoko, "435")

lyoko = awf.ReplaceFrames(deband, G41Fun.MaskedDHA(deband, rx=1.8, ry=1.8, darkstr=0.0, lowsens=70), "[384 420] [474 551] [606 673] [728 785]")
lyoko = fvf.Depth(lyoko, 8)

lyoko = lyoko[5:]
lyoko.set_output()
