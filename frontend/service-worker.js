const CACHE_NAME = 'ct-cache-v2';
const ASSETS = ['/', '/index.html', '/style.css', '/app.js', '/settings.html', '/settings.js'];

self.addEventListener('install', e => {
  self.skipWaiting(); // Force the new service worker to become the active one
  e.waitUntil(
    caches
      .open(CACHE_NAME)
      .then(cache => cache.addAll(ASSETS))
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.map(key => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim()) // Take control of all clients immediately
  );
});

self.addEventListener('fetch', e => {
  e.respondWith(
    caches.match(e.request).then(resp => resp || fetch(e.request))
  );
});
