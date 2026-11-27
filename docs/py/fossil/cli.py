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
    try: text = core.git_log(o.repo, o.rev)
    except Exception as e: sys.exit(f"could not read git history: {e}")
    c = core.course(text, o.max_steps)
    if not c["steps"]: sys.exit("no commits found")
    title = os.path.basename(os.path.abspath(o.repo))
    open(o.out, "w", encoding="utf-8").write(render.render_html(c, title, patches=o.with_patches)); print(f"wrote {o.out}: {c['commits']} commits -> {len(c['steps'])} steps")
    if o.md: open(o.md, "w", encoding="utf-8").write(render.render_md(c, title)); print(f"wrote {o.md}")


if __name__ == "__main__":
    main()
