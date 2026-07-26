# Essay-marking proxy — setup (≈3 minutes, free)

This lets your son use the essay-marking feature **without ever entering an API key**.
The Anthropic key lives as a secret on your Cloudflare account; the app talks to the
proxy, the proxy talks to Anthropic.

You need: a free **Cloudflare** account and an **Anthropic API key**
(console.anthropic.com → API keys — this is what funds the marking; a few pennies per essay).

## Steps

1. **Create the Worker**
   - Sign in at <https://dash.cloudflare.com> → **Workers & Pages** → **Create** → **Create Worker**.
   - Give it a name (e.g. `revision-marker`) → **Deploy** (the default hello-world is fine for now).
   - Click **Edit code**, delete what's there, and paste the entire contents of
     [`anthropic-worker.js`](./anthropic-worker.js). Click **Deploy**.

2. **Add your secrets** (Worker → **Settings** → **Variables and Secrets**)
   - `ANTHROPIC_API_KEY` — type **Secret** — paste your Anthropic key. **Save/Deploy.**
   - *(Recommended)* `ACCESS_TOKEN` — type **Secret** — invent a password (any random string).
     This stops strangers who find the URL from spending your credit.
   - *(Optional)* `ALLOWED_ORIGIN` — type **Text** — `https://gougey.github.io`
     (locks the proxy to your app's website).

3. **Copy the Worker URL** — it looks like `https://revision-marker.<your-subdomain>.workers.dev`.

4. **Point the app at it** — in the Revision Planner: **More → Marking service**
   - **Proxy URL**: paste the Worker URL.
   - **Proxy access token**: paste the same `ACCESS_TOKEN` you set (if you set one).
   - Leave the personal API-key box empty — the proxy is used whenever a Proxy URL is set.

That's it. Test it from **Essays** — paste any answer and mark it. If something's off,
open the Worker's **Logs** tab in Cloudflare to see the error.

## Notes
- **Cost/limits:** Cloudflare's free tier covers ~100k requests/day — far more than needed.
  Anthropic charges per essay marked (typically a few pennies); set a spend limit in the
  Anthropic console if you like.
- **Security:** with `ACCESS_TOKEN` set, only someone who knows the token can use your key.
  The token is a low-risk shared password, not your Anthropic key.
- The app still supports a personal on-device key as a fallback if you'd rather not run a proxy.
