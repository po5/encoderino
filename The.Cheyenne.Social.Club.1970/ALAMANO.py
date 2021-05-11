from vapoursynth import core
import awsmfunc as awf

cheyenne_social_club = core.d2v.Source("The Cheyenne Social Club (1970)/VTS_01_1.d2v")
cheyenne_social_club = core.vivtc.VFM(cheyenne_social_club, 1)
cheyenne_social_club = core.std.SelectEvery(cheyenne_social_club, cycle=5, offsets=[0, 1, 2, 4])
cheyenne_social_club = core.std.Crop(cheyenne_social_club, top=64, bottom=60)
cheyenne_social_club = awf.fb(cheyenne_social_club, top=1)
cheyenne_social_club = awf.bbmod(cheyenne_social_club, top=5, right=4, thresh=15, blur=10)

cheyenne_social_club.set_output()
