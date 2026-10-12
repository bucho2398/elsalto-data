#!/usr/bin/env python3
"""Build the published site: walls.json, terrain.json and index.json, the manifest the app and the
widget read first. It gives each file's SHA-256 and size, so they only download what changed and
throw away anything that doesn't match, and says where each file comes from and on what terms.

    python3 tools/site.py <out dir>
"""
import hashlib, json, os, shutil, subprocess, sys, time

HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
FILES = ["walls.json", "terrain.json"]

# What each file is made from, and whether we know we may redistribute it. Keep in step with DATA.md.
SOURCES = [
    {
        "files": ["walls.json"],
        "what": "zones, walls and routes: names, grades, stars, pitches, positions, aspect, tags, yes/no wall features",
        "from": "theCrag contributors (https://www.thecrag.com/en/climbing/mexico/el-salto), maintained by hand since 2026-10-12",
        "license": "CC BY-NC-SA 3.0 (theCrag's terms for climber-contributed content)",
        "permission": "not confirmed: theCrag asks to be asked before its material is reused; no permission on record",
        "flag": True,
    },
    {
        "files": ["terrain.json"],
        "what": "elevation, slope, facing, horizon, catchment and sky view per wall",
        "from": "computed by tools/terrain.py from AWS Terrain Tiles (SRTM, public domain) at walls.json's positions",
        "license": "SRTM public domain; Terrain Tiles attribution: https://github.com/tilezen/joerd/blob/master/docs/attribution.md",
        "permission": "yes",
        "flag": False,
    },
]


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    files = {}
    for name in FILES:
        data = open(os.path.join(HERE, name), "rb").read()
        json.loads(data)
        with open(os.path.join(out, name), "wb") as f:
            f.write(data)
        files[name] = {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
    walls = json.load(open(os.path.join(HERE, "walls.json"), encoding="utf-8"))
    commit = subprocess.run(["git", "-C", HERE, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    index = {
        "schema": 1,
        # Increases with every publish; clients keep whichever copy has the higher version.
        "version": int(time.time()),
        # When walls.json last changed: its last commit, unless the file says otherwise.
        "updated": walls.get("updated") or int(subprocess.run(["git", "-C", HERE, "log", "-1", "--format=%ct", "--", "walls.json"],
                                                             capture_output=True, text=True).stdout.strip() or time.time()),
        "commit": commit,
        "attribution": walls.get("attribution"),
        "files": files,
        "sources": SOURCES,
    }
    with open(os.path.join(out, "index.json"), "w") as f:
        json.dump(index, f, indent=1)
    shutil.copy(os.path.join(HERE, "DATA.md"), os.path.join(out, "DATA.md"))
    print(json.dumps({k: index[k] for k in ("version", "commit", "files")}))


if __name__ == "__main__":
    main()
