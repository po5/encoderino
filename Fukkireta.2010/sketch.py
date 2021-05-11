from vapoursynth import core, YUV444P8, YUV420P8, GRAY
import awsmfunc as awf
import havsfunc as haf
import functools
import ast

def nice_round(x, base=2):
    return base * round(x / base)

def resizeroo(clip, width, height, func=core.resize.Spline36, scale_x=1, scale_y=1, **more):
    scaled_width = clip.width * scale_x
    scaled_height = clip.height * scale_y
    ratio = max(width / scaled_width, height / scaled_height)
    clip = func(clip, nice_round(scaled_width * ratio), nice_round(scaled_height * ratio), **more)
    crop_left = (clip.width - width) / 2
    crop_top = (clip.height - height) / 2
    crop_right = crop_left
    crop_bottom = crop_top
    if crop_left % 2 == 1:
        crop_left += 1
        crop_right -= 1
    if crop_top % 2 == 1:
        crop_top += 1
        crop_bottom -= 1
    if crop_left or crop_right or crop_top or crop_bottom:
        clip = core.std.Crop(clip, crop_left, crop_right, crop_top, crop_bottom)
    return clip

def owoverlay(clip, image, func=core.resize.Spline36):
    image, image_mask = core.imwri.Read(image, alpha=True)
    if clip.width != image.width or clip.height != image.height:
        image = resizeroo(image, clip.width, clip.height, func, format=clip.format, matrix_s='709')
        image_mask = resizeroo(image_mask, clip.width, clip.height, func)
    return core.std.MaskedMerge(clip, image, image_mask)

def shifteroo(clip, left=0, top=0):
    og_w, og_h = clip.width, clip.height
    if left:
        clip = core.std.StackHorizontal([clip, clip])
    if top:
        clip = core.std.StackVertical([clip, clip])
    clip = clip.resize.Bicubic(src_left=left%og_w, src_top=top%og_h)
    clip = core.std.CropAbs(clip, og_w, og_h)
    return clip

heads = {}
hattoushin = {}

out = core.std.BlankClip(width=1024, height=768, length=6750, fpsnum=75, color=[255, 255, 255])
fc = len(out)

head_start = -1
hattoushin_start = -1

teto_id = 9
hattoushin_id = 11

head_first = True
hattoushin_first = True

for frame in range(fc):
    if frame > hattoushin_start:
        hattoushin_end = min(fc-1, frame+4)
        if hattoushin_id not in hattoushin:
            hattoushin[hattoushin_id] = ""
        if hattoushin_first:
            hattoushin_end = 3
        hattoushin_first = False
        hattoushin[hattoushin_id] += f"[{frame} {hattoushin_end}] "
        hattoushin_start = hattoushin_end
        hattoushin_id += 1
        if hattoushin_id > 12:
            hattoushin_id = 1

    if head_start >= frame:
        continue

    head_end = min(fc-1, frame+5)
    if teto_id not in heads:
        heads[teto_id] = ""
    if head_first:
        head_end = 2
    head_first = False
    heads[teto_id] += f"[{frame} {head_end}] "
    head_start = head_end
    teto_id += 1
    if teto_id > 10:
        teto_id = 1


mouths_lookup = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,4,4,1,1,1,3,4,2,2,3,5,5,2,2,4,4,0,5,5,5,0,5,5,4,5,1,1,4,4,5,5,4,4,5,5,0,0,2,2,4,4,4,1,1,2,2,2,1,1,1,2,2,5,2,3,2,0,0,0,4,4,3,4,4,4,3,2,5,5,5,2,2,1,1,1,1,1,4,4,4,5,5,5,0,0,3,4,2,2,3,2,2,5,5,5,2,2,4,4,4,3,3,4,4,4,5,5,2,2,3,2,1,2,2,5,5,5,0,0,2,2,2,0,2,4,3,4,2,2,3,2,2,5,5,5,5,5,2,2,1,1,1,2,2,3,3,4,4,0,0,3,4,3,3,2,4,3,3,3,2,3,3,3,3,2,5,5,5,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,3,4,4,4,4,4,3,3,3,2,4,3,3,3,3,3,2,2,2,1,1,1,5,5,5,1,1,4,4,3,3,3,3,3,4,0,0,0,0,3,2,2,2,2,3,4,4,4,4,1,2,2,2,2,3,0,4,4,4,3,2,0,2,2,3,2,2,1,1,1,1,1,1,0,0,0,0,0,0,0,5,5,5,5,5,5,5,2,2,3,5,5,5,5,5,5,0,2,2,3,2,2,0,5,5,5,0,1,1,3,3,3,4,4,4,0,0,0,0,0,1,1,1,1,1,1,5,5,5,5,3,3,3,3,4,4,3,3,3,2,2,2,2,2,5,5,3,3,5,5,5,5,3,3,2,3,5,5,5,0,5,5,5,5,0,0,5,5,5,5,2,2,2,2,3,2,2,3,3,2,4,3,5,5,5,5,4,4,4,3,3,3,3,4,0,0,0,0,0,3,2,2,2,2,4,4,4,4,4,1,1,1,1,1,0,0,2,2,2,3,2,2,2,2,3,5,5,4,1,1,1,4,0,0,0,0,0,0,0,5,5,5,5,5,5,5,2,2,2,3,1,1,1,1,1,1,0,0,0,3,3,4,4,0,5,5,5,2,2,3,2,2,2,2,3,0,0,0,0,5,5,5,5,5,5,5,1,1,1,1,1,2,2,2,3,2,5,5,5,3,4,3,3,3,2,3,3,3,5,5,5,2,2,2,5,5,5,5,0,3,2,2,2,2,3,2,2,2,5,5,0,3,3,3,2,3,3,4,0,4,3,4,2,2,5,5,4,4,2,3,4,3,3,3,2,2,2,2,4,4,3,5,2,2,3,2,2,4,4,4,2,2,2,5,5,5,5,5,4,4,4,2,2,2,5,5,0,2,2,1,1,0,2,2,3,2,4,3,2,3,2,2,3,3,5,0,5,5,5,2,2,2,1,5,5,0,2,2,4,3,4,5,5,1,1,5,5,2,2,3,5,4,4,0,0,0,2,2,4,3,2,2,5,5,3,2,2,2,5,5,2,4,3,2,3,2,3,4,2,3,2,2,4,4,1,1,5,5,5,0,0,5,5,5,5,4,4,1,1,1,3,4,2,2,3,5,5,2,2,4,4,0,5,5,5,0,5,5,4,5,1,1,4,4,5,5,4,4,5,5,0,0,2,2,4,4,4,1,1,2,2,2,1,1,1,2,2,5,2,3,2,0,0,0,4,4,3,4,4,4,3,2,5,5,5,2,2,1,1,1,1,1,4,4,4,5,5,5,0,0,3,4,2,2,3,2,2,5,5,5,2,2,4,4,4,3,3,4,4,4,5,5,2,2,3,2,1,2,2,5,5,5,0,0,2,2,2,0,2,4,3,4,2,2,3,2,2,5,5,5,5,5,2,2,1,1,1,2,2,3,3,4,4,0,0,3,4,3,3,2,4,3,3,3,2,3,3,3,3,2,5,5,5,5,0,0,4,4,1,1,2,2,1,2,3,5,5,5,5,0,2,2,1,1,1,2,5,1,1,1,2,2,1,1,3,2,5,1,1,1,1,1,1,1,1,1,1,1,1,0,0,4,4,4,4,4,3,3,5,5,0,5,5,5,5,1,1,2,2,3,2,5,5,1,1,1,0,0,2,3,2,2,1,2,3,2,2,2,2,0,0,2,0,4,4,4,5,5,5,3,2,2,4,4,4,2,2,2,2,3,2,2,2,2,2,3,3,3,3,2,3,3,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,5,2,3,4,3,4,4,0,2,2,2,2,1,2,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

mask = core.imwri.Read("catmask2.png", alpha=True)
mask = core.std.ShufflePlanes(clips=mask[0], planes=0, colorfamily=GRAY)

for rng, frames in heads.items():
    for start, end in ast.literal_eval("["+frames.replace(" ", ",")+"]"):
        try:
            mouth_id = mouths_lookup[start // 6]
        except Exception:
            mouth_id = 0
        out = awf.ReplaceFrames(out, core.std.AssumeFPS(core.imwri.Read(f"myteto/v3/sketch/tetoB{mouth_id}{rng:02}.png")*fc, fpsnum=75), f"[{start} {end}]") # use a cache here?

for rng, frames in hattoushin.items():
    cat = shifteroo(resizeroo(core.imwri.Read(f"吹っ切れた/furifuri/fuirfuir-{rng:02}.png").std.Crop(bottom=208), width=136, height=132), left=1)
    out = awf.ReplaceFrames(out, haf.Overlay(out, cat, y=out.height-cat.height, mask=mask), frames)

fucked = out.resize.Point(format=YUV420P8, matrix_s="170m")

fucked.set_output(0)
