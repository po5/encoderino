from vapoursynth import core, YUV420P8
import awsmfunc as awf

heads = {}

hattoushin = core.std.BlankClip(width=1024, height=768, length=6000, fpsnum=15, color=[255, 255, 255])

fc = len(hattoushin)

head_start = -1

hattoushin_id = 12

head_first = True

for frame in range(fc):
    if head_start >= frame:
        continue

    head_end = frame
    if hattoushin_id not in heads:
        heads[hattoushin_id] = ""
    if head_first:
        head_end = 2
    head_first = False
    heads[hattoushin_id] += f"{frame} "
    head_start = head_end
    hattoushin_id += 1
    if hattoushin_id > 12:
        hattoushin_id = 1

for rng, frames in heads.items():
    hattoushin = awf.ReplaceFrames(hattoushin, core.std.AssumeFPS(core.imwri.Read(f"吹っ切れた/furifuri/fuirfuir-{rng:02}.png")*fc, fpsnum=15), frames)

hattoushin = core.std.AssumeFPS(hattoushin, fpsnum=15)

hattoushin = hattoushin.resize.Point(format=YUV420P8, matrix_s="709")[3:1353]

hattoushin.set_output()
