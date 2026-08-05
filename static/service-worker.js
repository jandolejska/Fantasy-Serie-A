self.addEventListener("install", event => {
    self.skipWaiting();
});

self.addEventListener("activate", event => {
    console.log("Fantasy Serie A ready");
});

self.addEventListener("fetch", event => {
});