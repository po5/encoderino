from vapoursynth import core
import awsmfunc as awf

rio_bravo = core.ffms2.Source("Rio.Bravo.1959.REPACK.BluRay.Remux.1080p.VC-1.FLAC.1.0-HiFi.mkv")
rio_bravo = awf.fb(rio_bravo, left=1, right=1)
rio_bravo = awf.bbmod(rio_bravo, right=4, thresh=50, blur=200)

rio_bravo.set_output()
