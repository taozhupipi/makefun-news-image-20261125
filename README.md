# Wednesday 25 November 2026 — world news in one image

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/taozhupipi/makefun-news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/taozhupipi/makefun-news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

An entry for the [news-image-20261125](https://make.fun/c/news-image-20261125)
competition: a program that draws one 1024×1024 image summing up the world
news of Wednesday 25 November 2026 — eight verified stories, from the US
tariff proposals and the Russian strikes on Ukraine's power grid to the
first foreign astronaut aboard China's Tiangong station.

## The eight stories

1. **Russia hits Ukraine's power grid** — overnight strikes cut power in
   five regions; five killed and gas sites set ablaze. (Reuters)
2. **New US tariffs on 14 partners** — Washington targets excess factory
   capacity; the steepest duties will hit China. (Reuters)
3. **Houthi drone hits Riyadh tower** — the kingdom's tallest tower is
   struck a second time in a week; 11 people hurt. (Reuters)
4. **Solomons pick Australia as partner** — treaty bars any foreign
   military base; Canberra pledges $740m over a decade. (PM of Australia,
   CNN, AP)
5. **First foreigner boards Tiangong** — Shenzhou-24 docks; Pakistani
   pilot Zeeshan Ali joins the station for a week. (Reuters, Nature)
6. **Cartagena hostages freed at dawn** — troops storm an Exito store at
   dawn; all captives freed, one gunman killed. (AP)
7. **Abrego Garcia lands in Spain** — after a 20-month deportation
   fight, he flies to Madrid on a commercial flight. (Reuters, CNN)
8. **IS attack kills two in Hasaka** — Islamic State gunmen kill two
   security staff and wound five in northeast Syria. (Reuters)

## How it works

`draw.py` draws the image with Pillow (standard library only besides
Pillow, which the harness provides): a dated header band and a 2×4 grid
of story cards, each with a tag pill, a headline, a one-line summary and
a small pictogram drawn from simple shapes. `main.ts` runs it and writes
`/output/entry.png`. The program uses no network and is deterministic —
two runs produce byte-identical output.

Run it locally:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see [LICENSE](LICENSE).
