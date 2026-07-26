// Minimal service worker — lets the Revision Planner install as a PWA and
// work offline. Caches the shell on first load. Adapted from the game's sw.js.

const CACHE = 'revision-planner-v1';
const CORE = [
    './',
    './index.html',
    './manifest.json',
    './assets/icon-192.png',
    './assets/icon-512.png',
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE).then((cache) => cache.addAll(CORE)).catch(() => {})
    );
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keys) =>
            Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
        )
    );
    self.clients.claim();
});

self.addEventListener('fetch', (event) => {
    const req = event.request;
    // Never cache the LLM marking API — always go to network.
    if (req.url.includes('api.anthropic.com')) return;
    // Network-first for HTML so updates land on next load; cache-first otherwise.
    if (req.mode === 'navigate') {
        event.respondWith(fetch(req).catch(() => caches.match('./index.html')));
        return;
    }
    event.respondWith(
        caches.match(req).then((cached) => cached || fetch(req).then((resp) => {
            const copy = resp.clone();
            caches.open(CACHE).then((c) => c.put(req, copy)).catch(() => {});
            return resp;
        }).catch(() => cached))
    );
});
