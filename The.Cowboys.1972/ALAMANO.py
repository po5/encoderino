from vapoursynth import core
import awsmfunc as awf

the_cowboys = core.ffms2.Source("The.Cowboys.1972.BluRay.Remux.1080p.VC-1.DD.5.1-DrBlaze.mkv")
the_cowboys = core.std.Crop(the_cowboys, top=142, bottom=142, left=6, right=6)
the_cowboys = awf.fb(the_cowboys, right=1)
the_cowboys = awf.bbmod(the_cowboys, left=2, right=3, thresh=15, blur=20)

the_cowboys.set_output()
