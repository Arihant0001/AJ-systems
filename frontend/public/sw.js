const CACHE_NAME = 'aj-systems-v1';
const staticAssets = [
  '/',
  '/index.html',
  '/App.css',
  '/index.css'
];

// Cache static assets on install
self.addEventListener('install', (event) => {
  console.log('[Service Worker] Installing...');
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[Service Worker] Caching static assets');
      return cache.addAll(staticAssets).catch(err => {
        console.log('[Service Worker] Cache addAll error:', err);
        // Don't fail install if some assets aren't available yet
      });
    })
  );
  self.skipWaiting();
});

// Activate new service worker
self.addEventListener('activate', (event) => {
  console.log('[Service Worker] Activating...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('[Service Worker] Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Serve from cache, fallback to network
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip API requests (never cache)
  if (url.pathname.startsWith('/api/')) {
    return;
  }

  // Skip cross-origin requests
  if (url.origin !== location.origin) {
    return;
  }

  event.respondWith(
    caches.match(request).then((response) => {
      if (response) {
        console.log('[Service Worker] Serving from cache:', request.url);
        return response;
      }

      return fetch(request)
        .then((response) => {
          // Don't cache if not successful
          if (!response || response.status !== 200) {
            return response;
          }

          // Don't cache non-GET requests or non-basic responses
          if (request.method !== 'GET' || response.type !== 'basic') {
            return response;
          }

          // Clone and cache successful response
          const responseToCache = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(request, responseToCache);
          });

          return response;
        })
        .catch(() => {
          console.log('[Service Worker] Network failed, no cache for:', request.url);
          
          // Return offline page if trying to access HTML
          if (request.destination === 'document' || request.mode === 'navigate') {
            return new Response(
              `
              <!DOCTYPE html>
              <html>
              <head>
                <title>Offline</title>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <style>
                  body { font-family: system-ui; padding: 20px; text-align: center; }
                  h1 { color: #333; }
                  p { color: #666; }
                </style>
              </head>
              <body>
                <h1>⚠️ Offline</h1>
                <p>You're currently offline. Some features may not be available.</p>
                <p>Check your connection and refresh the page.</p>
              </body>
              </html>
              `,
              {
                status: 503,
                statusText: 'Service Unavailable',
                headers: new Headers({
                  'Content-Type': 'text/html'
                })
              }
            );
          }

          return new Response('Network error', {
            status: 503,
            statusText: 'Service Unavailable'
          });
        });
    })
  );
});
