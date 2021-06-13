from vapoursynth import core, RGBS, YUV444P8
import vardefunc as vdf
import awsmfunc as awf
import havsfunc as haf
import lvsfunc as lvf
import notvlc
import rekt

"""
the official NCED looks awful
taking advantage of the fact each credited ED has different credits,
we can use the credit mask to stack uncredited parts of each credited ED
until we get a full uncredited picture, that looks better than the official creditless
areas covered by all credited EDs are filled with a carefully matched version of the official creditless
"""

output = 0

def set_output(clip):
    global output
    clip.set_output(output)
    output += 1

def creditedvfm(clip):
    a = clip[:120].vivtc.VFM(1)
    b = clip[120:230].nnedi3cl.NNEDI3CL(1)
    c = clip[230:].vivtc.VFM(1)

    clip = a+b+c
    vinv = clip.vinverse.Vinverse()
    nnedi = core.nnedi3cl.NNEDI3CL(clip, field=1)

    clip = awf.ReplaceFrames(vinv, nnedi, "230 266 668 901 949 953 954 957 961 962 1091 1151 1580 [1582 1588] [1590 1599] 1600 1605 1608 1611 1638 1826 1858 2006 2012 2015 2133 2341 2385 2447 2585 2608 2620 2626 2634 2646 2658 2664 2669 2671 [2673 2675]")
    return clip

def creditlessvfm(clip):
    a = clip[:120].vivtc.VFM(1)
    b = clip[120:230].nnedi3cl.NNEDI3CL(1)
    c = clip[230:].vivtc.VFM(1)

    clip = a+b+c
    vinv = clip.vinverse.Vinverse()

    clip = awf.ReplaceFrames(vinv, core.nnedi3cl.NNEDI3CL(clip, field=1), "230 266 668 949 953 957 961 962 1091 1151 1580 1611 1638 1826 1858 2006 2133 2341 2385 2447 2585 2608 2620 2626 2634 2646 2658 2664 2669 2671")
    return clip

def ivtc(clip):
    clips = []
    clips.append(clip[:64])
    clips.append(clip[64:120].std.SelectEvery(cycle=5, offsets=[0, 2, 3, 4]))
    clips.append(clip[120:230])
    clips.append(clip[230:266].std.SelectEvery(cycle=5, offsets=[0, 1, 2, 3]))
    clips.append(clip[266:363].std.SelectEvery(cycle=5, offsets=[0, 1, 2, 3]))
    clips.append(clip[363:668])
    clips.append(clip[668:727].std.SelectEvery(cycle=5, offsets=[0, 1, 2, 3]))
    clips.append(clip[727:841])
    clips.append(clip[842:962].std.SelectEvery(cycle=4, offsets=[0, 1, 2]))
    clips.append(clip[962:1091].std.SelectEvery(cycle=5, offsets=[0, 1, 2, 3]))
    clips.append(clip[1091:1339].std.SelectEvery(cycle=5, offsets=[0, 1, 2, 3]))
    clips.append(clip[1339:1429].std.SelectEvery(cycle=5, offsets=[0, 1, 2, 4]))
    clips.append(clip[1429:1478])
    clips.append(clip[1478:1580].std.SelectEvery(cycle=5, offsets=[0, 1, 3, 4]))
    clips.append(clip[1580:1612])
    clips.append(clip[1612:1858].std.SelectEvery(cycle=5, offsets=[0, 1, 2, 3]))
    clips.append(clip[1858:1927])
    clips.append(clip[1927:2006].std.SelectEvery(cycle=5, offsets=[0, 1, 2, 4]))
    clips.append(clip[2006:2053])
    clips.append(clip[2053:2133].std.SelectEvery(cycle=5, offsets=[0, 1, 2, 4]))
    clips.append(clip[2133:2259])
    clips.append(clip[2259:2385].std.SelectEvery(cycle=5, offsets=[0, 1, 3, 4]))
    clips.append(clip[2385:2611])
    clips.append(clip[2612:2623])
    clips.append(clip[2624:2629])
    clips.append(clip[2630:2637])
    clips.append(clip[2638:2649])
    clips.append(clip[2650:2663])
    clips.append(clip[2664:])
    out = []
    for clip in clips:
        if not out:
            out = clip
        else:
            out += clip
    return out

sp = core.d2v.Source("Strawberry Panic DVD/STRAWBERRYPANIC_SP_01.d2v")
nced = notvlc.dvd_titles("Strawberry Panic DVD/STRAWBERRYPANIC_SP_01", sp, title=3, chapters=False)[15:2712]
nced = nced.tcomb.TComb()
nced = creditlessvfm(nced)
nced = nced.knlm.KNLMeansCL()
nced = lvf.denoise.bm3d(nced, sigma=1.0)
nced = nced.std.Crop(top=56, bottom=60)

sp1 = core.d2v.Source("Strawberry Panic DVD/STRAWBERRYPANIC_SP_01.d2v")
sp1 = notvlc.dvd_titles("Strawberry Panic DVD/STRAWBERRYPANIC_SP_01", sp1, titles=False) # credits: 4, 9 / creditless: 12
sp2 = core.d2v.Source("Strawberry Panic DVD/STRAWBERRYPANIC_SP_02.d2v")
sp2 = notvlc.dvd_titles("Strawberry Panic DVD/STRAWBERRYPANIC_SP_02", sp2, titles=False) # credits: 4, 9, 14
sp3 = core.d2v.Source("Strawberry Panic DVD/STRAWBERRYPANIC_SP_03.d2v")
sp3 = notvlc.dvd_titles("Strawberry Panic DVD/STRAWBERRYPANIC_SP_03", sp3, titles=False) # credits: 4, 9, 14
sp4 = core.d2v.Source("Strawberry Panic DVD/STRAWBERRYPANIC_SP_04.d2v")
sp4 = notvlc.dvd_titles("Strawberry Panic DVD/STRAWBERRYPANIC_SP_04", sp4, titles=False) # credits: 4, 9, 14
sp5 = core.d2v.Source("Strawberry Panic DVD/STRAWBERRYPANIC_SP_05.d2v")
sp5 = notvlc.dvd_titles("Strawberry Panic DVD/STRAWBERRYPANIC_SP_05", sp5, titles=False) # credits: 4, 9

eds = []

for disc in [sp1, sp2, sp3, sp4]:
    eds.append(disc[3])
    eds.append(disc[8])

eds.append(sp5[3])

for disc in [sp2, sp3, sp4]:
    eds.append(disc[13])

worst_to_best = [eds[7], eds[10], eds[2], eds[3], eds[1], eds[9], eds[4], eds[0], eds[8], eds[11], eds[6], eds[5]]

merged = nced
merged = awf.ReplaceFrames(merged, core.std.Levels(merged, min_in=0, max_in=255, min_out=0, max_out=249, planes=0), "[120 229] [668 726]")
merged = awf.ReplaceFrames(merged, core.std.Levels(merged, min_in=0, max_in=255, min_out=0, max_out=249, planes=0), "[726 775]")
merged = awf.ReplaceFrames(merged, core.std.Levels(merged, min_in=0, max_in=255, min_out=0, max_out=249, planes=0), "[775 836]")
merged = awf.ReplaceFrames(merged, core.std.Levels(merged, min_in=0, max_in=255, min_out=0, max_out=249, planes=0), "[836 961]")
merged = awf.ReplaceFrames(merged, core.std.Levels(merged, min_in=0, max_in=255, min_out=0, max_out=251, planes=0), "[2507 2584]")
merged = awf.ReplaceFrames(merged, core.std.Levels(merged, min_in=0, max_in=253, min_out=0, max_out=253, planes=0), "[120 214]")
merged = awf.ReplaceFrames(merged, core.std.Levels(merged, min_in=0, max_in=252, min_out=0, max_out=253, planes=0), "[215 229]")
merged = core.resize.Bicubic(merged, format=RGBS)
merged = core.timecube.Cube(merged, cube="credits.cube")
merged = core.resize.Bicubic(merged, format=nced.format, matrix_s="170m", src_left=-0.1)
merged = haf.ContraSharpening(merged, eds[0].std.Crop(top=56, bottom=60))
yes = merged

#damage = core.std.BlankClip(nced)

for i, ed in enumerate(worst_to_best):
    nnedi = core.nnedi3cl.NNEDI3CL(ed, field=1)

    ed = creditedvfm(ed)

    if i in [2, 5]:
        ed = awf.ReplaceFrames(ed, nnedi, "2011 2023")
    if i in [2]:
        ed = awf.ReplaceFrames(ed, nnedi, "2013 2021 2025 2029 2031 2035")
    if i in [5]:
        ed = awf.ReplaceFrames(ed, nnedi, "2014 2020 2026")
    if i in [2, 5, 10]:
        ed = awf.ReplaceFrames(ed, nnedi, "2017")
    if i in [6]:
        ed = awf.ReplaceFrames(ed, nnedi, "2018 2024 2051")
    if i in [2, 11]:
        ed = awf.ReplaceFrames(ed, nnedi, "2019 2033 2036")
    if i in [6, 10]:
        ed = awf.ReplaceFrames(ed, nnedi, "2030")
    if i in [11]:
        ed = awf.ReplaceFrames(ed, nnedi, "2043 2047 2050")

    ed = ed.std.Crop(top=56, bottom=60)

    ededge = rekt.rekt_fast(yes, fun = lambda m: ed.std.Crop(left=4, right=4), left=4, right=4)

    diff = vdf.mask.Difference().creditless(src_clip=ededge+ededge[0], credit_clip=ededge, nc_clip=nced, start_frame=0, thr=70, prefilter=True, expand=5)
    diffedge = vdf.mask.Difference().creditless(src_clip=ededge+ededge[0], credit_clip=ededge, nc_clip=nced, start_frame=0, thr=20, prefilter=True, expand=5)

    diff = core.std.StackVertical([diffedge.std.CropAbs(width=diffedge.width, height=4), diff.std.Crop(top=4, bottom=4), diffedge.std.CropAbs(width=diffedge.width, height=4, top=360)])[:-1]

    diff = diff.std.Deflate().std.Deflate().std.Deflate()
    merged = core.std.MaskedMerge(ed, merged, diff)
    #damage = core.std.MaskedMerge(ed, damage, diff)

merged = merged.std.Crop(left=2, right=2)
merged = core.resize.Bicubic(merged, format=YUV444P8)
merged = merged.std.Crop(left=1, right=1)
merged = rekt.rektlvls(merged, rownum=[0], rowval=[10])
merged = merged.fb.FillBorders(bottom=1, left=1, mode="fixborders")
merged = awf.bbmod(merged, top=8, thresh=2, blur=4)
merged = awf.bbmod(merged, left=6, right=6, thresh=2, blur=10)
merged = awf.bbmod(merged, bottom=2, thresh=4, blur=4)
merged = merged.std.AddBorders(top=56, bottom=60)

set_output(ivtc(merged))
