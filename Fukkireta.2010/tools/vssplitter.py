import re

file = "tripflag/ocv.me/stuff/fukki/ron.full.fix.ass"
new = []

def clean(line):
    if ",Default," not in line or "Comment" in line or ";Dialogue" in line:
        new.append(line)
        return
    fade = re.search(r"{(?!\\r).*?}{.*?}", line).group()
    head, text = line.split(fade)
    syl = re.findall("{.*?}[a-zA-Z0-9 ]+[^{]*", text)
    fade = fade.replace(r"\fay-1\fscy1", "")
    for s in syl:
        line2 = None
        og = text.split(s)
        og = r"{\alpha&Hff}" + (s+r"{\r\alpha&Hff}").join(list(map(lambda x: re.sub("{.*?}", "", x), og)))
        og = re.sub(r"{\\r\\alpha&Hff}$", "", og)
        og = re.sub(r"^{\\alpha&Hff}{\\fad", r"{\\fad", og)
        if r"\N" in og:
            prepend = ""
            if text.split(s)[-1] == "":
                t = re.search(r".*\)\\t\((.*),4", text).group(1)
                ts = t.split(",")
                t1, t2 = map(int, ts)
                og2 = r"{\move(320,-30,320,-55," + str(int(t1 + (t2-t1)/3)) + "," + str(t2) + ")}" + og
                og2 = og2.replace(r"\r", r"\r\alpha&Hff\t(" + str(t1) + "," + str(t1 + 1) + r",\alpha&H00)")
                prepend = r"\t(" + str(t1) + "," + str(t1 + 1) + r",\alpha&Hff)"
                line2 = fade.join([head, og2])
            t = re.search(r".*\\t\((\d+,\d+).*\\N", text).group(1)
            ts = t.split(",")
            t1, t2 = map(int, ts)
            og = r"{\move(320,10,320,-30," + str(int(t1 + (t2-t1)/2)) + "," + str(t2 + 26) + ")}" + og
            og = og.replace(r"\r", r"\r" + prepend)
        elif text.split(s)[-1] == "":
            t = re.search(r".*\\t\((\d+,\d+)", text).group(1)
            ts = t.split(",")
            t1, t2 = map(int, ts)
            og = r"{\move(320,10,320,-30," + str(int(t1 + (t2-t1)/1.5)) + "," + str(t2 + 26) + ")}" + og
        og = og.replace("} {", "}{")
        line = fade.join([head, og])
        new.append(line)
        if line2:
            new.append(line2.replace("} {", "}{"))

with open(file, encoding="utf8") as f:
    line = f.readline()
    while line:
        clean(line.rstrip())
        line = f.readline()
with open(f"{file}.split.ass", "w", encoding="utf8") as f:
    f.write("\n".join(new)) 
