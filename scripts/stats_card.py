"""Pixel-art stats card built from GitHub's contribution data (private work included).

Public stats services only see public repos. GitHub's contribution calendar counts private
contributions too (as long as "Private contributions" is on in profile settings), so this
card reads that instead.

Run:  GH_TOKEN=... python scripts/stats_card.py OUTPUT.svg
"""
import datetime as dt
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(__file__))
from make_pixels import CYAN, GREEN, NIGHT, ORANGE, PURPLE, WHITE, YELLOW, svg, text_path, text_width  # noqa: E402

USER = os.environ.get("PROFILE_USER", "Apurvsheldiya25")
TOKEN = os.environ["GH_TOKEN"]


def gql(query, **variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "User-Agent": "profile-stats-card"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        out = json.load(r)
    if "errors" in out:
        raise SystemExit(out["errors"])
    return out["data"]


YEAR = """query($u:String!,$from:DateTime,$to:DateTime){user(login:$u){contributionsCollection(from:$from,to:$to){
  totalCommitContributions restrictedContributionsCount totalPullRequestContributions totalIssueContributions
  totalPullRequestReviewContributions totalRepositoriesWithContributedCommits contributionCalendar{totalContributions}}}}"""


def collect():
    created = dt.datetime.fromisoformat(gql("query($u:String!){user(login:$u){createdAt}}", u=USER)["user"]["createdAt"].replace("Z", "+00:00"))
    last = gql(YEAR, u=USER)["user"]["contributionsCollection"]
    total, start = 0, created
    now = dt.datetime.now(dt.timezone.utc)
    while start < now:
        end = min(start + dt.timedelta(days=365), now)
        c = gql(YEAR, u=USER, **{"from": start.isoformat(), "to": end.isoformat()})["user"]["contributionsCollection"]
        total += c["contributionCalendar"]["totalContributions"]
        start = end
    return {
        "year": last["contributionCalendar"]["totalContributions"],
        # private commits a viewer can't see are reported as "restricted"; count them as commits
        "commits": last["totalCommitContributions"] + last["restrictedContributionsCount"],
        "prs": last["totalPullRequestContributions"],
        "issues": last["totalIssueContributions"],
        "reviews": last["totalPullRequestReviewContributions"],
        "repos": last["totalRepositoriesWithContributedCommits"],
        "alltime": total,
        "since": created.year,
    }


def card(d):
    W, H = 1200, 300
    p = [f'<rect width="{W}" height="{H}" fill="{NIGHT}"/>',
         f'<rect x="6" y="6" width="{W - 12}" height="{H - 12}" fill="none" stroke="{PURPLE}" stroke-width="6"/>',
         f'<path d="{text_path("HIGH SCORES", 40, 34, 5)}" fill="{ORANGE}"/>',
         f'<path class="blink" d="{text_path("1UP", W - 40 - text_width("1UP", 5), 34, 5)}" fill="{GREEN}"/>']
    # big number: contributions this year
    big = f"{d['year']:,}"
    alltime = "{:,} ALL-TIME SINCE {}".format(d["alltime"], d["since"])
    p.append(f'<path d="{text_path(big, 40, 100, 9)}" fill="{YELLOW}"/>')
    p.append(f'<path d="{text_path("CONTRIBUTIONS - LAST 12 MONTHS", 40, 175, 3)}" fill="{WHITE}" opacity=".8"/>')
    p.append(f'<path d="{text_path(alltime, 40, 205, 3)}" fill="{CYAN}"/>')
    rows = [("COMMITS", d["commits"], ORANGE), ("PULL REQUESTS", d["prs"], CYAN), ("CODE REVIEWS", d["reviews"], PURPLE),
            ("ISSUES", d["issues"], GREEN), ("REPOS", d["repos"], YELLOW)]
    for i, (k, v, col) in enumerate(rows):
        y = 100 + i * 34
        p.append(f'<rect class="pop" style="animation-delay:{i * 0.15:.2f}s" x="660" y="{y - 4}" width="12" height="29" fill="{col}"/>')
        p.append(f'<path d="{text_path(k, 690, y + 2, 3)}" fill="{WHITE}"/>')
        val = f"{v:,}"
        p.append(f'<path d="{text_path(val, W - 40 - text_width(val, 3), y + 2, 3)}" fill="{col}"/>')
    p.append(f'<path d="{text_path("PRIVATE REPOS INCLUDED - UPDATED DAILY", 40, 258, 2)}" fill="#8a84b8"/>')
    style = (".blink{animation:bl 1s steps(1) infinite}@keyframes bl{50%{opacity:0}}"
             ".pop{animation:pop .3s steps(1) both}@keyframes pop{from{opacity:0}}")
    return svg(W, H, "\n".join(p), style, f"{d['year']} contributions in the last year, {d['commits']} commits, private repos included")


if __name__ == "__main__":
    data = collect()
    print(data)
    with open(sys.argv[1], "w", encoding="utf-8", newline="\n") as f:
        f.write(card(data))
