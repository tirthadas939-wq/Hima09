# Hima09

A small setup kit for running [OmniRoute](https://github.com/diegosouzapw/OmniRoute), a self-hosted AI gateway, on your own machine (including Android via Termux) and checking that it is private and working.

## What's in here

| File | Purpose |
|---|---|
| [OMNIROUTE.md](OMNIROUTE.md) | Step-by-step guide: install, start locally, set up the dashboard, connect a client |
| [check-omniroute.sh](check-omniroute.sh) | Tests the gateway: a request with your key should work, one without should return 401 |
| [.env.example](.env.example) | Template for your local settings. Copy it to `.env` |

## Quick start

```bash
# 1. Install and start (listens on this machine only, requires a key)
npm install -g omniroute
OMNIROUTE_SERVER_HOST=127.0.0.1 REQUIRE_API_KEY=true omniroute --no-open

# 2. In the dashboard (http://localhost:20128/dashboard):
#    set a management password, add one provider, create an endpoint key

# 3. Save the key locally and test
cp .env.example .env        # then put your endpoint key in OMNIROUTE_API_KEY
./check-omniroute.sh
```

Client settings: base URL `http://localhost:20128/v1`, your endpoint key as the API key.

## Safety

- `.env` is git-ignored. Never commit real keys.
- Keep the gateway on `127.0.0.1`. Do not expose it to the internet.
- Full notes are in [OMNIROUTE.md](OMNIROUTE.md#safety-notes).
