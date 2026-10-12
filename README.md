# El Salto data

The walls and routes the [El Salto conditions app](https://github.com/bucho2398/elsalto-app) and
widget show. Edited by hand, published on GitHub Pages at
**https://bucho2398.github.io/elsalto-data/**. Phones pick up changes on their own, with no new APK.

Data terms: see [DATA.md](DATA.md). ⚠️ `walls.json` is theCrag-derived (CC BY-NC-SA) without
confirmed redistribution permission.

## Updating the data

1. Edit `walls.json` (on GitHub: open it, ✏️, *Commit changes*).
2. The [Publish](.github/workflows/publish.yml) workflow checks it, works out terrain for walls that
   are new or moved, and publishes. A red ❌ in *Actions* means the check found a mistake: its log
   names the wall and the problem, and the phones keep the last good data until it's fixed.
3. Phones check `index.json` when the app opens or refreshes, and every 6 hours from the widget. They
   download only the files whose checksum changed, verify them, and keep a copy for offline use.

Keep wall and route `id`s as they are: favourites, shade windows and the route log on everyone's
phone are stored under them. New walls and routes need new ids: anything unique made of letters,
digits, `-` and `_` (like `own-cueva-2`).

## `walls.json`

```jsonc
{
  "area": "El Salto",
  "pos": [25.37819, -100.29952],          // the crag, [latitude, longitude]
  "attribution": "Walls and routes: …",   // shown in the app
  "url": "https://www.thecrag.com/…",     // the area's theCrag page
  "zones": [{ "id": "…", "name": "Los Delirios" }],
  "walls": [{
    "id": "9288353292",                   // never change; new walls: any unique id
    "name": "Nebulosidad",
    "zone": "Los Delirios",               // one of the zones' names
    "url": "https://www.thecrag.com/…",   // its theCrag page (the app links it), or leave out
    "aspect": "SE",                       // N … NNW, or two like "E/SE", or null
    "deg": 135,                           // the face's direction in degrees, or null
    "pos": [25.38315, -100.19127],        // the wall's base, or null
    "tags": ["Limestone", "Dry in the rain"],
    "features": { "slab": true, "overhang": false, "roof": false, "cave": false,
                  "vertical": false, "tufa": false, "seep": false },
    "routes": [{ "id": "9367151625", "name": "Dogodrilo", "grade": "5.10d",
                 "stars": 0, "pitches": 1, "style": "sport" }],
    "count": 18                           // optional: routes on the wall if not all are listed
  }]
}
```

What the model uses: `pos` (weather point, terrain), `aspect`/`deg` (which way the face looks;
otherwise terrain), `tags` ("Dry in the rain", "Wet in rain", "Morning sun", "Afternoon sun", …) and
`features` (how much water the face holds and catches; `seep` keeps it wet after rain).

## Files

| file | made by |
|---|---|
| `walls.json` | you, by hand |
| `terrain.json` | `tools/terrain.py`, run by the workflow (don't edit) |
| `index.json` (published only) | `tools/site.py`: version, checksums, sources and terms |
| `tools/check.py` | the checks a hand edit must pass; run it yourself with `python3 tools/check.py` |
