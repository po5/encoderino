def shifteroo(clip, left=0, top=0):
    og_w, og_h = clip.width, clip.height
    if left:
        clip = core.std.StackHorizontal([clip, clip])
    if top:
        clip = core.std.StackVertical([clip, clip])
    clip = clip.resize.Bicubic(src_left=left%og_w, src_top=top%og_h)
    clip = core.std.CropAbs(clip, og_w, og_h)
    return clip
