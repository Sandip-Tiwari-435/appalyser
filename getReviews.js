// file: getReviews.js
const appStore = require('app-store-scraper');

const appId = process.argv[2];
const pages=Math.ceil(parseInt(process.argv[3])/50.0)

appStore.reviews({
  id: appId,
  sort: appStore.sort.HELPFUL,
  page: pages
}).then(console.log).catch(console.error);

