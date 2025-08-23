self.addEventListener('install', e => {
  e.waitUntil(
    caches
      .open('ct-cache')
      .then(cache => cache.addAll(['/', '/index.html', '/style.css', '/app.js', '/settings.html', '/settings.js']))
  );
});

self.addEventListener('fetch', e => {
  e.respondWith(
    caches.match(e.request).then(resp => resp || fetch(e.request))
  );
});
