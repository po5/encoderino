from functools import partial
from vapoursynth import core
import vsutil

def prop_comp(lst, func, prop):
    return func(range(len(lst)), key=lambda i: lst[i][prop])

def stats(ref, clips, stat_func):
    scores = []
    for clip in clips:
        diff = stat_func(clip, ref)
        scores.append(diff.get_frame(0).props)
    return scores

def select(n, f, ref, stat_func, prop, comp_func, debug=False):
    clips = list(map(vsutil.frame2clip, f))
    scores = stats(ref, clips, stat_func)
    best = prop_comp(scores, comp_func, prop)
    out = f[best]
    if debug:
        out = vsutil.frame2clip(f[best]).text.Text("\n".join([f"Prop: {prop}", *[f"{i}: {s[prop]}" for i, s in enumerate(scores)], f"Best: {best}"])).get_frame(0)
    return out


def bestframeselect(clips, ref, stat_func, prop, comp_func, debug=False):
    """
    clips: list of clips
    ref: reference clip, e.g. core.average.Mean(clips) / core.median.Median(clips)
    stat_func: function that adds frame properties, e.g. core.std.PlaneStats / mvsfunc.PlaneCompare / core.butteraugli.butteraugli
    prop: property added by stat_func to compare, e.g. PlaneStatsDiff / PlaneMAE / PlaneRMSE / PlanePSNR / PlaneCov / PlaneCorr / _Diff
    comp_func: function to decide which clip to pick, e.g. min, max
    debug: display values of prop for each clip, and which clip was picked
    """
    return core.std.ModifyFrame(clip=clips[0], clips=clips, selector=partial(select, ref=ref, stat_func=stat_func, prop=prop, comp_func=comp_func, debug=debug))

# Usage:
# ref = core.average.Median([av1, vp9, h264])
# out = bestframeselect(clips=[av1, vp9, h264], ref=ref, stat_func=mvsfunc.PlaneCompare, prop="PlaneCov", comp_func=min, debug=True)
