from vapoursynth import core, GRAY, YUV, YUV444P16, YUV420P10
import awsmfunc as awf
import lvsfunc as lvf
import havsfunc as haf
import vardefunc as vdf
from rekt import rektlvls

src = core.ffms2.Source("[SubsPlease] Nomad - Megalo Box 2 - 01 (1080p) [99D681F1].mkv")
fb = rektlvls(src, colnum=[0, 1919], colval=[15, 15])
fb = rektlvls(fb, rownum=[0, 1079], rowval=[16, 16])
descale = lvf.scale.descale(fb, upscaler=None, height=720, kernel=lvf.kernels.Bicubic(b=0, c=1))
descale = lvf.scale.descale(descale, upscaler=None, height=405, kernel=lvf.kernels.Bicubic(b=0, c=1/2))
downscale = fb.resize.Spline36(width=descale.width, height=descale.height, format=YUV444P16)
descale = descale.resize.Spline36(format=YUV444P16)
u = core.std.ShufflePlanes(downscale, planes=[1], colorfamily=GRAY)
v = core.std.ShufflePlanes(downscale, planes=[2], colorfamily=GRAY)
descale = core.std.ShufflePlanes([descale, u, v], planes=[0, 0, 0], colorfamily=YUV)
deband = descale.placebo.Deband(threshold=3, radius=8, grain=0)
rescale = vdf.fsrcnnx_upscale(deband, 1920, 1080, shader_file="FSRCNNX_x2_56-16-4-1.glsl").resize.Spline36(1920, 1080)
rescale = vdf.merge_chroma(rescale, deband.resize.Spline36(width=1920, height=1080))
rescale = awf.ReplaceFrames(rescale, haf.Deblock_QED(src).placebo.Deband(threshold=3, radius=8, grain=0).resize.Spline36(format=YUV444P16), "[0 167] [662 757] [806 901] [950 1045] [1130 1125] [1418 1513] [2514 2637] [32698 34694]")
rescale = awf.ReplaceFrames(rescale, fb.placebo.Deband(threshold=3, radius=8, grain=0).resize.Spline36(format=YUV444P16), "[168 601] [25058 25185]")
rescale = rescale.resize.Spline36(format=YUV420P10, dither_type="error_diffusion")

rescale.set_output()
