import subprocess, os
from fossil import core, render, cli


def git(d, *a, env=None):
    e = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t", **(env or {}))
    return subprocess.run(["git", "-C", str(d), *a], capture_output=True, text=True, check=True, env=e).stdout


def make_repo(tmp_path):
    d = tmp_path / "r"; d.mkdir(); git(d, "init", "-q", "-b", "main")
    (d / "app.py").write_text("def hello():\n    return 1\n"); git(d, "add", "-A"); git(d, "commit", "-qm", "Start: hello function")
    (d / "app.py").write_text("def hello():\n    return 1\n\nclass Greeter:\n    pass\n"); git(d, "commit", "-qam", "Add Greeter class")
    (d / "t.js").write_text("export function add(a, b) { return a + b }\n"); git(d, "add", "-A"); git(d, "commit", "-qm", "<script>alert(1)</script> JS add")
    (d / "app.py").unlink(); git(d, "add", "-A"); git(d, "commit", "-qm", "Remove app.py")
    return d


def test_parse_and_steps(tmp_path):
    d = make_repo(tmp_path); c = core.course(core.git_log(str(d)), tiny=0)
    assert c["commits"] == 4 and len(c["steps"]) == 4
    s = c["steps"]
    assert s[0]["title"] == "Start: hello function" and ("function", "hello", "app.py") in s[0]["things"]
    assert ("class", "Greeter", "app.py") in s[1]["things"] and ("function", "add", "t.js") in s[2]["things"]
    assert s[3]["files"][0]["status"] == "deleted"


def test_counts_match_git_numstat(tmp_path):
    d = make_repo(tmp_path); commits = core.parse(core.git_log(str(d)))
    for c in commits:
        ns = git(d, "show", "--numstat", "--format=", c["hash"]).split("\n")
        add = sum(int(l.split("\t")[0]) for l in ns if l.strip()); dele = sum(int(l.split("\t")[1]) for l in ns if l.strip())
        assert (sum(f["add"] for f in c["files"]), sum(f["dele"] for f in c["files"])) == (add, dele)


def test_html_escapes_commit_messages(tmp_path):
    d = make_repo(tmp_path); h = render.render_html(core.course(core.git_log(str(d)), tiny=0), "r")
    assert "alert(1)" in h and "<script>alert(1)" not in h and "&lt;script&gt;alert(1)&lt;/script&gt;" in h


def test_tiny_commits_merge_and_cap(tmp_path):
    d = tmp_path / "m"; d.mkdir(); git(d, "init", "-q", "-b", "main")
    for i in range(12):
        (d / "f.txt").write_text("\n".join(str(j) for j in range(i + 1)) + "\n"); git(d, "add", "-A"); git(d, "commit", "-qm", f"c{i}")
    c = core.course(core.git_log(str(d)), max_steps=3)
    assert c["commits"] == 12 and len(c["steps"]) <= 3


def test_cli(tmp_path):
    d = make_repo(tmp_path); out = tmp_path / "c.html"; cli.main([str(d), "--out", str(out), "--md", str(tmp_path / "c.md")])
    assert out.exists() and "Start: hello function" in (tmp_path / "c.md").read_text()


def test_merged_status_added_then_deleted(tmp_path):
    d = make_repo(tmp_path); c = core.course(core.git_log(str(d)))
    assert len(c["steps"]) == 1 and [f["status"] for f in c["steps"][0]["files"] if f["path"] == "app.py"] == ["added, later deleted"]


def test_export_default_omits_patches_and_secret(tmp_path):
    d = tmp_path / "s"; d.mkdir(); git(d, "init", "-q", "-b", "main")
    (d / "cfg.py").write_text("API_KEY = 'FAKE-RETIRED-KEY-0000-INVENTED'\nx = 1\n"); git(d, "add", "-A"); git(d, "commit", "-qm", "Add config")
    (d / "cfg.py").write_text("x = 1\n"); git(d, "commit", "-qam", "Remove key from config")
    c = core.course(core.git_log(str(d)), tiny=0)
    safe = render.render_html(c, "s")
    assert "FAKE-RETIRED-KEY" not in safe and "cfg.py" in safe and "file-list export" in safe
    full = render.render_html(c, "s", patches=True)
    assert "FAKE-RETIRED-KEY" in full and "contains full patch lines" in full
    out = tmp_path / "o.html"; cli.main([str(d), "--out", str(out)])
    assert "FAKE-RETIRED-KEY" not in out.read_text(encoding="utf-8")
    cli.main([str(d), "--out", str(out), "--with-patches"])
    assert "FAKE-RETIRED-KEY" in out.read_text(encoding="utf-8")


def test_bad_repo_gives_clean_error(tmp_path):
    import subprocess, sys
    for args in ([str(tmp_path)], [str(tmp_path / "nope")]):
        r = subprocess.run([sys.executable, "-m", "fossil.cli", *args], capture_output=True, text=True)
        assert r.returncode != 0 and "Traceback" not in r.stderr and "fossil:" in r.stderr
