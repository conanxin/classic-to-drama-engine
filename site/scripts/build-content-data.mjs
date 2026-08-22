import { createHash } from 'node:crypto';
import { cp, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

const siteRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const repoRoot = path.resolve(siteRoot, '..');
const outRoot = path.join(siteRoot, 'src/generated');
const mediaRoot = path.join(siteRoot, 'public/media');
const readJson = async (p) => JSON.parse(await readFile(path.join(repoRoot, p), 'utf8'));
const readText = async (p) => readFile(path.join(repoRoot, p), 'utf8');
const sha = (buffer) => createHash('sha256').update(buffer).digest('hex');
const writeJson = (name, value) => writeFile(path.join(outRoot, name), `${JSON.stringify(value, null, 2)}\n`);

await rm(outRoot, { recursive: true, force: true });
await rm(mediaRoot, { recursive: true, force: true });
await mkdir(outRoot, { recursive: true });
await mkdir(mediaRoot, { recursive: true });

const publication = await readJson('site/content/PUBLICATION_MANIFEST.json');
const assetManifest = await readJson('site/content/ASSET_PUBLICATION_MANIFEST.json');
const screenplayManifest = await readJson('scripts/odyssey_m1_v2/SCREENPLAY_V2_MANIFEST.json');
const sceneIndex = await readJson('preproduction/odyssey_m1_p3/SCENE_MASTER_INDEX.json');
const animatic = await readJson('animatic/odyssey_m1_p5/ANIMATIC_MASTER_MANIFEST.json');
const storyboard = await readJson('storyboards/odyssey_m1_p4/STORYBOARD_IMAGE_MANIFEST.json');
const look = await readJson('visual-development/odyssey_m1_p4/LOOKDEV_RENDER_MANIFEST.json');
const characterStates = await readJson('design/odyssey_m1_p4/CHARACTER_STATE_MATRIX.json');
const costumeStates = await readJson('design/odyssey_m1_p4/COSTUME_STATE_MATRIX.json');

const assetBySource = new Map(assetManifest.assets.map((x) => [x.source_path, x]));
const responsiveBySource = new Map();
const imageMetadata = {};
for (const asset of assetManifest.assets) {
  if (asset.status !== 'APPROVED') throw new Error(`Non-approved published asset: ${asset.source_path}`);
  const source = path.join(repoRoot, asset.source_path);
  const bytes = await readFile(source);
  if (bytes.length !== asset.bytes || sha(bytes) !== asset.sha256) throw new Error(`Asset identity mismatch: ${asset.source_path}`);
  const dest = path.join(siteRoot, 'public', asset.published_path);
  await mkdir(path.dirname(dest), { recursive: true });
  await cp(source, dest);
  if (asset.type === 'image') {
    const metadata = await sharp(bytes).metadata();
    const extension = path.extname(asset.published_path);
    const responsivePath = asset.published_path.slice(0, -extension.length) + '-w720.webp';
    const desktopPath = asset.published_path.slice(0, -extension.length) + '-w1600.webp';
    await sharp(bytes).resize({ width:720, withoutEnlargement:true }).webp({ quality:78, effort:4 }).toFile(path.join(siteRoot, 'public', responsivePath));
    await sharp(bytes).resize({ width:1600, withoutEnlargement:true }).webp({ quality:82, effort:4 }).toFile(path.join(siteRoot, 'public', desktopPath));
    responsiveBySource.set(asset.source_path, responsivePath);
    imageMetadata[asset.published_path] = {
      width: metadata.width,
      height: metadata.height,
      responsive_w720: responsivePath,
      responsive_w1600: desktopPath
    };
  }
}
await writeJson('image-metadata.json', imageMetadata);

function cleanInline(text) {
  return text.replace(/^\*\*(.+)\*\*$/, '$1').replace(/`([^`]+)`/g, '$1').trim();
}

function parseEpisode(raw, artifact, sceneRows, renderedRuntime) {
  const lines = raw.replace(/\r/g, '').split('\n');
  const titleMatch = lines[0].match(/^#\s+(EP\d{2})《(.+)》$/);
  if (!titleMatch) throw new Error(`Episode title missing: ${artifact.path}`);
  const metadata = {};
  for (const line of lines.slice(1, 16)) {
    const m = line.match(/^-\s+([^：]+)：(.+)$/);
    if (m) metadata[m[1].trim()] = m[2].trim();
  }
  const scenes = [];
  let current = null;
  let pendingCharacter = false;
  let paragraph = [];
  const flush = () => {
    if (!current || !paragraph.length) { paragraph = []; return; }
    const text = paragraph.join('\n').trim();
    if (!text) { paragraph = []; return; }
    current.blocks.push({ type: pendingCharacter ? 'dialogue' : 'action', text });
    pendingCharacter = false;
    paragraph = [];
  };
  for (const line of lines) {
    if (/^<!--/.test(line)) { flush(); continue; }
    const scene = line.match(/^##\s+场\s+(\d+)｜(.+)$/);
    if (scene) {
      flush();
      current = { number: Number(scene[1]), heading: scene[2].trim(), blocks: [] };
      scenes.push(current);
      pendingCharacter = false;
      continue;
    }
    if (!current) continue;
    if (!line.trim() || line.trim() === '---') { flush(); continue; }
    const bold = line.trim().match(/^\*\*(.+)\*\*$/);
    if (bold) {
      flush();
      const value = bold[1].trim();
      if (/淡入|淡出|切至|黑场/.test(value)) current.blocks.push({ type: 'transition', text: value });
      else { current.blocks.push({ type: 'character', text: value }); pendingCharacter = true; }
      continue;
    }
    paragraph.push(line);
  }
  flush();
  if (scenes.length !== artifact.scene_count) throw new Error(`${artifact.episode_id} scene parse ${scenes.length} != ${artifact.scene_count}`);
  const cast = [...new Set(sceneRows.flatMap((x) => x.cast || []))];
  const locations = [...new Set(sceneRows.map((x) => x.story_location).filter(Boolean))];
  const complexityValues = sceneRows.map((x) => Number(x.complexity ?? x.complexity_score ?? 0)).filter(Number.isFinite);
  return {
    id: artifact.episode_id,
    number: Number(artifact.episode_id.slice(2)),
    title: titleMatch[2],
    source_path: artifact.path,
    source_sha256: artifact.sha256,
    estimated_runtime_seconds: artifact.estimated_runtime_seconds,
    animatic_runtime_seconds: renderedRuntime,
    scene_count: artifact.scene_count,
    source_books: artifact.source_books,
    source_event_ids: artifact.source_event_ids,
    want: metadata['本集目标'] || '',
    irreversible_turn: metadata['不可逆转'] || '',
    production_baseline: metadata['制作基线'] || '',
    characters: cast,
    locations,
    complexity: complexityValues.length ? Math.max(...complexityValues) : null,
    scenes,
    visible_text_sha256: sha(Buffer.from(scenes.flatMap((s) => [s.heading, ...s.blocks.map((b) => b.text)]).join('\n')))
  };
}

const scenesByEpisode = Map.groupBy(sceneIndex.scenes, (x) => x.episode);
const runtimeByEpisode = new Map(animatic.episode_animatics.map((x) => [x.episode, x.rendered_runtime_seconds]));
const episodes = [];
for (const artifact of screenplayManifest.artifacts) {
  const raw = await readText(artifact.path);
  if (sha(Buffer.from(raw)) !== artifact.sha256) throw new Error(`V2 source changed: ${artifact.path}`);
  episodes.push(parseEpisode(raw, artifact, scenesByEpisode.get(artifact.episode_id) || [], runtimeByEpisode.get(artifact.episode_id)));
}
if (episodes.length !== 30 || new Set(episodes.map((x) => x.number)).size !== 30) throw new Error('Episode route coverage failure');
await writeJson('episodes.json', episodes);

function section(markdown, heading) {
  const escaped = heading.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const m = markdown.match(new RegExp(`^##\\s+${escaped}[^\\n]*\\n([\\s\\S]*?)(?=^##\\s+|(?![\\s\\S]))`, 'm'));
  return m ? m[1].trim() : '';
}
const voice = await readText('editorial/odyssey_m1_v2/CHARACTER_VOICE_BIBLE.md');
const arcs = await readText('editorial/odyssey_m1_v2/CHARACTER_ARC_AUDIT.md');
const core = [
  { slug:'odysseus', zh:'奥德修斯', en:'Odysseus', role:'返乡者／受控身份的实践者', recognition:['故事与名字','伤疤','弓与十二把斧','婚床','父亲与土地'], props:['弓','伤疤','婚床'] },
  { slug:'penelope', zh:'佩涅洛佩', en:'Penelope', role:'家庭政治的执行者／最终人类验证者', recognition:['家库与织机','公共证词','伤疤与弓','只有两人知道的婚床'], props:['织机','钥匙','婚床'] },
  { slug:'telemachus', zh:'忒勒马科斯', en:'Telemachus', role:'继承人／从说话到承担共同体责任', recognition:['父亲的故事','证词判断','共同保密','并肩作战'], props:['剑','账板','父亲酒杯'] },
  { slug:'athena', zh:'雅典娜', en:'Athena', role:'条件改变者／不替人完成选择的神', recognition:['伪装','节奏与风','显形条件','武器放下'], props:['长矛','斗篷','门槛'] }
];
for (const ch of core) {
  const states = characterStates.states.filter((x) => x.character === ch.en).map((x) => x.state_id);
  const costumes = costumeStates.costumes.filter((x) => x.character === ch.en).map((x) => x.costume_id);
  const eps = episodes.filter((e) => e.characters.some((name) => name.includes(ch.zh))).map((e) => e.number);
  const principal = look.assets.find((x) => x.asset_type === 'PRINCIPAL_CHARACTER_SHEET' && x.character === ch.en && x.status === 'APPROVED');
  ch.episodes = eps;
  ch.voice_source = section(voice, `${ch.zh} ${ch.en}`);
  ch.arc_source = section(arcs, `${ch.en}:`);
  ch.visual_states = states;
  ch.costume_states = costumes;
  ch.image = principal ? assetBySource.get(principal.output_path)?.published_path : null;
  ch.image_responsive = principal ? responsiveBySource.get(principal.output_path) : null;
}
const supportCounts = new Map();
for (const e of episodes) for (const name of e.characters) {
  if (core.some((x) => name.includes(x.zh))) continue;
  supportCounts.set(name, (supportCounts.get(name) || 0) + 1);
}
const supporting = [...supportCounts].sort((a,b) => b[1]-a[1] || a[0].localeCompare(b[0])).slice(0,24).map(([name,count]) => ({name, episode_count:count}));
await writeJson('characters.json', { core, supporting });

const worldSpecs = [
  ['ithaca','伊萨卡','家、占领、验证与共同体',['伊萨卡','厅堂','婚房','果园','田野']],
  ['sea','海','归途的条件、代价与不可控力量',['海','甲板','木筏','船']],
  ['phaeacia','菲埃克斯／斯刻里亚','款待、讲述与第一次公共自证',['菲埃克斯','斯刻里亚']],
  ['cyclops-cave','独眼巨人洞穴','名字、聪明与后果被放大的封闭空间',['独眼巨人']],
  ['circe','喀耳刻之岛','欲望、变形与重新组织船员关系',['喀耳刻']],
  ['underworld','冥界','记忆、母亲、预言与未结责任',['冥界','血沟']],
  ['eumaeus-farm','欧迈俄斯农庄','劳动、忠诚与受控身份的试验场',['农庄','猪舍','欧迈俄斯']],
  ['orchard','果园与土地','父亲、边界石与血缘之外的土地证明',['果园','田野']],
  ['strait','海峡与怪物海域','有限选择、六个损失与指挥责任',['斯库拉','海妖','海峡']]
];
const world = worldSpecs.map(([slug,name,thesis,keys]) => {
  const rows = sceneIndex.scenes.filter((s) => keys.some((k) => (s.story_location || '').includes(k)));
  return { slug,name,thesis,episode_numbers:[...new Set(rows.map((x)=>Number(x.episode.slice(2))))].sort((a,b)=>a-b),locations:[...new Set(rows.map((x)=>x.story_location))],scene_count:rows.length };
});
await writeJson('world.json', world);

const published = (source) => assetBySource.get(source)?.published_path || null;
const responsive = (source) => responsiveBySource.get(source) || null;
const boardEpisodes = Array.from({ length: 30 }, (_, i) => {
  const ep = `EP${String(i+1).padStart(2,'0')}`;
  const pages = storyboard.board_pages.filter((x) => x.scene_id.startsWith(ep)).map((x) => ({
    ...x,
    board_page_id:`${x.scene_id}-P${String(x.page).padStart(2,'0')}`,
    shot_ids:[...new Set(x.frame_ids.map((frame) => frame.replace(/-F\d+$/, '')))],
    public_path: published(x.path),
    public_responsive: responsive(x.path)
  }));
  const sheet = storyboard.episode_contact_sheets.find((x) => x.episode === ep);
  return { episode: ep, number:i+1, contact_sheet: sheet ? published(sheet.path) : null, contact_sheet_responsive:sheet ? responsive(sheet.path) : null, pages };
});
await writeJson('storyboards.json', boardEpisodes);

const visual = {
  hero: look.assets.filter((x) => x.asset_type === 'HERO_LOOKDEV_FRAME' && x.status === 'APPROVED' && published(x.output_path)).map((x) => ({ asset_id:x.asset_id,label:x.label,episode:x.episode,shot_id:x.shot_id,path:published(x.output_path),responsive:responsive(x.output_path) })),
  characters: look.assets.filter((x) => x.asset_type === 'PRINCIPAL_CHARACTER_SHEET' && x.status === 'APPROVED').map((x) => ({ asset_id:x.asset_id,character:x.character,path:published(x.output_path),responsive:responsive(x.output_path) })).filter((x)=>x.path),
  sets: look.assets.filter((x) => x.asset_type === 'STANDING_SET_ANCHOR' && x.status === 'APPROVED').map((x) => ({ asset_id:x.asset_id,label:`${x.set_id} · ${x.set_state}`,path:published(x.output_path),responsive:responsive(x.output_path) })).filter((x)=>x.path),
  color: assetManifest.assets.filter((x) => x.published_path.includes('/visual/color/')).map((x) => ({ episode:path.basename(x.source_path).slice(0,4),path:x.published_path,responsive:responsive(x.source_path) }))
};
await writeJson('visual.json', visual);

const forbiddenPatterns = [/\/home\/conanxin\//i, /C:\\Users\\/i, /\\\\wsl\$/i, /OPENAI_API_KEY/i, /authorization registry/i];
const docs = [];
for (const item of publication.documents) {
  let raw = await readText(item.source);
  raw = raw.replaceAll('/home/conanxin/workspace/classic-to-drama-engine/', '').replace(/C:\\Users\\[^\\\s]+\\/g, '');
  if (forbiddenPatterns.some((re) => re.test(raw))) throw new Error(`Forbidden public document text in ${item.source}`);
  const headings = [...raw.matchAll(/^(#{2,3})\s+(.+)$/gm)].map((m) => ({ depth:m[1].length,text:cleanInline(m[2]),id:cleanInline(m[2]).toLowerCase().replace(/[^\p{Letter}\p{Number}]+/gu,'-').replace(/(^-|-$)/g,'') }));
  const firstParagraph = raw.match(/^#\s+[^\n]+\n+(?![-#|`])([^\n]+(?:\n(?!\n|[-#|`])[^\n]+)*)/m)?.[1]?.replace(/\s+/g, ' ').trim();
  docs.push({ ...item, deck:item.deck || firstParagraph || '冻结的 Classic-to-Drama Engine 项目文档。', raw, headings, source_url:`https://github.com/conanxin/classic-to-drama-engine/blob/478fd10f5b115c70f7b4b8ce5146ae2b6c6d37e5/${item.source}` });
}
await writeJson('documents.json', docs);

const searchRecords = [
  ...episodes.map((episode) => ({
    route:`episodes/${String(episode.number).padStart(2,'0')}/`, type:'剧本', title:`${episode.id}《${episode.title}》`,
    text:[episode.title,episode.want,...episode.scenes.flatMap((scene)=>[scene.heading,...scene.blocks.map((block)=>block.text)])].join('\n')
  })),
  ...docs.map((doc)=>({route:`documents/${doc.slug}/`,type:'文档',title:doc.title,text:doc.raw})),
  ...core.map((character)=>({route:`characters/${character.slug}/`,type:'人物',title:character.zh,text:[character.en,character.role,character.voice_source,character.arc_source,...character.recognition,...character.props].join('\n')})),
  ...world.map((place)=>({route:'world/',type:'世界',title:place.name,text:[place.name,place.thesis,...place.locations].join('\n')}))
];
await writeFile(path.join(siteRoot,'public/search-data.json'),`${JSON.stringify(searchRecords)}\n`);

const timeline = [
  ['Engine foundation','Classic-to-Drama Engine establishes traceable adaptation infrastructure.'],
  ['Candidate','A synthetic-only candidate path proves the bounded workflow.'],
  ['24 Books','Source events and responsibility chains cover Books 1–24.'],
  ['Adaptation Bible','M1 world, fidelity boundaries and recognition thesis are frozen.'],
  ['Screenplay V1','Thirty structurally complete episode drafts are preserved.'],
  ['Screenplay V2','Editorial rewrite produces playable, character-specific production drafts.'],
  ['P3','Director, shot, schedule and budget package reaches preproduction readiness.'],
  ['P4','Approved look development, technical storyboards and teaser previs are frozen.'],
  ['P5','Art handoff, full-series animatics, VFX previs and pitch proof pass independently.'],
  ['Web Archive','The frozen work becomes a curated, searchable public viewer while P6 remains paused.']
].map(([milestone,summary],index)=>({index:index+1,milestone,summary}));
await writeJson('project.json', { timeline, baseline_commit:'478fd10f5b115c70f7b4b8ce5146ae2b6c6d37e5', p5_manifest_sha256:'6078af3ab505aab3958d82aea2bfa3e2a5b5e07bc163293285fe411c1a469353' });

await writeJson('media.json', {
  pitch_teaser: published('pitch/odyssey_m1_p5/PITCH_TEASER_PREVIS.mp4'),
  p4_teaser: published('previs/odyssey_m1_p4/TEASER_PREVIS.mp4'),
  animatics: animatic.episode_animatics.map((x) => ({...x, public_path:published(x.file), poster:boardEpisodes[Number(x.episode.slice(2))-1].contact_sheet,poster_responsive:boardEpisodes[Number(x.episode.slice(2))-1].contact_sheet_responsive}))
});

await writeJson('build-summary.json', {
  episodes:episodes.length,
  scenes:episodes.reduce((n,x)=>n+x.scene_count,0),
  documents:docs.length,
  public_assets:assetManifest.asset_count,
  public_images:assetManifest.assets.filter((x)=>x.type==='image').length,
  public_videos:assetManifest.assets.filter((x)=>x.type==='video').length,
  public_media_bytes:assetManifest.total_bytes,
  search_documents:searchRecords.length,
  generated_at:'DETERMINISTIC_FROM_BASELINE_478fd10'
});

console.log(JSON.stringify({status:'PASS_CONTENT_GENERATION',episodes:episodes.length,documents:docs.length,assets:assetManifest.asset_count}));
