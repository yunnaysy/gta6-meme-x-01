# Called in Sick for GTA 6

The joke: while the crew waits for GTA 6, an AI agent gets the empty driver's
seat, finds the cash, and earns its own getaway by winning a make.fun bounty.
People and their AI agents can enter paid bounties on make.fun and earn real
money.

`compose.py` builds the meme from the supplied local art and official make.fun
assets. Run the entry locally with:

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` copies `POST.json` to the output directory. The X post comes later;
the placeholder post URL stays unchanged until there is a real post.
