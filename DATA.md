# Data sources and terms

This repository keeps the third-party data for the [El Salto conditions app](https://github.com/bucho2398/elsalto-app)
apart from the app's MIT-licensed code. The code in `tools/` is MIT (see `tools/LICENSE`); the data
files are **not**, and each keeps its source's terms:

| file | what | from | terms | redistribution permission |
|---|---|---|---|---|
| `walls.json` | zones, walls, routes: names, grades, stars, pitches, positions, aspect, tags, yes/no wall features | [theCrag](https://www.thecrag.com/en/climbing/mexico/el-salto) contributors; maintained by hand since 2026-10-12 | [CC BY-NC-SA 3.0](https://creativecommons.org/licenses/by-nc-sa/3.0/) ([theCrag copyright notes](https://www.thecrag.com/en/article/mixedcopyright)) | ⚠️ **Not confirmed.** theCrag asks to be asked before its material is reused, and no permission is on record. |
| `terrain.json` | elevation, slope, facing, horizon, catchment, sky view per wall | computed by `tools/terrain.py` from [AWS Terrain Tiles](https://registry.opendata.aws/terrain-tiles/) (SRTM) | SRTM: public domain; [Terrain Tiles attribution](https://github.com/tilezen/joerd/blob/master/docs/attribution.md) | ✅ yes |

The same table is published in `index.json` (`sources`, with `"flag": true` on content without
confirmed permission), so the app can show it.

## ⚠️ Flagged: `walls.json`

- No descriptions, topos, photos or comments are copied: only facts (names, grades, positions) and
  short tags. Route names are community facts in theCrag's own words; the rest is theCrag-derived.
- Use it non-commercially, credit theCrag, and share changes under the same terms.
- To clear the flag: get theCrag's written permission and note it here and in `tools/site.py`
  (`SOURCES`), or replace theCrag-derived entries with your own observations.
- Walls and routes you add yourself from your own knowledge are yours. Leave their `url` out, or
  point it at their theCrag page if there is one.

No scraper or scheduled job collects any of this: theCrag is never contacted.
