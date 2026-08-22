import { createHash } from 'node:crypto';
import { access, readFile, readdir, stat } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';

const siteRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const repoRoot = path.resolve(siteRoot, '..');
const hasDist = process.argv.includes('--dist');
const readJson = async (relative) => JSON.parse(await readFile(path.join(siteRoot, relative), 'utf8'));
const exists = async (target) => access(target).then(() => true).catch(() => false);
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const fail = (message) => { throw new Error(message); };

const episodes = await readJson('src/generated/episodes.json');
const documents = await readJson('src/generated/documents.json');
const storyboards = await readJson('src/generated/storyboards.json');
const assets = await readJson('content/ASSET_PUBLICATION_MANIFEST.json');
const publication = await readJson('content/PUBLICATION_MANIFEST.json');
const summary = await readJson('src/generated/build-summary.json');
const imageMetadata = await readJson('src/generated/image-metadata.json');
const graphicPrototypes = await readJson('src/generated/graphic-prototypes.json');
const graphicCharacters = await readJson('src/generated/graphic-characters.json');

if (episodes.length !== 30) fail(`episode count ${episodes.length}`);
if (episodes.reduce((n, episode) => n + episode.scene_count, 0) !== 150) fail('scene count is not 150');
if (new Set(episodes.map((episode) => episode.number)).size !== 30) fail('duplicate episode route');
if (episodes.some((episode) => episode.scenes.length !== episode.scene_count)) fail('episode scene body incomplete');
if (episodes.some((episode) => episode.scenes.some((scene) => !scene.heading || !scene.blocks.some((block) => block.type === 'action') || !scene.blocks.some((block) => block.type === 'dialogue')))) fail('script rendering structure incomplete');
if (documents.length !== publication.documents.length || documents.length < 12) fail('curated document coverage failed');
if (new Set(documents.map((doc) => doc.slug)).size !== documents.length) fail('duplicate document route');
if (storyboards.length !== 30 || storyboards.reduce((n, episode) => n + episode.pages.length, 0) !== 173) fail('storyboard coverage failed');
if (assets.assets.some((asset) => asset.status !== 'APPROVED')) fail('non-approved media published');
const rejected = new Set(assets.rejected_hero_frame_ids);
if (assets.assets.some((asset) => [...rejected].some((id) => asset.source_path.includes(id)))) fail('rejected P4 target promoted');
if (assets.assets.filter((asset) => asset.type === 'video').length !== 32) fail('video allowlist coverage failed');
if (Object.keys(imageMetadata).length !== assets.assets.filter((asset) => asset.type === 'image').length) fail('image metadata coverage failed');
if (Object.values(imageMetadata).some((item) => !item.width || !item.height || !item.responsive_w720 || !item.responsive_w1600)) fail('image dimensions or derivatives incomplete');
if (graphicPrototypes.length !== 3 || graphicPrototypes.reduce((count,item)=>count+item.scenes.length,0) !== 15) fail('graphic prototype coverage failed');
if (graphicCharacters.characters.length < 16) fail('graphic character recognition coverage failed');

for (const asset of assets.assets) {
  const source = path.join(repoRoot, asset.source_path);
  const bytes = await readFile(source);
  if (bytes.length !== asset.bytes || sha(bytes) !== asset.sha256) fail(`asset identity mismatch ${asset.source_path}`);
}

const publicText = `${JSON.stringify(documents)}\n${JSON.stringify(episodes)}\n${JSON.stringify(graphicPrototypes)}\n${JSON.stringify(graphicCharacters)}`;
for (const pattern of [/\/home\/conanxin\//i, /C:\\Users\\/i, /\\\\wsl\$/i, /OPENAI_API_KEY/i]) {
  if (pattern.test(publicText)) fail(`forbidden public text ${pattern}`);
}

const immutablePaths = [
  'scripts/odyssey_m1_v2','editorial/odyssey_m1_v2','production/odyssey_m1_v2','preproduction/odyssey_m1_p3',
  'visual-development/odyssey_m1_p4','storyboards/odyssey_m1_p4','design/odyssey_m1_p4','previs/odyssey_m1_p4',
  'art-department/odyssey_m1_p5','animatic/odyssey_m1_p5','vfx-previs/odyssey_m1_p5','production-tests/odyssey_m1_p5',
  'pitch/odyssey_m1_p5','runtime_capability_prototype'
];
const diff = execFileSync('git', ['diff','--name-only','478fd10f5b115c70f7b4b8ce5146ae2b6c6d37e5','--',...immutablePaths], { cwd:repoRoot, encoding:'utf8' }).trim();
if (diff) fail(`immutable source modified:\n${diff}`);

const routeFiles = ['index.html','episodes/index.html','episodes/01/index.html','episodes/30/index.html','graphic/index.html','episodes/01/graphic/index.html','episodes/19/graphic/index.html','episodes/27/graphic/index.html','characters/index.html','visual/index.html','storyboards/index.html','storyboards/27/index.html','watch/index.html','production/index.html','project/index.html','search/index.html'];
if (hasDist) {
  for (const relative of routeFiles) if (!(await exists(path.join(siteRoot,'dist',relative)))) fail(`missing route ${relative}`);
  if (!(await exists(path.join(siteRoot,'dist','_pagefind','pagefind.js')))) fail('Pagefind index missing');
  if (!(await exists(path.join(siteRoot,'dist','search-data.json')))) fail('deterministic CJK search index missing');
  if (!(await exists(path.join(siteRoot,'dist','sitemap-index.xml')))) fail('sitemap missing');
  const selected = [1,10,19,25,27,29,30];
  for (const number of selected) {
    const episode = episodes[number - 1];
    const html = await readFile(path.join(siteRoot,'dist','episodes',String(number).padStart(2,'0'),'index.html'),'utf8');
    const readable = html.replaceAll('&#39;', "'").replaceAll('&quot;', '"').replaceAll('&amp;', '&').replaceAll('&lt;', '<').replaceAll('&gt;', '>');
    const probes = [episode.title, episode.scenes[0].heading, episode.scenes[0].blocks.find((block) => block.type === 'action')?.text, episode.scenes.at(-1).blocks.findLast((block) => block.type === 'dialogue')?.text].filter(Boolean);
    if (probes.some((probe) => !readable.includes(probe))) fail(`script reader probe failed EP${number}`);
  }
  for (const prototype of graphicPrototypes) {
    const html = await readFile(path.join(siteRoot,'dist','episodes',String(prototype.number).padStart(2,'0'),'graphic','index.html'),'utf8');
    const readable = html.replaceAll('&#39;', "'").replaceAll('&quot;', '"').replaceAll('&amp;', '&').replaceAll('&lt;', '<').replaceAll('&gt;', '>');
    const probes = [prototype.title,prototype.core_conflict,prototype.scenes[0].heading,prototype.scenes.at(-1).essential_dialogue.at(-1).text,prototype.end_hook];
    if (probes.some((probe)=>!readable.includes(probe))) fail(`graphic reader probe failed ${prototype.episode}`);
  }
  const htmlFiles = [];
  async function walk(dir) { for (const name of await readdir(dir)) { const target=path.join(dir,name); const info=await stat(target); if(info.isDirectory()) await walk(target); else if(name.endsWith('.html')) htmlFiles.push(target); } }
  await walk(path.join(siteRoot,'dist'));
  for (const file of htmlFiles) {
    const html = await readFile(file,'utf8');
    if (/\/home\/conanxin\/|C:\\Users\\|\\\\wsl\$/i.test(html)) fail(`absolute path leaked ${path.relative(siteRoot,file)}`);
    if (/href="\/(?!classic-to-drama-engine\/)|src="\/(?!classic-to-drama-engine\/)/.test(html)) fail(`root-relative deployment break ${path.relative(siteRoot,file)}`);
    if (!/<html[^>]+lang="zh-CN"/.test(html) || !/<main id="main">/.test(html) || !/class="skip-link"/.test(html)) fail(`semantic shell missing ${path.relative(siteRoot,file)}`);
    const ids = [...html.matchAll(/\sid="([^"]+)"/g)].map((match)=>match[1]);
    if (new Set(ids).size !== ids.length) fail(`duplicate HTML id ${path.relative(siteRoot,file)}`);
    const internal = [...html.matchAll(/(?:href|src)="(\/classic-to-drama-engine\/[^"#?]*)/g)].map((match)=>match[1]);
    for (const url of internal) {
      const relative = url.slice('/classic-to-drama-engine/'.length);
      const target = path.join(siteRoot,'dist',relative);
      const candidate = path.extname(target) ? target : path.join(target,'index.html');
      if (!(await exists(candidate))) fail(`broken internal reference ${url} in ${path.relative(siteRoot,file)}`);
    }
  }
  for (const asset of assets.assets.filter((item)=>item.type==='image')) {
    const extension=path.extname(asset.published_path);
    for (const width of [720,1600]) {
      const variant=asset.published_path.slice(0,-extension.length)+`-w${width}.webp`;
      if (!(await exists(path.join(siteRoot,'dist',variant)))) fail(`responsive image missing ${variant}`);
    }
  }
}

console.log(JSON.stringify({
  status:'PASS_PUBLICATION_VERIFY', dist_verified:hasDist, episodes:episodes.length, scenes:summary.scenes,
  documents:documents.length, images:assets.assets.filter((asset)=>asset.type==='image').length,
  videos:assets.assets.filter((asset)=>asset.type==='video').length, storyboard_pages:storyboards.reduce((n,x)=>n+x.pages.length,0),
  forbidden_internal_publication:0, immutable_modifications:0
}));
