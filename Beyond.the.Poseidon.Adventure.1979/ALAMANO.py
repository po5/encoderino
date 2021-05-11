from vapoursynth import core
import awsmfunc as awf

beyond_the_poseidon_adventure = core.ffms2.Source("Beyond.the.Poseidon.Adventure.1979.1080p.AMZN.WEB-DL.DDP2.0.x264-ABM.mkv")
beyond_the_poseidon_adventure = core.std.Crop(beyond_the_poseidon_adventure, left=2, right=2)
beyond_the_poseidon_adventure = awf.fb(beyond_the_poseidon_adventure, left=1, right=1)
beyond_the_poseidon_adventure = awf.bbmod(beyond_the_poseidon_adventure, right=2, thresh=15, blur=20)

beyond_the_poseidon_adventure.set_output()
