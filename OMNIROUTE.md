# Connecting OmniRoute

[OmniRoute](https://github.com/diegosouzapw/OmniRoute) is a self-hosted, open-source AI gateway. You add your model
providers to it once, then point your tools (Claude Code, Codex, Cursor, OpenCode and others) at one
OpenAI-compatible endpoint.

This guide sets it up on your own machine, keeps it private, and checks that a client can reach it.

## 1. Install and start

You need Node.js (22.x, or 24 up to 26) and npm.

```bash
node --version
npm install -g omniroute
omniroute --output json doctor --no-liveness
```

Start it so it only listens on your own machine and requires a key for model traffic:

```bash
OMNIROUTE_SERVER_HOST=127.0.0.1 REQUIRE_API_KEY=true omniroute --no-open
```

Defaults:

| Item | Value |
|---|---|
| Port | `20128` |
| Dashboard | http://localhost:20128/dashboard |
| Client base URL | http://localhost:20128/v1 |

Without `OMNIROUTE_SERVER_HOST`, some versions listen on all network interfaces, so set it.
The values are also listed in `.env.example`.

## 2. Set up the dashboard

1. Open the dashboard and set a strong management password. Keep dashboard login turned on.
2. Add **one provider** using your own API key. Start with a single test provider before adding more.
3. Open **Endpoints** and create a separate **endpoint key** for each client.

Do not put real keys in this repo. `.env` is ignored by git.

## 3. Check it works

Put your endpoint key in `.env` as `OMNIROUTE_API_KEY` (or export it in your shell), then run:

```bash
./check-omniroute.sh
```

The script lists models with your key (should succeed), then without a key (should return 401).

## 4. Point a client at it

Use these settings in any OpenAI-compatible tool:

```
Base URL: http://localhost:20128/v1
API key:  your endpoint key
Model:    an explicit provider/model name for the first test, then "auto" if you want routing
```

For Claude Code and other supported CLIs, OmniRoute has helper commands. Run the dry run first, because
setup commands may write configuration files:

```bash
omniroute setup-claude --dry-run
omniroute launch        # runs Claude Code with the gateway settings, without saving them
```

Base URL formats differ between clients, so check OmniRoute's own docs for your tool.

## Safety notes

- Keep it on `127.0.0.1`. Do not expose it to the internet. One report says the `/api/acp/agents`
  route had an unfixed issue, so never put that route behind a tunnel or public address.
- Keep login and `REQUIRE_API_KEY` on.
- Do not paste real keys into shell history, screenshots, issues, or shared files.
- Check each provider's terms before routing through a gateway, and be careful with anything promising
  "free" access to paid models.

## Sources

- https://omniroute.online/de/deploy/
- https://agentpedia.codes/blog/omniroute-ai-gateway-routing-setup-guide
- https://docs.digitalocean.com/products/marketplace/catalog/omniroute/
