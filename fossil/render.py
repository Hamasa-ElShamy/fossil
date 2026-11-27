"""Render a course as one self-contained HTML page, or as Markdown."""
import html

CSS = """
*{box-sizing:border-box}:root{--bg:#faf7f0;--ink:#1f2328;--mut:#57606a;--line:#d8d2c4;--card:#fff;--acc:#8a4b08;--add:#e6f6e6;--del:#fdeaea;--r:3px}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 'Literata','Cairo',Georgia,serif}
.wrap{display:grid;grid-template-columns:260px 1fr;gap:0;max-width:1180px;margin:0 auto}
nav{position:sticky;top:0;align-self:start;max-height:100vh;overflow:auto;padding:20px 14px;border-inline-end:1px solid var(--line)}
nav a{display:block;padding:8px 6px;min-height:44px;color:var(--ink);text-decoration:none;font:600 .85rem system-ui,sans-serif;border-radius:var(--r)}
nav a:hover{background:#efe8d6}nav small{color:var(--mut);font-weight:400}
main{padding:20px 28px 80px;min-width:0}
h1{font:700 2rem/1.15 'Literata','Cairo',serif;margin:.2em 0}h2{font:700 1.35rem 'Literata','Cairo',serif;margin:0}
.note{background:#fff7e0;border-inline-start:5px solid #e0a82e;padding:10px 14px;margin:14px 0;font:.9rem system-ui,sans-serif}
.step{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:18px 20px;margin:20px 0}
.meta{font:.82rem system-ui,sans-serif;color:var(--mut);margin:4px 0 10px}.tag{display:inline-block;padding:1px 8px;border:1px solid var(--line);border-radius:99px;margin-inline-end:6px}
code,pre{font-family:'JetBrains Mono',ui-monospace,Menlo,Consolas,monospace}code{background:#f0ebdd;padding:1px 5px;border-radius:3px;font-size:.88em;overflow-wrap:anywhere}
ul.t{font:.9rem system-ui,sans-serif;padding-inline-start:20px}
details{margin:6px 0;border:1px solid var(--line);border-radius:var(--r)}summary{padding:10px 12px;min-height:44px;cursor:pointer;font:.85rem 'JetBrains Mono',monospace;direction:ltr;overflow-wrap:anywhere}
pre.d{margin:0;padding:0;overflow:auto;font-size:.78rem;line-height:1.45;direction:ltr;text-align:left;max-height:420px}
pre.d span{display:block;padding:0 10px;white-space:pre}.a{background:var(--add)}.r{background:var(--del)}.h{color:#6b5a99;background:#f3f0fa}
button.lang{font:600 .9rem system-ui,sans-serif;min-height:44px;padding:0 14px;border:1px solid var(--ink);background:#fff;border-radius:var(--r);cursor:pointer}
@media(max-width:820px){.wrap{grid-template-columns:1fr}nav{position:static;max-height:none;border:0;border-bottom:1px solid var(--line)}main{padding:16px}}
"""


def esc(s): return html.escape(str(s), quote=True)


def diff_html(f, cap=400):
    if f["binary"]: return "<pre class='d'><span>binary file, not shown</span></pre>"
    out = []
    for line in f["lines"][:cap]:
        c = "a" if line.startswith("+") else ("r" if line.startswith("-") else ("h" if line.startswith("@@") else ""))
        out.append(f"<span class='{c}'>{esc(line) or ' '}</span>")
    if len(f["lines"]) > cap: out.append(f"<span class='h'>… {len(f['lines']) - cap} more lines not shown</span>")
    return "<pre class='d'>" + "".join(out) + "</pre>"


def render_html(c, title="Course"):
    P = []
    P.append(f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{esc(title)}: rebuild course</title><style>{CSS}</style></head><body><div class='wrap'>")
    P.append("<nav aria-label='Steps'><button class='lang' id='lg' type='button'>عربي</button>")
    for s in c["steps"]: P.append(f"<a href='#s{s['n']}'>{s['n']}. {esc(s['title'][:48])}<br><small>{s['level']} · +{s['add']} −{s['dele']}</small></a>")
    P.append("</nav><main>")
    P.append(f"<h1>{esc(title)}</h1><p data-ar='دورة لإعادة بناء المشروع خطوة خطوة من تاريخ git: {c['commits']} commit اتحولت لـ {len(c['steps'])} خطوة.'>A course to rebuild this project step by step from its git history: {c['commits']} commits became {len(c['steps'])} steps.</p>")
    P.append("<div class='note' data-ar='العناوين جاية من رسائل الـ commit، والحاجات «الجديدة» من أنماط بسيطة على السطور المضافة. الأداة مش بتفهم الكود ومش بتشرح ليه حصل التغيير. لو الـ commit الأول ضخم، الخطوة الأولى هتبقى ضخمة.'>Titles come from commit messages and the \"new things\" from simple patterns on added lines. Nothing here understands the code or explains why a change was made. If the first commit is huge, step 1 is huge.</div>")
    for s in c["steps"]:
        P.append(f"<section class='step' id='s{s['n']}'><h2>{s['n']}. {esc(s['title'])}</h2><div class='meta'><span class='tag'>{s['level']}</span><span class='tag'>+{s['add']} −{s['dele']}</span><span class='tag'>{esc(s['date'])}</span> <code>git checkout {esc(s['last'])}</code></div>")
        if s["body"]: P.append(f"<p>{esc(s['body'][:600])}</p>")
        if s["try_first"]:
            P.append("<p><b data-ar='جرّب الأول (من غير ما تبص على الـ diff): اكتب'>Try first, before reading the diff: write</b></p><ul class='t'>" + "".join(f"<li><code>{esc(t)}</code></li>" for t in s["try_first"]) + "</ul>")
        if s["order"]:
            P.append("<p><b data-ar='ترتيب بناء مقترح (قواعد بسيطة: الأصغر الأول، الاختبارات والتوثيق في الآخر)'>Suggested build order (simple rule: smaller first, tests and docs last)</b></p><ol class='t'>" + "".join(f"<li><code>{esc(p)}</code></li>" for p in s["order"]) + "</ol>")
        for f in s["files"]:
            P.append(f"<details><summary>{esc(f['status'])}: {esc(f['path'])} (+{f['add']} −{f['dele']})</summary>{diff_html(f)}</details>")
        P.append("</section>")
    P.append("""</main></div><script>
const T=new Map();document.querySelectorAll('[data-ar]').forEach(e=>T.set(e,e.textContent));let ar=false;
document.getElementById('lg').onclick=()=>{ar=!ar;document.documentElement.lang=ar?'ar':'en';document.documentElement.dir=ar?'rtl':'ltr';document.querySelectorAll('[data-ar]').forEach(e=>e.textContent=ar?e.dataset.ar:T.get(e));document.getElementById('lg').textContent=ar?'English':'عربي'};
</script></body></html>""")
    return "".join(P)


def render_md(c, title="Course"):
    L = [f"# {title}: rebuild course", "", f"{c['commits']} commits became {len(c['steps'])} steps. Titles are commit messages; nothing here understands the code.", ""]
    for s in c["steps"]:
        L += [f"## {s['n']}. {s['title']}", f"`git checkout {s['last']}` · {s['level']} · +{s['add']} -{s['dele']} · {s['date']}", ""]
        if s["body"]: L += [s["body"][:600], ""]
        if s["try_first"]: L += ["Try first, before reading the diff, write:"] + [f"- `{t}`" for t in s["try_first"]] + [""]
        if s["order"]: L += ["Suggested build order (smaller first, tests and docs last):"] + [f"{i}. `{p}`" for i, p in enumerate(s["order"], 1)] + [""]
        L += ["Files: " + ", ".join(f"{f['status']} `{f['path']}` (+{f['add']} -{f['dele']})" for f in s["files"]), ""]
    return "\n".join(L)
