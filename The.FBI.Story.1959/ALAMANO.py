from vapoursynth import core
import awsmfunc as awf
import havsfunc as haf

fbi_story = core.d2v.Source("THE_FBI_STORY/VTS_01_1.d2v")
fbi_story = core.vivtc.VFM(fbi_story, 1)
fbi_story = awf.ReplaceFrames(core.std.SelectEvery(fbi_story, cycle=5, offsets=[0, 1, 2, 4]), core.std.SelectEvery(fbi_story, cycle=5, offsets=[0, 1, 2, 3]), f"[0 127490]")
fbi_story = haf.Deblock_QED(fbi_story)

fbi_story.set_output()
