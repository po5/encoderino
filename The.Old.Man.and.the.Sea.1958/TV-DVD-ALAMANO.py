from vapoursynth import core
import havsfunc as haf
import bakafunc

def nice_round(x, base=2):
    return base * round(x / base)

def resizeroo(clip, width, height, func=core.resize.Spline36, scale_x=1, scale_y=1, top=False, bottom=False, **more):
    scaled_width = clip.width * scale_x
    scaled_height = clip.height * scale_y
    ratio = max(width / scaled_width, height / scaled_height)
    clip = func(clip, nice_round(scaled_width * ratio), nice_round(scaled_height * ratio), **more)
    crop_left = (clip.width - width) / 2
    crop_top = (clip.height - height) / 2
    crop_right = crop_left
    crop_bottom = crop_top
    if top:
        crop_bottom += crop_top
        crop_top = 0
    if bottom:
        crop_top += crop_bottom
        crop_bottom = 0
    if crop_left % 2 == 1:
        crop_left += 1
        crop_right -= 1
    if crop_top % 2 == 1:
        crop_top += 1
        crop_bottom -= 1
    if crop_left or crop_right or crop_top or crop_bottom:
        clip = core.std.Crop(clip, crop_left, crop_right, crop_top, crop_bottom)
    return clip

resolution = (1280, 720)

old_man_and_the_sea_ntsc = core.d2v.Source("The Old Man and the Sea - 1958 - John Sturges/VTS_01_1.d2v")
old_man_and_the_sea_ntsc = core.vivtc.VFM(old_man_and_the_sea_ntsc, 1)
old_man_and_the_sea_ntsc = core.std.SelectEvery(old_man_and_the_sea_ntsc, cycle=5, offsets=[0, 2, 3, 4])
old_man_and_the_sea_ntsc = haf.Deblock_QED(old_man_and_the_sea_ntsc)
old_man_and_the_sea_ntsc = core.std.Crop(old_man_and_the_sea_ntsc, left=8, right=8)
old_man_and_the_sea_ntsc = bakafunc.LazyChromaBleedFix(old_man_and_the_sea_ntsc)

old_man_and_the_sea_ntsc = core.std.Crop(old_man_and_the_sea_ntsc, bottom=36)
old_man_and_the_sea_ntsc = core.resize.Bicubic(old_man_and_the_sea_ntsc, format=YUV444P8)
old_man_and_the_sea_ntsc = core.std.Crop(old_man_and_the_sea_ntsc, left=1)
old_man_and_the_sea_ntsc = core.knlm.KNLMeansCL(old_man_and_the_sea_ntsc)
old_man_and_the_sea_ntsc = resizeroo(old_man_and_the_sea_ntsc, *resolution, scale_x=(16/9)/(4/3))

old_man_and_the_sea_tv = core.lsmas.LWLibavSource("Az öreg halász és a tenger.mkv")
old_man_and_the_sea_tv = core.std.Crop(old_man_and_the_sea_tv, top=6, bottom=6, left=12, right=24)

old_man_and_the_sea_tv = core.resize.Bicubic(old_man_and_the_sea_tv, format=YUV444P8)
old_man_and_the_sea_tv = core.std.Crop(old_man_and_the_sea_tv, bottom=80)
old_man_and_the_sea_tv = resizeroo(old_man_and_the_sea_tv, *resolution, scale_y=0.671)
old_man_and_the_sea_tv = old_man_and_the_sea_tv[:3727] + old_man_and_the_sea_tv

old_man_and_the_sea_mask = core.imwri.Read("oldman.png", alpha=True)
old_man_and_the_sea_mask = core.std.ShufflePlanes(clips=old_man_and_the_sea_mask[0], planes=0, colorfamily=GRAY)
old_man_and_the_sea = core.std.MaskedMerge(old_man_and_the_sea_tv, old_man_and_the_sea_ntsc, resizeroo(old_man_and_the_sea_mask, *resolution))

old_man_and_the_sea.set_output()
