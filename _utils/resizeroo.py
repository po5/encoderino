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
