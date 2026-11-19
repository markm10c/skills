import csv, html, json, os, sys
base = sys.argv[1]
rows = {}
with open(os.path.join(base, "rows.tsv")) as f:
    for i, line in enumerate(f.read().split("\n")):
        cols = line.split("\t") + [""] * 7
        rows[i + 2] = [c.replace("\\n", "\n") for c in cols[:7]]
results = []
with open(os.path.join(base, "agent-results.tsv")) as f:
    reader = csv.reader(f, delimiter="\t")
    next(reader)
    for r in reader:
        r += [""] * 5
        results.append({"row": int(r[0]), "result": r[1], "notes": r[2], "proof": r[3], "design": r[4]})
tested = [r for r in results if r["result"] in ("PASS", "FAIL")]
counts = {k: sum(1 for r in results if r["result"] == k) for k in ("PASS", "FAIL", "SKIP")}
platform = ""
platform_by_row = {}
for n in sorted(rows):
    if rows[n][0].strip().upper() in ("WEB", "APP", "ADMIN", "WEB & APP"):
        platform = rows[n][0].strip().upper()
    platform_by_row[n] = platform
e = html.escape
cards = []
for r in sorted(tested, key=lambda r: (r["result"] != "FAIL", r["row"])):
    a, b, c, d, loc, sec, case, exp = [""] + rows[r["row"]]
    proof = "proof/" + os.path.splitext(r["proof"])[0] + ".jpg" if r["proof"] else ""
    design = "design/" + os.path.splitext(os.path.basename(r["design"]))[0] + ".jpg" if r["design"] else ""
    where = " / ".join(x for x in (platform_by_row.get(r["row"], ""), loc, sec) if x)
    figs = ""
    if design:
        figs += f'<figure><figcaption>Design</figcaption><a href="{design}" target="_blank"><img loading="lazy" src="{design}" alt="Design for row {r["row"]}"></a></figure>'
    if proof:
        figs += f'<figure><figcaption>Staging</figcaption><a href="{proof}" target="_blank"><img loading="lazy" src="{proof}" alt="Staging screenshot for row {r["row"]}"></a></figure>'
    cards.append(f'''<article id="r{r["row"]}" class="case" data-result="{r["result"]}">
<header><span class="row">Row {r["row"]}</span><span class="pill {r["result"].lower()}">{r["result"]}</span><span class="where">{e(where)}</span></header>
{f'<p class="label">{e(case)}</p>' if case else ''}
{f'<p class="expected">{e(exp)}</p>' if exp else ''}
{f'<p class="notes"><b>Agent:</b> {e(r["notes"])}</p>' if r["notes"] else ''}
<div class="figs">{figs}</div>
</article>''')
template = open(sys.argv[2]).read()
out = template.replace("{{TITLE}}", sys.argv[3]).replace("{{PASS}}", str(counts["PASS"])).replace("{{FAIL}}", str(counts["FAIL"])).replace("{{SKIP}}", str(counts["SKIP"])).replace("{{TESTED}}", str(len(tested))).replace("{{CARDS}}", "\n".join(cards))
open(os.path.join(base, "site", "index.html"), "w").write(out)
sheet = []
by_row = {r["row"]: r for r in results}
for n in range(2, max(rows) + 1):
    r = by_row.get(n)
    if not r:
        sheet.append(["", "", ""])
        continue
    link = "{{URL}}#r%d" % n if r["result"] in ("PASS", "FAIL") and (r["proof"] or r["design"]) else ""
    sheet.append([r["result"], r["notes"], link])
json.dump(sheet, open(os.path.join(base, "sheet-values.json"), "w"))
print(counts, len(tested), max(rows))
