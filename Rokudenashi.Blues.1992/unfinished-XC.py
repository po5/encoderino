from vapoursynth import core
import awsmfunc as awf
import havsfunc as haf
import muvsfunc as muf
import vsTAAmbk as taa

src = core.lsmas.LWLibavSource("VBR.mkv")
src = src[:54023]
sr = muf.Cdeblend(src, omode=3)
sr = awf.ReplaceFrames(sr, src, "[0 441] [2791 2793] [2796 2797] [2807 2808] [2937 2951] [3006 3048] [4193 4228] [4981 4994] [5042 5146] [5358 5431] [51869 54022]")
sr = sr.placebo.Deband(threshold=3, radius=8, grain=0)
sr = taa.TAAmbk(sr, "Nnedi3SangNom")
dehalo = haf.DeHalo_alpha(sr)

dehalo.set_output()
