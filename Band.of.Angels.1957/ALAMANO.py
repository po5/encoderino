from vapoursynth import core
import awsmfunc as awf

band_of_angels = core.ffms2.Source("Band.of.Angels.1957.1080p.WEB-DL.DD1.0.H.264-SbR.mkv")
band_of_angels = core.std.Crop(band_of_angels, left=6, right=2)
band_of_angels = awf.fb(band_of_angels, right=1)

band_of_angels.set_output()
