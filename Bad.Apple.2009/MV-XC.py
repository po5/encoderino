from vapoursynth import core
import vsTAAmbk as taa
import fvsfunc as fvf

apple = core.ffms2.Source('apple.mkv')

apple = core.std.Crop(apple, 2, 2, 2, 2)
apple = fvf.Depth(apple, 16)
apple = core.resize.Spline36(apple, 720, 540)

apple_d = core.placebo.Deband(apple, dither=False)
apple_ds = core.placebo.Deband(apple, iterations=2, threshold=10, radius=20, dither=False)
apple_dv = core.placebo.Deband(apple, iterations=4, threshold=23, radius=20, grain=0.7, dither=False)

apple = taa.TAAmbk(apple_d[:814] + apple_ds[814:821] + apple_d[821:1709] + apple_dv[1709:1812] + apple_d[1812:2950] + apple_ds[2950:3320] + apple_d[3320:3786], 2) + taa.TAAmbk(apple_d[3786:3793], 1) + taa.TAAmbk(apple_d[3793:4250], 2) + taa.TAAmbk(apple_d[4250:4316], 1) + taa.TAAmbk(apple_d[4316:4447], 2) + taa.TAAmbk(apple_d[4447:4559], 1) + taa.TAAmbk(apple_d[4559:4586], 2) + taa.TAAmbk(apple_d[4586:4612], 1) + taa.TAAmbk(apple_d[4612:4627], 2) + taa.TAAmbk(apple_d[4627:4652], 1) + taa.TAAmbk(apple_d[4652:4666], 2) + taa.TAAmbk(apple_d[4666:4836], 1) + taa.TAAmbk(apple_d[4836:5395], 2) + taa.TAAmbk(apple_d[5395:5653], 1) + taa.TAAmbk(apple_d[5653:5896], 2) + taa.TAAmbk(apple_d[5896:5986], 1) + taa.TAAmbk(apple_d[5986:6090], 2) + taa.TAAmbk(apple_d[6090:6118], 1) + taa.TAAmbk(apple_d[6118:6144], 2) + taa.TAAmbk(apple_d[6144:6163], 1) + taa.TAAmbk(apple_d[6163:6279], 2) + taa.TAAmbk(apple_d[6279:6290], 1) + taa.TAAmbk(apple_d[6290:6294], 2) + taa.TAAmbk(apple_d[6294:6318], 1) + taa.TAAmbk(apple_d[6318:6396], 2) + taa.TAAmbk(apple_d[6396:6416], 1) + taa.TAAmbk(apple_d[6416:6445] + apple_ds[6445:6461] + apple_d[6461:6499], 2) + apple_d[6499:6505] + taa.TAAmbk(apple_d[6505:6507], 2) + core.std.BlankClip(apple_d, length=54) + apple_d[6561:]

apple.set_output()
