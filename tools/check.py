#!/usr/bin/env python3
"""Check walls.json before it's published: the app and widget only ever see data that passes.

    python3 tools/check.py [walls.json]

Prints every problem and exits 1 if there is any, so a typo in a hand edit stops the publish
instead of reaching the phones (they keep the last good data)."""
import json, re, sys

ASPECTS = {"N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"}
FEATURES = {"roof", "cave", "overhang", "vertical", "slab", "tufa", "seep"}
ID = re.compile(r"^[A-Za-z0-9_-]{1,64}$")


def check(d):
    errs = []
    err = errs.append
    if not isinstance(d, dict):
        return ["the file must be one JSON object"]
    for k in ("area", "zones", "walls"):
        if k not in d:
            err(f"missing top-level '{k}'")
    if "updated" in d and not isinstance(d["updated"], int):
        err("'updated' must be a Unix time in whole seconds, or left out (the publish uses the commit time)")
    zones = [z.get("name") for z in d.get("zones", []) if isinstance(z, dict)]
    if len(zones) != len(d.get("zones", [])) or not all(isinstance(z, str) and z for z in zones):
        err("every zone needs a 'name'")
    walls = d.get("walls", [])
    if not isinstance(walls, list) or not walls:
        return errs + ["'walls' must be a non-empty list"]
    seen, route_ids = set(), set()
    for i, w in enumerate(walls):
        where = f"wall #{i + 1} ({w.get('name', '?')})" if isinstance(w, dict) else f"wall #{i + 1}"
        if not isinstance(w, dict):
            err(f"{where}: must be an object"); continue
        wid = w.get("id")
        if not isinstance(wid, str) or not ID.match(wid):
            err(f"{where}: 'id' must be a string of letters, digits, - or _ (keep existing ids: favourites and route logs use them)")
        elif wid in seen:
            err(f"{where}: id {wid} is used twice")
        seen.add(wid)
        if not isinstance(w.get("name"), str) or not w["name"].strip():
            err(f"{where}: needs a 'name'")
        if w.get("zone") not in zones:
            err(f"{where}: zone {w.get('zone')!r} isn't in 'zones'")
        url = w.get("url")
        if url is not None and not (isinstance(url, str) and url.startswith("https://")):
            err(f"{where}: 'url' must be an https link (its theCrag page) or left out")
        a = w.get("aspect")
        if a is not None and not (isinstance(a, str) and all(p in ASPECTS for p in a.split("/"))):
            err(f"{where}: aspect {a!r} must be one of {' '.join(sorted(ASPECTS))}, two of them like \"E/SE\", or null")
        deg = w.get("deg")
        if deg is not None and not (isinstance(deg, (int, float)) and 0 <= deg < 360):
            err(f"{where}: 'deg' must be 0–359 or null")
        pos = w.get("pos")
        if pos is not None and not (isinstance(pos, list) and len(pos) == 2 and all(isinstance(x, (int, float)) for x in pos)
                                    and 24.5 < pos[0] < 26.5 and -101.5 < pos[1] < -99.0):
            err(f"{where}: 'pos' must be [latitude, longitude] near El Salto, or null")
        tags = w.get("tags", [])
        if not (isinstance(tags, list) and all(isinstance(t, str) for t in tags)):
            err(f"{where}: 'tags' must be a list of strings")
        feats = w.get("features", {})
        if not isinstance(feats, dict) or not all(k in FEATURES and isinstance(v, bool) for k, v in feats.items()):
            err(f"{where}: 'features' takes true/false for {', '.join(sorted(FEATURES))}")
        routes = w.get("routes", [])
        if not isinstance(routes, list):
            err(f"{where}: 'routes' must be a list"); continue
        for j, r in enumerate(routes):
            rw = f"{where}, route #{j + 1}"
            if not isinstance(r, dict):
                err(f"{rw}: must be an object"); continue
            rid = r.get("id")
            if not isinstance(rid, str) or not ID.match(rid):
                err(f"{rw}: 'id' must be a string of letters, digits, - or _ (the route log uses it)")
            elif rid in route_ids:
                err(f"{rw}: route id {rid} is used twice")
            route_ids.add(rid)
            if not isinstance(r.get("name"), str) or not r["name"].strip():
                err(f"{rw}: needs a 'name'")
            if not isinstance(r.get("grade", ""), str):
                err(f"{rw}: 'grade' must be text, like \"5.11a\"")
            for k in ("stars", "pitches"):
                if k in r and not (isinstance(r[k], int) and r[k] >= 0):
                    err(f"{rw}: '{k}' must be a whole number")
        if "count" in w and not (isinstance(w["count"], int) and w["count"] >= 0):
            err(f"{where}: 'count' must be a whole number (or leave it out to count the routes listed)")
    return errs


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "walls.json"
    try:
        d = json.load(open(path, encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"{path}: not valid JSON: {e}")
        sys.exit(1)
    errs = check(d)
    for e in errs:
        print(f"{path}: {e}")
    if errs:
        sys.exit(1)
    print(f"{path}: ok, {len(d['walls'])} walls, {sum(len(w.get('routes', [])) for w in d['walls'])} routes")


if __name__ == "__main__":
    main()
