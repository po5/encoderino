from vapoursynth import core
import awsmfunc as awf
import havsfunc as haf
import fvsfunc as fvf
import lvsfunc as lvf
import G41Fun

ep = 1

lyoko = core.lsmas.LWLibavSource(f"Code.Lyoko.S01E{ep:02}.DVD.Remux.Multi-Odd_HD.mkv")
lyoko = lyoko.std.AssumeFPS(fpsnum=25)
lyoko = lyoko.std.Crop(top=2, bottom=2, left=10, right=8)
lyoko = awf.fb(lyoko, left=1, right=1)

no_deblock = lyoko
lyoko = fvf.AutoDeblock(lyoko)
lyoko = haf.Deblock_QED(lyoko)
lyoko = awf.ReplaceFrames(lyoko, no_deblock, "[4864 4942]")

lyoko = awf.bbmod(lyoko, top=6, bottom=6, thresh=2, blur=5)
lyoko = lvf.aa.upscaled_sraa(lyoko, rfactor=3.0, rep=True)
lyoko = lyoko.vinverse.Vinverse()

no_deband = lyoko
lyoko = lyoko.placebo.Deband(radius=8, threshold=1.0)
lyoko = awf.ReplaceFrames(lyoko, no_deband, "[4864 4942]")

lyoko = G41Fun.MaskedDHA(lyoko, rx=1.8, ry=1.8, darkstr=0.0, lowsens=70)

lyoko.set_output()
