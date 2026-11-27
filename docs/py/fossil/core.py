"""Read git history and turn it into course steps. Standard library only (needs the git program for repos).

Nothing here understands the code. Titles come from commit messages, 'new things'
come from simple patterns on added lines. The output says so.
"""
import re, subprocess

SEP = "\x1e"
FMT = SEP + "%H\x1f%an\x1f%ad\x1f%s\x1f%b\x1f"
DEFS = [
    (r"^\+\s*(?:async\s+)?def\s+(\w+)\s*\(", "function"), (r"^\+\s*class\s+(\w+)", "class"),
    (r"^\+\s*(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\(", "function"),
    (r"^\+\s*(?:export\s+)?(?:const|let)\s+(\w+)\s*=\s*(?:async\s*)?(?:\([^)]*\)|\w+)\s*=>", "function"),
    (r"^\+\s*(?:public|private|protected|static|\s)*\w[\w<>\[\]]*\s+(\w+)\s*\([^;]*\)\s*\{", "method"),
    (r"^\+\s*func\s+(?:\(\w+\s+\*?\w+\)\s+)?(\w+)\s*\(", "function"),
    (r"^\+\s*(?:pub\s+)?fn\s+(\w+)", "function"),
]
CODE_EXT = (".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".rs", ".java", ".c", ".cpp", ".rb", ".php", ".sh")


def git_log(repo, rev="HEAD"):
    return subprocess.run(["git", "-C", repo, "log", "--reverse", "--no-merges", "--date=short", "--find-renames",
                           "--format=" + FMT, "-p", "--unified=3", rev], capture_output=True, text=True, encoding="utf-8", errors="replace", check=True).stdout


def parse(text):
    """Parse the output of git_log() (also what a person can paste in the browser)."""
    commits = []
    for chunk in text.split(SEP):
        if not chunk.strip(): continue
        head, _, rest = chunk.partition("\x1f")           # hash
        parts = chunk.split("\x1f", 5)
        if len(parts) < 6: continue
        h, author, date, subj, body, diff = parts
        files, cur = [], None
        for line in diff.split("\n"):
            if line.startswith("diff --git "):
                m = re.match(r"diff --git a/(.*) b/(.*)$", line)
                cur = dict(path=m.group(2) if m else line[11:], old=m.group(1) if m else "", status="modified", add=0, dele=0, lines=[], binary=False)
                files.append(cur)
            elif cur is None: continue
            elif line.startswith("new file mode"): cur["status"] = "added"
            elif line.startswith("deleted file mode"): cur["status"] = "deleted"
            elif line.startswith("rename from"): cur["status"] = "renamed"
            elif line.startswith("Binary files") or line.startswith("GIT binary patch"): cur["binary"] = True
            elif not cur["lines"] and not line.startswith("@@"): pass      # header lines before the first hunk
            else:
                cur["lines"].append(line)
                if line.startswith("+"): cur["add"] += 1
                elif line.startswith("-"): cur["dele"] += 1
        commits.append(dict(hash=h.strip(), author=author, date=date, subject=subj.strip(), body=body.strip(), files=files))
    return commits


def new_things(c):
    found = []
    for f in c["files"]:
        if not f["path"].endswith(CODE_EXT): continue
        for line in f["lines"]:
            for rx, kind in DEFS:
                m = re.match(rx, line)
                if m and m.group(1) not in ("if", "for", "while", "switch", "catch", "return"):
                    found.append((kind, m.group(1), f["path"])); break
    seen, out = set(), []
    for t in found:
        if t[1:] not in seen: seen.add(t[1:]); out.append(t)
    return out


def size(c): return sum(f["add"] + f["dele"] for f in c["files"])


def build_steps(commits, max_steps=30, tiny=12):
    """Merge neighbouring tiny commits so the course is not 200 steps long; cap the step count."""
    steps = []
    for c in commits:
        if steps and size(c) < tiny and size(steps[-1]["commits"][-1]) < tiny and len(steps[-1]["commits"]) < 6:
            steps[-1]["commits"].append(c)
        else: steps.append(dict(commits=[c]))
    while len(steps) > max_steps:   # merge the smallest neighbouring pair
        i = min(range(len(steps) - 1), key=lambda k: sum(size(x) for x in steps[k]["commits"] + steps[k + 1]["commits"]))
        steps[i]["commits"] += steps.pop(i + 1)["commits"]
    for n, s in enumerate(steps, 1):
        cs = s["commits"]; files = {}
        for c in cs:
            for f in c["files"]:
                g = files.setdefault(f["path"], dict(path=f["path"], status=f["status"], add=0, dele=0, lines=[], binary=f["binary"]))
                if g is not files[f["path"]] or True:
                    if g["status"] == "added" and f["status"] == "deleted": g["status"] = "added, later deleted"
                    elif g["status"] == "added": pass
                    elif f["status"] in ("added", "deleted", "renamed"): g["status"] = f["status"]
                g["add"] += f["add"]; g["dele"] += f["dele"]; g["lines"] += f["lines"]
        s.update(n=n, title=cs[0]["subject"] if len(cs) == 1 else f"{cs[0]['subject']} (+{len(cs) - 1} small commits)",
                 files=list(files.values()), things=[t for c in cs for t in new_things(c)],
                 first=cs[0]["hash"][:7], last=cs[-1]["hash"][:7], date=cs[-1]["date"], body="\n".join(c["body"] for c in cs if c["body"]),
                 add=sum(f["add"] for f in files.values()), dele=sum(f["dele"] for f in files.values()))
        s["level"] = "small" if s["add"] + s["dele"] < 40 else ("medium" if s["add"] + s["dele"] < 200 else "large")
        added = [f for f in s["files"] if f["status"] == "added" and not f["binary"]]
        s["order"] = [f["path"] for f in sorted(added, key=lambda f: (bool(re.search(r"(^|/)(tests?|spec)|test_|_test\.|\.test\.", f["path"])), f["path"].endswith((".md", ".txt")), f["add"]))] if len(added) > 3 else []
        s["try_first"] = [f"{k} {name} in {p}" for k, name, p in s["things"][:6]]
    return steps


def course(text, max_steps=30, tiny=12):
    commits = parse(text)
    return dict(commits=len(commits), steps=build_steps(commits, max_steps, tiny))
