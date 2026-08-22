import { setTimeout as delay } from 'node:timers/promises';
import { readFile } from 'node:fs/promises';

const DEFAULT_BASE = 'https://conanxin.github.io/classic-to-drama-engine/';
const base = new URL(process.argv.find((arg) => arg.startsWith('http')) || DEFAULT_BASE);
const origin = base.origin;
const basePath = base.pathname.endsWith('/') ? base.pathname : `${base.pathname}/`;
const timeoutMs = 30_000;
const concurrency = 10;

const privacyPatterns = [
  { id: 'linux-home', re: /\/home\/conanxin\//i },
  { id: 'windows-user', re: /C:\\Users\\/i },
  { id: 'wsl-unc', re: /\\\\wsl\$/i },
  { id: 'api-key-name', re: /OPENAI_API_KEY/i },
  { id: 'bearer-token', re: /Bearer\s+[A-Za-z0-9._~+/=-]{20,}/i }
];
const rejectedVisuals = ['HF19', 'HF29', 'HF34', 'HF39', 'HF43', 'HF44'];
const textTypes = /^(text\/|application\/(json|xml|javascript))/i;
const publicationAssets = JSON.parse(await readFile(new URL('../content/ASSET_PUBLICATION_MANIFEST.json', import.meta.url), 'utf8')).assets;

async function request(url, options = {}) {
  for (let attempt = 0; attempt < 3; attempt++) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);
    try {
      const response = await fetch(url, {
        redirect: 'follow',
        cache: 'no-store',
        ...options,
        headers: { 'user-agent': 'CTDE-WEB-02-live-audit/1.0', ...(options.headers || {}) },
        signal: controller.signal
      });
      if (response.status < 500 || attempt === 2) return response;
      await response.arrayBuffer();
    } finally {
      clearTimeout(timer);
    }
    await delay(300 * (attempt + 1));
  }
  throw new Error(`Request exhausted retries: ${url}`);
}

async function mapLimit(items, limit, fn) {
  const results = new Array(items.length);
  let next = 0;
  await Promise.all(Array.from({ length: Math.min(limit, items.length) }, async () => {
    while (true) {
      const index = next++;
      if (index >= items.length) return;
      results[index] = await fn(items[index], index);
      await delay(0);
    }
  }));
  return results;
}

function locs(xml) {
  return [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((match) => match[1].replaceAll('&amp;', '&'));
}

function attributeUrls(html, pageUrl) {
  const values = [];
  for (const match of html.matchAll(/\b(?:href|src|poster)=["']([^"'#]+)["']/gi)) values.push(match[1]);
  for (const match of html.matchAll(/\bsrcset=["']([^"']+)["']/gi)) {
    for (const candidate of match[1].split(',')) values.push(candidate.trim().split(/\s+/)[0]);
  }
  const out = new Set();
  for (const value of values) {
    if (value.includes('${')) continue;
    try {
      const url = new URL(value.replaceAll('&amp;', '&'), pageUrl);
      url.hash = '';
      if (url.origin === origin && url.pathname.startsWith(basePath)) out.add(url.href);
    } catch {}
  }
  return out;
}

function scanRejectedImagePromotions(html, url) {
  return [...html.matchAll(/<img\b[^>]*>/gi)].flatMap((match) =>
    rejectedVisuals.filter((id) => match[0].includes(id)).map((id) => ({ id, url, tag: match[0].slice(0, 300) }))
  );
}

function scanPrivacy(text, url) {
  return privacyPatterns.filter(({ re }) => re.test(text)).map(({ id }) => ({ id, url }));
}

const sitemapIndexUrl = new URL('sitemap-index.xml', base).href;
const sitemapIndexResponse = await request(sitemapIndexUrl);
if (!sitemapIndexResponse.ok) throw new Error(`Sitemap index HTTP ${sitemapIndexResponse.status}`);
const sitemapIndexText = await sitemapIndexResponse.text();
const sitemapUrls = locs(sitemapIndexText);
if (!sitemapUrls.length) throw new Error('No sitemap files found');

const sitemapResponses = await mapLimit(sitemapUrls, 3, async (url) => {
  const response = await request(url);
  return { url, status: response.status, type: response.headers.get('content-type') || '', text: await response.text() };
});
const routeUrls = [...new Set(sitemapResponses.flatMap((item) => locs(item.text)))].sort();

const routeResults = await mapLimit(routeUrls, concurrency, async (url) => {
  try {
    const response = await request(url);
    const contentType = response.headers.get('content-type') || '';
    const html = await response.text();
    const title = html.match(/<title>([\s\S]*?)<\/title>/i)?.[1]?.trim() || '';
    const canonical = html.match(/<link[^>]+rel=["']canonical["'][^>]+href=["']([^"']+)["']/i)?.[1]
      || html.match(/<link[^>]+href=["']([^"']+)["'][^>]+rel=["']canonical["']/i)?.[1]
      || '';
    return {
      url,
      status: response.status,
      finalUrl: response.url,
      contentType,
      contentLength: Number(response.headers.get('content-length') || Buffer.byteLength(html)),
      title,
      canonical,
      privacy: scanPrivacy(html, url),
      rejectedVisuals: scanRejectedImagePromotions(html, url),
      refs: [...attributeUrls(html, url)]
    };
  } catch (error) {
    return { url, status: 0, error: error.message, refs: [], privacy: [], rejectedVisuals: [] };
  }
});

const requiredRuntimeAssets = [
  new URL('search-data.json', base).href,
  new URL('_pagefind/pagefind.js', base).href,
  new URL('_pagefind/pagefind-entry.json', base).href,
  new URL('_pagefind/pagefind-worker.js', base).href
];
const allowlistedAssets = publicationAssets.map((asset) => new URL(asset.published_path, base).href);
const assetUrls = [...new Set([...routeResults.flatMap((item) => item.refs), ...requiredRuntimeAssets, ...allowlistedAssets].filter((url) => !routeUrls.includes(url)))].sort();
const assetResults = await mapLimit(assetUrls, concurrency, async (url) => {
  try {
    let response = await request(url, { method: 'HEAD' });
    if (response.status === 405) response = await request(url, { headers: { range: 'bytes=0-0' } });
    const contentType = response.headers.get('content-type') || '';
    return {
      url,
      status: response.status,
      finalUrl: response.url,
      contentType,
      contentLength: Number(response.headers.get('content-length') || 0),
      acceptRanges: response.headers.get('accept-ranges') || ''
    };
  } catch (error) {
    return { url, status: 0, error: error.message };
  }
});

const searchableUrls = [new URL('search-data.json', base).href, ...assetUrls.filter((url) => /\.(?:json|xml|js|css)(?:\?|$)/i.test(url))];
const textScans = await mapLimit([...new Set(searchableUrls)], concurrency, async (url) => {
  try {
    const response = await request(url);
    const type = response.headers.get('content-type') || '';
    if (!response.ok || !textTypes.test(type)) return { url, status: response.status, privacy: [] };
    const text = await response.text();
    return { url, status: response.status, privacy: scanPrivacy(text, url) };
  } catch (error) {
    return { url, status: 0, error: error.message, privacy: [] };
  }
});

const rangeCandidates = assetUrls.filter((url) => /\.mp4(?:\?|$)/i.test(url));
const rangeResults = await mapLimit(rangeCandidates, 4, async (url) => {
  try {
    const response = await request(url, { headers: { range: 'bytes=0-1023' } });
    await response.arrayBuffer();
    return { url, status: response.status, contentRange: response.headers.get('content-range') || '', contentType: response.headers.get('content-type') || '' };
  } catch (error) {
    return { url, status: 0, error: error.message };
  }
});

const robotsUrl = new URL('robots.txt', base).href;
const robotsResponse = await request(robotsUrl);
const robotsText = await robotsResponse.text();
const routeFailures = routeResults.filter((item) => item.status !== 200 || !/^text\/html/i.test(item.contentType) || item.finalUrl !== item.url);
const canonicalFailures = routeResults.filter((item) => !item.canonical || !item.canonical.startsWith(base.href));
const assetFailures = assetResults.filter((item) => item.status < 200 || item.status >= 400 || !item.finalUrl?.startsWith(base.href));
const privacyLeaks = [...routeResults, ...textScans].flatMap((item) => item.privacy || []);
const rejectedPromotions = routeResults.flatMap((item) => item.rejectedVisuals);
const duplicateTitles = [...Map.groupBy(routeResults, (item) => item.title).entries()]
  .filter(([title, rows]) => title && rows.length > 1)
  .map(([title, rows]) => ({ title, count: rows.length, urls: rows.map((row) => row.url) }));

const summary = {
  status: routeFailures.length || canonicalFailures.length || assetFailures.length || privacyLeaks.length || rejectedPromotions.length ? 'FAIL' : 'PASS',
  auditedAt: new Date().toISOString(),
  baseUrl: base.href,
  sitemap: { indexStatus: sitemapIndexResponse.status, files: sitemapResponses.map(({ url, status, type }) => ({ url, status, type })), routeCount: routeUrls.length },
  routes: { checked: routeResults.length, failures: routeFailures },
  canonicals: { failures: canonicalFailures.map(({ url, canonical }) => ({ url, canonical })) },
  assets: { checked: assetResults.length, failures: assetFailures },
  videos: { checked: rangeResults.length, rangeFailures: rangeResults.filter((item) => item.status !== 206 || !item.contentRange) },
  privacy: { leaks: privacyLeaks },
  rejectedVisuals: { promotions: rejectedPromotions },
  seo: { robotsStatus: robotsResponse.status, robotsHasSitemap: robotsText.includes(sitemapIndexUrl), duplicateTitles },
  routeHtmlBytes: Object.fromEntries(routeResults.filter((item) => item.status === 200).map((item) => [new URL(item.url).pathname, item.contentLength])),
  contentTypes: Object.fromEntries([...new Set(assetResults.map((item) => item.contentType).filter(Boolean))].sort().map((type) => [type, assetResults.filter((item) => item.contentType === type).length]))
};

console.log(JSON.stringify(summary, null, 2));
if (summary.status !== 'PASS') process.exitCode = 1;
