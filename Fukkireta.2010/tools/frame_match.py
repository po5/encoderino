from vapoursynth import core, RGB24
from PIL import Image

dupes = core.ffms2.Source("ron.mp4")
mouths = core.std.SelectEvery(dupes[1:409], cycle=12, offsets=[0, 2, 5, 8, 10]) + core.std.SelectEvery(dupes[410:], cycle=12, offsets=[0, 2, 5, 8, 10])
mouths = mouths[:759] + mouths[759] + mouths[759:823] + mouths[824:]
mouths = core.std.AssumeFPS(dupes[:1] + mouths, mouths)
mouths = core.std.Crop(mouths, top=400, bottom=196, left=320, right=270)

rgb = core.resize.Bicubic(mouths, format=RGB24, matrix_in_s="470bg")
rgb = core.imwri.Write(rgb, "PNG", "mouths/%04d.png")

framenumber = 0
teto_id = 9
mouth_cache = {}

for frame in rgb.frames():
    i1 = Image.open(f"mouths/{framenumber:04}.png")
    scores = {}
    for mouth_id in [0, 1, 2, 3, 4, 5]:
        if f"{teto_id}_{mouth_id}" not in mouth_cache:
            i2 = Image.open(f"teto-psd/tetoB0{teto_id:02}/(invalid UTF-8 string) #6/tetoB{mouth_id}{teto_id:02}.png")
            i2 = i2.resize((dupes.width, dupes.height)).crop((320, 400, dupes.width-270, dupes.height-196)).convert("RGB")
            mouth_cache[f"{teto_id}_{mouth_id}"] = i2
        else:
            i2 = mouth_cache[f"{teto_id}_{mouth_id}"]
        assert i1.mode == i2.mode, "Different kinds of images."
        assert i1.size == i2.size, "Different sizes."
         
        pairs = zip(i1.getdata(), i2.getdata())
        if len(i1.getbands()) == 1:
            dif = sum(abs(p1-p2) for p1,p2 in pairs)
        else:
            dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
        ncomponents = i1.size[0] * i1.size[1] * 3
        diff_percentage = (dif / 255.0 * 100) / ncomponents
        scores[mouth_id] = diff_percentage
    best_mouth = min(scores, key=scores.get)
    print("frame", framenumber, "mouth", best_mouth, "diff", scores[best_mouth])
    framenumber += 1
    teto_id += 1
    if teto_id > 10:
        teto_id = 1
