import argparse, os, sys
from . import core, render


def main(argv=None):
    ap = argparse.ArgumentParser(prog="fossil", description="Turn a git repository's history into a step-by-step course that rebuilds the project.")
    ap.add_argument("repo", help="path to a git repository")
    ap.add_argument("--out", default="course.html", help="HTML output file (default course.html)")
    ap.add_argument("--md", metavar="FILE", help="also write Markdown")
    ap.add_argument("--max-steps", type=int, default=30)
    ap.add_argument("--with-patches", action="store_true", help="include full patch lines (incl. deleted lines) in the HTML. Off by default: history can hold old secrets. Review before sharing.")
    ap.add_argument("--rev", default="HEAD", help="history up to this revision")
    o = ap.parse_args(argv)
    import subprocess
    try: text = core.git_log(o.repo, o.rev)
    except FileNotFoundError: sys.exit("fossil: git is not installed or not on your PATH.")
    except subprocess.CalledProcessError as e:
        why = (e.stderr or "").strip().splitlines()
        why = why[0] if why else f"git exited with {e.returncode}"
        sys.exit(f"fossil: could not read git history of '{o.repo}': {why}. Check that the folder is a git repository with at least one commit and that '{o.rev}' exists.")
    try: shallow = subprocess.run(["git", "-C", o.repo, "rev-parse", "--is-shallow-repository"], capture_output=True, text=True).stdout.strip() == "true"
    except OSError: shallow = False
    if shallow: print("fossil: warning: this is a shallow clone. Its oldest commit contains the whole project, so step 1 will be huge. Run `git fetch --unshallow` first for a real course.", file=sys.stderr)
    c = core.course(text, o.max_steps)
    if not c["steps"]: sys.exit("no commits found")
    title = os.path.basename(os.path.abspath(o.repo))
    try: open(o.out, "w", encoding="utf-8").write(render.render_html(c, title, patches=o.with_patches))
    except OSError as e: sys.exit(f"fossil: cannot write {o.out}: {e.strerror or e}")
    print(f"wrote {o.out}: {c['commits']} commits -> {len(c['steps'])} steps")
    if o.md: open(o.md, "w", encoding="utf-8").write(render.render_md(c, title)); print(f"wrote {o.md}")


if __name__ == "__main__":
    main()
