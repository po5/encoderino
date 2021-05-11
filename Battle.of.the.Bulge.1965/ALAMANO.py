from vapoursynth import core
import awsmfunc as awf
from rekt import rektlvls

battle_of_the_bulge = core.ffms2.Source("Battle.of.the.Bulge.1965.BluRay.Remux.1080p.VC-1.DD.5.1-decibeL.mkv")
battle_of_the_bulge = core.std.Crop(battle_of_the_bulge, top=194, bottom=192, left=6, right=6)
battle_of_the_bulge = awf.fb(battle_of_the_bulge, right=1)
battle_of_the_bulge = rektlvls(battle_of_the_bulge, colnum=[0,1,1905,1906,1907], colval=[-14, -5, -5, -12, -15])

battle_of_the_bulge.set_output()
