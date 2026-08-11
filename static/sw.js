var CACHE = 'korva-v2';

var CORE = [
  '/',
  '/static/manifest.json',
  '/static/icons/icon-192.png',
  '/static/icons/icon-512.png',
  '/static/icons/icon-maskable-512.png'
];

self.addEventListener('install', function (event) {
  event.waitUntil(
    caches.open(CACHE)
      .then(function (cache) { return cache.addAll(CORE); })
      .then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches.keys()
      .then(function (keys) {
        return Promise.all(
          keys.filter(function (k) { return k !== CACHE; })
            .map(function (k) { return caches.delete(k); })
        );
      })
      .then(function () { return self.clients.claim(); })
      .then(function () {
        // Al actualizar el SW, recarga las pestañas abiertas para quitar cache viejo
        return self.clients.matchAll({ type: 'window', includeUncontrolled: true })
          .then(function (clients) {
            clients.forEach(function (client) {
              try { client.navigate(client.url); } catch (e) {}
            });
          });
      })
  );
});

self.addEventListener('fetch', function (event) {
  var req = event.request;
  if (req.method !== 'GET' || req.url.indexOf(self.location.origin) !== 0) return;

  // Navegacion: red primero con timeout de 8s; si falla/tarda, sirve cache
  if (req.mode === 'navigate') {
    event.respondWith(
      Promise.race([
        fetch(req),
        new Promise(function (resolve) {
          setTimeout(function () {
            caches.match(req).then(function (m) { resolve(m || null); });
          }, 8000);
        })
      ]).then(function (res) {
        if (res && res.status === 200) {
          var copy = res.clone();
          caches.open(CACHE).then(function (c) { c.put(req, copy); }).catch(function () {});
          return res;
        }
        if (res) return res;
        return caches.match('/');
      }).catch(function () {
        return caches.match('/');
      })
    );
    return;
  }

  // Estaticos: cache-first con respaldo a red. Las API pasan directo (datos frescos).
  if (req.url.indexOf('/api/') !== -1) return;
  event.respondWith(
    caches.match(req).then(function (m) {
      if (m) return m;
      return fetch(req).then(function (res) {
        if (res && res.status === 200 && res.type === 'basic') {
          var copy = res.clone();
          caches.open(CACHE).then(function (c) { c.put(req, copy); }).catch(function () {});
        }
        return res;
      });
    })
  );
});
