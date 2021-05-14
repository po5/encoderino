from vapoursynth import core
import awsmfunc as awf
import havsfunc as haf
import fvsfunc as fvf
import lvsfunc as lvf
import G41Fun

ep = 2

source = core.lsmas.LWLibavSource(f"Code.Lyoko.S01E{ep:02}.DVD.Remux.Multi-Odd_HD.mkv")[1130:]
source = source.std.AssumeFPS(fpsnum=25)
source = source.std.Crop(top=6, bottom=2, left=10, right=8)
lyoko = awf.fb(source, left=1, right=1)
lyoko = lyoko.vinverse.Vinverse()
lyoko = fvf.Depth(lyoko, 16)
no_filter = lyoko
lyoko = awf.bbmod(lyoko, top=4, bottom=4, thresh=4, blur=4)
lyoko = fvf.AutoDeblock(lyoko, adb1=0.4, adb2=0.1, adb1d=0.3, adb2d=1.4)
aa2 = lvf.aa.upscaled_sraa(lyoko, rfactor=2.0, rep=True)
lyoko = lvf.aa.upscaled_sraa(lyoko, rfactor=3.0, rep=True)
lyoko = G41Fun.MaskedDHA(lyoko, rx=1.4, ry=1.4, darkstr=0.0, lowsens=70)
lyoko = awf.ReplaceFrames(lyoko, aa2, "[4189 4238] [4931 5386] [6796 6845] [9084 9133] [14670 14876] [16507 16556] [19215 19512] [19560 19662] [21924 22287] [22348 22486] [22577 22751] [23495 23843] [24354 25444] [25498 26806] [26950 27304] [27947 28648] [28751 29253] [29421 29768] [29824 29905] [30008 30104] [30250 30304] [30391 30419] [30506 30590] [30659 30699] [31071 31323]")
lyoko = lyoko.f3kdb.Deband(range=2, grainy=16, grainc=16)
lyoko = fvf.ReplaceFrames(haf.Deblock_QED(no_filter), lyoko, "[0 33399] [33650 33655]")

lyoko = fvf.Depth(lyoko, 10)

lyoko.set_output()
