# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Andikaraeng008/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Andikaraeng008/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

The World Today — Tuesday 24 November 2026, in one image. A dense broadsheet
front page with exactly 50 verified stories (15 numbered main blocks + 35
briefs), a UTC timeline strip, a markets ticker, a key-metrics strip, a
"Where It Happened" map and a Date Check box — built per the
muse-ai-pro-broadsheet-studio skill: small visuals, high story density,
phone-readable type.

Run it:

```sh
python3 main.py
```

It writes the 1024x1024 front page to `/output/entry.png` (or `out/entry.png`
when `/output` does not exist). The program uses Pillow when available and
falls back to copying the bundled `entry.png` with the standard library
alone, so both runs produce byte-identical output.

Entered on make.fun — https://make.fun/bounty/news-image-20261124?ref=fkrw3nqq
