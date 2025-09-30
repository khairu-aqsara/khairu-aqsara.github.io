// Service Worker for Caching and Performance
const CACHE_NAME = 'khairu-blog-v1.0.0';
const STATIC_CACHE = 'static-v1.0.0';
const RUNTIME_CACHE = 'runtime-v1.0.0';

// Resources to cache immediately
const PRECACHE_RESOURCES = [
  '/',
  '/posts/',
  '/search/',
  '/about/',
  '/index.json',
  '/manifest.json',
  // Add critical CSS and JS files
  // These will be dynamically identified during build
];

// Resources to cache at runtime
const RUNTIME_CACHE_PATTERNS = [
  /\.(?:png|jpg|jpeg|svg|webp|gif)$/,
  /\.(?:css|js)$/,
  /\.(?:html)$/
];

// Install event - precache resources
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then(cache => cache.addAll(PRECACHE_RESOURCES))
      .then(() => self.skipWaiting())
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== STATIC_CACHE && cacheName !== RUNTIME_CACHE) {
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch event - serve from cache, fall back to network
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  // Handle same-origin requests
  if (url.origin === location.origin) {
    event.respondWith(cacheFirst(request));
  }
});

// Cache-first strategy
async function cacheFirst(request) {
  const cachedResponse = await caches.match(request);
  
  if (cachedResponse) {
    return cachedResponse;
  }

  try {
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      const cache = await caches.open(RUNTIME_CACHE);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    // Return offline page for navigation requests
    if (request.mode === 'navigate') {
      return caches.match('/offline/');
    }
    throw error;
  }
}

// Background sync for analytics and non-critical requests
self.addEventListener('sync', event => {
  if (event.tag === 'background-sync') {
    event.waitUntil(doBackgroundSync());
  }
});

async function doBackgroundSync() {
  // Implement background sync logic here
  // For example, sending analytics data when online
  console.log('Background sync triggered');
}