/**
 * Revision Planner — essay-marking proxy (Cloudflare Worker).
 *
 * Why this exists: so the student never has to hold an Anthropic API key.
 * The key lives here as a server-side secret; the app calls this Worker,
 * and the Worker calls Anthropic. Free tier is plenty for personal use.
 *
 * ── One-time setup (see proxy/README.md for the click-by-click version) ──
 *  1. Create a free Cloudflare account → Workers & Pages → Create Worker.
 *  2. Paste this whole file in as the Worker code and Deploy.
 *  3. Add secrets/variables (Worker → Settings → Variables):
 *       ANTHROPIC_API_KEY  (Secret)      — your Anthropic key, funded by you.
 *       ALLOWED_ORIGIN     (Text, opt.)  — e.g. https://gougey.github.io
 *       ACCESS_TOKEN       (Secret, opt.)— a shared password to stop strangers
 *                                          using your key. If set, paste the
 *                                          same value into the app (More →
 *                                          Marking service → Proxy access token).
 *  4. Copy the Worker URL (…​.workers.dev) into the app:
 *       More → Marking service → Proxy URL.
 */
export default {
  async fetch(request, env) {
    const cors = {
      'Access-Control-Allow-Origin': env.ALLOWED_ORIGIN || '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'content-type, x-access-token',
      'Access-Control-Max-Age': '86400',
    };
    const json = (obj, status = 200) =>
      new Response(JSON.stringify(obj), { status, headers: { ...cors, 'content-type': 'application/json' } });

    if (request.method === 'OPTIONS') return new Response(null, { headers: cors });
    if (request.method !== 'POST') return json({ error: 'POST only' }, 405);

    // Optional shared-token gate so a public URL can't be used to burn your key.
    if (env.ACCESS_TOKEN && request.headers.get('x-access-token') !== env.ACCESS_TOKEN)
      return json({ error: 'unauthorized' }, 401);

    if (!env.ANTHROPIC_API_KEY) return json({ error: 'server missing ANTHROPIC_API_KEY' }, 500);

    let body;
    try { body = await request.json(); } catch { return json({ error: 'invalid JSON body' }, 400); }
    if (!Array.isArray(body.messages)) return json({ error: 'messages[] required' }, 400);

    // Only forward the fields we allow — the caller can't set arbitrary options.
    const payload = {
      model: body.model || 'claude-sonnet-5',
      max_tokens: Math.min(body.max_tokens || 1200, 4000),
      messages: body.messages,
    };

    const upstream = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        'x-api-key': env.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify(payload),
    });
    const text = await upstream.text();
    return new Response(text, { status: upstream.status, headers: { ...cors, 'content-type': 'application/json' } });
  },
};
