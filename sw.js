/* 介入病例库 · 手机建档 —— Service Worker
 *
 * ⚠ 这个文件是 scripts/build_mobile_pwa.py 生成的，不要手改。
 *   CACHE 里的版本号是 index.html 内容哈希的前 10 位，
 *   所以只要内容变了，版本号必然变 —— 不需要人记住任何事。
 *
 * 策略：
 *   HTML  → 网络优先（拿不到再用缓存）：上传新版后下次打开就是新的，断网也能用
 *   静态  → 缓存优先
 *
 * 历史教训：v1 曾经是纯 cache-first，结果只要 sw.js 字节没变，
 * 手机上就永远读旧 index.html，更新后完全看不到变化。
 */
const CACHE = "ir-pwa-5406b2e1e6";
const ASSETS = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./icons/icon-180.png",
  "./icons/icon-192.png",
  "./icons/icon-512.png",
  "./icons/icon-maskable-512.png"
];

self.addEventListener("install", (e) => {
  e.waitUntil(
    caches.open(CACHE)
      .then((c) => c.addAll(ASSETS))
      .then(() => self.skipWaiting())
      .catch(() => self.skipWaiting())   /* 有个别文件缺失也不拦着装 */
  );
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((ks) => Promise.all(
        ks.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET") return;

  const isDoc = req.mode === "navigate" ||
    (req.headers.get("accept") || "").indexOf("text/html") !== -1;

  if (isDoc) {
    /* 网络优先。必须 cache:"no-store"，否则会拿到浏览器 HTTP 缓存里的旧 HTML */
    e.respondWith(
      fetch(req, { cache: "no-store" })
        .then((res) => {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(req, copy)).catch(() => {});
          return res;
        })
        .catch(() => caches.match(req)
          .then((hit) => hit || caches.match("./index.html")))
    );
    return;
  }

  e.respondWith(
    caches.match(req).then((hit) => {
      if (hit) return hit;
      return fetch(req)
        .then((res) => {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(req, copy)).catch(() => {});
          return res;
        })
        .catch(() => caches.match("./index.html"));
    })
  );
});
