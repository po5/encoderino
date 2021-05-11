from vapoursynth import core
import havsfunc as haf
import fvsfunc as fvf
import vsTAAmbk as taa

gambo = core.lsmas.LWLibavSource("Tokyo Gambo 1-5/tokyo gambo 2.mp4")
gambo = core.std.SelectEvery(gambo, cycle=2, offsets=[0])
gambo = gambo.std.Crop(left=34, right=62)
gambo = gambo[13:]

gambo = gambo[:4504]

gambo = fvf.GradFun3(gambo, thr=0.35, radius=12, elast=8.0, mode=3, ampo=1, ampn=0, pat=32, dyn=False, staticnoise=False, thr_det=2 + round(max(1 - 0.35, 0) / 0.3), debug=False, thrc=1, radiusc=12, planes=list(range(gambo.format.num_planes)), ref=gambo, bits=gambo.format.bits_per_sample)
gambo = core.asharp.ASharp(gambo)
gambo = haf.FineDehalo(gambo)

gambo = taa.TAAmbk(gambo, "Nnedi3SangNom")

gambo = gambo.resize.Bicubic(height=844, width=int(gambo.width / gambo.height * 844 + 0.5))

gambo.set_output()
