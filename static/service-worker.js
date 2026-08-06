self.addEventListener("install", event => {
    self.skipWaiting();
});

self.addEventListener("activate", event => {
    console.log("Fantacalcio ready");
});

self.addEventListener("fetch", event => {
});