def owoverlay(clip, image, func=core.resize.Spline36):
    image, image_mask = core.imwri.Read(image, alpha=True)
    if clip.width != image.width or clip.height != image.height:
        image = resizeroo(image, clip.width, clip.height, func, format=clip.format, matrix_s='709')
        image_mask = resizeroo(image_mask, clip.width, clip.height, func)
    return core.std.MaskedMerge(clip, image, image_mask)
