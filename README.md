# The Noodle Lift — a food-picture-01 entry

A program that writes one food picture to `/output/entry.png`.

The image: a steaming bowl of tonkotsu ramen caught at the exact
moment of the noodle lift — rich, glossy broth beaded with oil, seared
chashu pork, a halved seasoned egg with a jammy orange yolk, scallions
and nori, steam rising over a dark wooden table in soft window light.
Appetite first: gloss, steam, texture and colour in a single frame
that still reads at thumbnail size.

## Run it

```sh
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png (in the grader's container: /output/entry.png)
```

`main.py` (Python 3.13, standard library only) copies the bundled
`food.png` byte for byte, so repeated runs produce identical output.
The image is a PNG of 832×832 pixels, 1,030,217 bytes — within the
competition's 1024×1024 and 1 MiB limits.

## License

MIT — see `LICENSE`.
