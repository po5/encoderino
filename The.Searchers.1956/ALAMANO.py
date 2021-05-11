from vapoursynth import core
import awsmfunc as awf
import havsfunc as haf

the_searchers = core.ffms2.Source("The.Searchers.1956.BluRay.Remux.1080p.VC-1.AC3.1.0-decibeL.mkv")
the_searchers = haf.Deblock_QED(the_searchers)
the_searchers = awf.fb(the_searchers, top=1, bottom=1, right=1)
the_searchers = core.fb.FillBorders(the_searchers, left=2)
the_searchers = awf.bbmod(the_searchers, top=6, right=4, thresh=55, blur=200)
the_searchers = awf.bbmod(the_searchers, left=8, thresh=200, blur=20)

the_searchers.set_output()
