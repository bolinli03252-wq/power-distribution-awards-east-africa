"""Build the public datasets in data/ from the raw keyword extracts in raw_private/ (not published).

    python build.py

Rules (documented in README.md):
- Kenya: rows flagged during manual review and contracts whose title is a service (consultancy, security, cleaning,
  fumigation, SCADA, insurance, training, fire protection, catering, civil or building works, transport, air conditioning)
  are dropped; exact duplicates (same supplier, title, amount and date) are dropped.
- Tanzania: only Tanzania rows; awards whose title or description is a service (consultancy, supervision, security,
  cleaning, software, building or civil works, insurance, training, audit) are dropped; exact duplicate rows dropped.
- Personal and contact data are never published: postal addresses, telephone numbers, e-mail addresses and
  contact-person names are removed. Only organisation names, titles, dates and amounts remain.
- USD values are approximate: KES at 129 per USD, TZS at 2,550 per USD.
"""
import csv, json, re
from pathlib import Path

ROOT = Path(__file__).parent
RAW, OUT = ROOT / "raw_private", ROOT / "data"
OUT.mkdir(exist_ok=True)
num = lambda v: float(re.sub(r"[^\d.]", "", v or "") or 0)
SERVICE_KE = re.compile(r"consult|security|guard|clean|fumigat|scada|insurance|training|audit|fire protection|fire suppression|catering|"
                        r"civil works|building works|transportation services|provision of .{0,60}services|air.?condition|repair and maintenance of", re.I)
SERVICE = re.compile(r"consult|supervision|security|guard|clean|software|scada|building|civil works|construction of (office|staff)|"
                     r"insurance|training|audit|design and supervision", re.I)

# Kenya (PPIP contract awards)
rows, seen = [], set()
for x in csv.DictReader(open(RAW / "kenya_awards_power.csv", encoding="utf-8-sig")):
    if x["excluded"].strip() or SERVICE_KE.search(x["title"]):
        continue
    k = (x["supplier"].strip().upper(), x["title"].strip().upper(), x["kes"], x["date"][:10])
    if k in seen:
        continue
    seen.add(k)
    kes = num(x["kes"])
    rows.append({"award_date": x["date"][:10], "buyer": x["buyer"].strip(), "supplier": x["supplier"].strip(),
                 "tender_title": " ".join(x["title"].split()), "amount_kes": round(kes), "amount_usd_approx": round(kes / 129)})
rows.sort(key=lambda r: (r["award_date"], r["buyer"]))
ke = OUT / "kenya_power_distribution_awards.csv"
with open(ke, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
ke_rows = rows

# Tanzania (OCDS publication 152)
rows, seen = [], set()
for x in csv.DictReader(open(RAW / "ocds_power_title.csv", encoding="utf-8-sig")):
    if x["country"] != "tanzania" or SERVICE.search(x["title"] + " " + x["description"]):
        continue
    k = (x["ocid"], x["supplier"].strip().upper(), x["amount"], x["date"][:10], x["description"][:120])
    if k in seen:
        continue
    seen.add(k)
    amt = num(x["amount"])
    usd = amt / 2550 if x["currency"].upper() in ("TZS", "") else num(x["usd"])
    rows.append({"award_date": x["date"][:10], "buyer": x["buyer"].strip(), "supplier": x["supplier"].strip(),
                 "tender_title": " ".join((x["title"] or "").split()), "description": " ".join(x["description"].split())[:400],
                 "amount": round(amt), "currency": x["currency"] or "TZS", "amount_usd_approx": round(usd), "ocid": x["ocid"]})
rows.sort(key=lambda r: (r["award_date"], r["buyer"]))
tz = OUT / "tanzania_power_distribution_awards.csv"
with open(tz, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
tz_rows = rows

def summary(rs, buyer_key):
    tot = sum(r["amount_usd_approx"] for r in rs)
    by = {}
    for r in rs:
        by[r["buyer"]] = by.get(r["buyer"], 0) + r["amount_usd_approx"]
    top = sorted(by.items(), key=lambda kv: -kv[1])[:5]
    return {"records": len(rs), "usd_total_approx": tot, "first": rs[0]["award_date"], "last": rs[-1]["award_date"],
            "top_buyers_usd": [[b, v] for b, v in top]}

s = {"kenya": summary(ke_rows, "buyer"), "tanzania": summary(tz_rows, "buyer")}
(OUT / "summary.json").write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")
# guard: nothing personal leaks
for p in (ke, tz):
    t = p.read_text(encoding="utf-8")
    assert not re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", t), f"e-mail address in {p.name}"
print(json.dumps(s, indent=1))
