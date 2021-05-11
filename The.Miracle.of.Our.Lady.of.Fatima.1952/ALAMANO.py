from vapoursynth import core
import awsmfunc as awf

lady_of_fatima = core.ffms2.Source("The.Miracle.of.Our.Lady.of.Fatima.1952.1080p.WEB-DL.DD+2.0.H.264-SbR.mkv")
lady_of_fatima = core.std.Crop(lady_of_fatima, left=2, right=2)
lady_of_fatima = core.fb.FillBorders(lady_of_fatima, right=1)
lady_of_fatima = awf.bbmod(lady_of_fatima, right=2, thresh=15, blur=20)

lady_of_fatima.set_output()
