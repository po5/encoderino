from vapoursynth import core
from acsuite import eztrim

gambo = core.lsmas.LWLibavSource("Tokyo Gambo 1-5/tokyo gambo 1.mp4")
gambo = core.std.SelectEvery(gambo, cycle=2, offsets=[0])

gambo2 = core.lsmas.LWLibavSource("Tokyo Gambo 1-5/tokyo gambo 2.mp4")
gambo2 = core.std.SelectEvery(gambo2, cycle=2, offsets=[0])

gambo3 = core.lsmas.LWLibavSource("Tokyo Gambo 1-5/tokyo gambo 3.mp4")
gambo3 = core.std.SelectEvery(gambo3, cycle=2, offsets=[0])

gambo4 = core.lsmas.LWLibavSource("Tokyo Gambo 1-5/tokyo gambo 4.mp4")
gambo4 = core.std.SelectEvery(gambo4, cycle=2, offsets=[0])

gambo5 = core.lsmas.LWLibavSource("Tokyo Gambo 1-5/tokyo gambo 5.mp4")
gambo5 = core.std.SelectEvery(gambo5, cycle=2, offsets=[0])

eztrim(gambo, [(None,10),(None,4506)], "tokyo gambo 1.track_2.aac")
eztrim(gambo2, [(13,4504)], "tokyo gambo 2.track_2.aac")
eztrim(gambo3, [(None,3),(None,4506)], "tokyo gambo 3.track_2.aac")
eztrim(gambo4, [(None,9),(None,4506)], "tokyo gambo 4.track_2.aac")
eztrim(gambo5, [(None,10),(None,4506)], "tokyo gambo 5.track_2.aac")
