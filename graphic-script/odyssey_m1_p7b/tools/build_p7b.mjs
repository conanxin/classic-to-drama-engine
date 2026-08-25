import { createHash } from 'node:crypto';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const outDir = path.resolve(here, '..');
const repoRoot = path.resolve(outDir, '..', '..');
const readJson = async (relative) => JSON.parse(await readFile(path.join(repoRoot, relative), 'utf8'));
const readText = async (relative) => readFile(path.join(repoRoot, relative), 'utf8');
const writeJson = async (name, value) => writeFile(path.join(outDir, name), `${JSON.stringify(value, null, 2)}\n`);
const sha256 = (value) => createHash('sha256').update(value).digest('hex');
const clean = (value) => String(value || '').replace(/\r/g, '').replace(/[\t ]+/g, ' ').trim();

await mkdir(outDir, { recursive: true });

const screenplay = await readJson('scripts/odyssey_m1_v2/SCREENPLAY_V2_MANIFEST.json');
const architecture = await readJson('adaptation/odyssey_m1_v1/episode_architecture.json');
const sceneMaster = await readJson('preproduction/odyssey_m1_p3/SCENE_MASTER_INDEX.json');
const shotList = await readJson('preproduction/odyssey_m1_p3/SHOT_LIST_MASTER.json');
const actionPrevis = await readJson('preproduction/odyssey_m1_p3/EP26_EP28_ACTION_PREVIS.json');
const storyboard = await readJson('storyboards/odyssey_m1_p4/STORYBOARD_IMAGE_MANIFEST.json');
const look = await readJson('visual-development/odyssey_m1_p4/LOOKDEV_RENDER_MANIFEST.json');
const colorScript = await readJson('visual-development/odyssey_m1_p4/COLOR_SCRIPT.json');
const animaticEdl = await readJson('animatic/odyssey_m1_p5/FULL_SERIES_ANIMATIC_EDL.json');
const recognition = await readJson('graphic-script/odyssey_m1_p7a/CHARACTER_RECOGNITION_SYSTEM.json');
const p7aPrototypes = await Promise.all(['01', '19', '27'].map((number) => readJson(`graphic-script/odyssey_m1_p7a/prototypes/EP${number}_GRAPHIC_SCRIPT_PROTOTYPE.json`)));

const cardByEpisode = new Map(architecture.episodes.map((episode) => [episode.episode_id, episode]));
const sceneById = new Map(sceneMaster.scenes.map((scene) => [scene.scene_id, scene]));
const shotsByScene = Map.groupBy(shotList.shots, (shot) => shot.scene_id);
const eventsByShot = new Map(animaticEdl.events.map((event) => [event.shot_id, event]));
const prototypeByEpisode = new Map(p7aPrototypes.map((episode) => [episode.episode, episode]));
const prototypeSceneById = new Map(p7aPrototypes.flatMap((episode) => episode.scenes).map((scene) => [scene.scene_id, scene]));
const actionBeatsByScene = Map.groupBy(actionPrevis.beats, (beat) => beat.scene_id);
const colorByEpisode = new Map(colorScript.episodes.map((episode) => [episode.episode, episode]));

const approvedHeroes = look.assets.filter((asset) => asset.status === 'APPROVED' && asset.asset_type === 'HERO_LOOKDEV_FRAME');
const heroByShot = new Map(approvedHeroes.filter((asset) => asset.shot_id).map((asset) => [asset.shot_id, asset]));
const heroesByEpisode = Map.groupBy(approvedHeroes, (asset) => asset.episode);
const frameRecords = [];
for (const board of storyboard.board_pages) {
  for (const [index, frameId] of board.frame_ids.entries()) frameRecords.push({ frame_id: frameId, shot_id: frameId.replace(/-F\d+$/, ''), index, board });
}
const frameByShot = new Map(frameRecords.map((record) => [record.shot_id, record]));

const formalMovements = [
  { id: 'ARC-01', range: [1, 4], title: '伊萨卡失序与出航', function: '忒勒马科斯激活伊萨卡，并开始收集父亲的证词。' },
  { id: 'ARC-02', range: [5, 8], title: '脱离停滞与重新获得名字', function: '奥德修斯离开被占有的停滞，在菲埃克斯人面前重新说出名字。' },
  { id: 'ARC-03', range: [9, 15], title: '漂流自述：聪明、骄傲与损失', function: '嵌套讲述检验聪明、领导、炫耀与幸存代价。' },
  { id: 'ARC-04', range: [16, 24], title: '返乡伪装、忠诚测试与判断准备', function: '受控身份回到伊萨卡，逐层检验忠诚并准备判断。' },
  { id: 'ARC-05', range: [25, 30], title: '弓、清算、识别与共同体归位', function: '弓、清算、婚床、父亲与共同体和平共同完成返乡。' }
];
for (const [index, movement] of architecture.act_movements.entries()) {
  const formal = formalMovements[index];
  if (!formal || formal.range[0] !== movement.episodes[0] || formal.range[1] !== movement.episodes[1]) throw new Error(`Formal movement mismatch at ${index + 1}`);
  formal.authority = movement.function;
}
const movementFor = (number) => formalMovements.find((movement) => number >= movement.range[0] && number <= movement.range[1]);

function parseEpisode(raw, artifact) {
  const lines = raw.replace(/\r/g, '').split('\n');
  const title = lines[0].match(/^#\s+(EP\d{2})《(.+)》$/);
  if (!title) throw new Error(`Missing title in ${artifact.path}`);
  const metadata = {};
  for (const line of lines.slice(1, 16)) {
    const match = line.match(/^-\s+([^：]+)：(.+)$/);
    if (match) metadata[match[1].trim()] = match[2].trim();
  }
  const scenes = [];
  let current = null;
  let paragraph = [];
  let awaitingDialogue = false;
  const flush = () => {
    if (!current || paragraph.length === 0) { paragraph = []; return; }
    const text = paragraph.join('\n').trim();
    if (text) current.blocks.push({ type: awaitingDialogue ? 'dialogue' : 'action', text });
    paragraph = [];
    awaitingDialogue = false;
  };
  for (const line of lines) {
    if (/^<!--/.test(line)) { flush(); continue; }
    const sceneMatch = line.match(/^##\s+场\s+(\d+)｜(.+)$/);
    if (sceneMatch) {
      flush();
      current = { number: Number(sceneMatch[1]), heading: sceneMatch[2].trim(), blocks: [] };
      scenes.push(current);
      continue;
    }
    if (!current) continue;
    if (!line.trim() || line.trim() === '---') { flush(); continue; }
    const bold = line.trim().match(/^\*\*(.+)\*\*$/);
    if (bold) {
      flush();
      const value = bold[1].trim();
      if (/淡入|淡出|切至|黑场/.test(value)) current.blocks.push({ type: 'transition', text: value });
      else { current.blocks.push({ type: 'character', text: value }); awaitingDialogue = true; }
      continue;
    }
    paragraph.push(line);
  }
  flush();
  if (scenes.length !== artifact.scene_count) throw new Error(`${artifact.episode_id} scene count mismatch`);
  return { id: artifact.episode_id, number: Number(artifact.episode_id.slice(2)), title: title[2], metadata, scenes };
}

const sourceEpisodes = [];
for (const artifact of screenplay.artifacts) {
  const raw = await readText(artifact.path);
  if (sha256(Buffer.from(raw)) !== artifact.sha256) throw new Error(`V2 source identity mismatch: ${artifact.path}`);
  sourceEpisodes.push({ ...parseEpisode(raw, artifact), artifact, raw });
}

const p7aByName = new Map();
for (const character of recognition.characters) {
  p7aByName.set(character.name, character.id);
  for (const alias of character.aliases || []) p7aByName.set(alias, character.id);
}
const canonicalAliasRules = [
  [/^奥德修斯(?:\/乞丐)?$/, 'odysseus'], [/^雅典娜(?:\/.+)?$/, 'athena'], [/^众求婚者$/, 'suitors'],
  [/^波塞冬$/, 'poseidon'], [/^欧迈俄斯$/, 'eumaeus'], [/^欧律克勒娅$/, 'eurycleia'], [/^安提诺俄斯$/, 'antinous'],
  [/^欧律马科斯$/, 'eurymachus'], [/^安菲诺摩斯$/, 'amphinomus'], [/^菲洛提俄斯$/, 'philoetius'], [/^墨兰提俄斯$/, 'melanthius'], [/^斐弥俄斯$/, 'phemius']
];
const resolveKnownId = (name) => {
  if (p7aByName.has(name)) return p7aByName.get(name);
  for (const [pattern, id] of canonicalAliasRules) if (pattern.test(name)) return id;
  return null;
};
const supportId = (name) => `support-${sha256(Buffer.from(name)).slice(0, 10)}`;
const resolveId = (name) => resolveKnownId(name) || supportId(name);

const factionColors = {
  household: '#9b8050', 'loyal-household': '#6f7754', suitors: '#9a4f3f', gods: '#758091',
  'sea-pressure': '#426877', phaeacia: '#8b7468', otherworld: '#66504f', sailors: '#657b7b', civic: '#8c7659'
};
const sets = {
  phaeacia: new Set(['劳达玛斯','厄刻涅俄斯','得摩多科斯','欧律阿罗斯','瑙西卡','菲埃克斯船长','阿尔喀诺俄斯','阿瑞忒','桨手']),
  gods: new Set(['宙斯声','赫利俄斯声','赫尔墨斯','伊诺']),
  otherworld: new Set(['卡吕普索','喀耳刻','厄尔佩诺耳','安提克勒娅','忒瑞西阿斯','阿伽门农','阿喀琉斯','波吕斐摩斯','斯库拉局部','海妖声','莱斯特律戈涅斯人','洞外独眼巨人们','求婚者亡魂','安提诺俄斯亡魂']),
  suitors: new Set(['伊洛斯','墨兰托','雷奥克里托斯','雷奥得斯']),
  household: new Set(['佩涅洛佩','忒勒马科斯','拉厄耳忒斯','多利俄斯','伊萨卡亲族','磨坊女奴']),
  loyal: new Set(['欧佩忒斯','猪场帮工']),
  sailors: new Set(['三名船员','侦察船员','伏击船员','复原船员','年长船员','船员'])
};
function classifyFaction(name) {
  const known = recognition.characters.find((character) => character.id === resolveKnownId(name));
  if (known) return known.faction;
  if (sets.phaeacia.has(name)) return 'phaeacia';
  if (sets.gods.has(name)) return 'gods';
  if (sets.otherworld.has(name)) return 'otherworld';
  if (sets.suitors.has(name) || name.includes('求婚者')) return 'suitors';
  if (sets.household.has(name)) return 'household';
  if (sets.loyal.has(name)) return 'loyal-household';
  if (sets.sailors.has(name) || name.includes('船员')) return 'sailors';
  return 'civic';
}
function shortRole(name, faction) {
  if (name.includes('/')) return name.split('/')[1] + '状态';
  if (name.endsWith('声')) return '声音／神意层';
  if (/船员|桨手/.test(name)) return '航海行动角色';
  if (/亡魂|忒瑞西阿斯|安提克勒娅|阿伽门农|阿喀琉斯/.test(name)) return '冥界证词角色';
  return { household:'伊萨卡家宅', 'loyal-household':'忠诚家宅', suitors:'求婚者阵营', gods:'神明层', 'sea-pressure':'海神压力', phaeacia:'菲埃克斯人物', otherworld:'异境角色', sailors:'船员', civic:'城邦／旅途人物' }[faction];
}

const sourceCastNames = [...new Set(sceneMaster.scenes.flatMap((scene) => scene.cast || []))].sort((a, b) => a.localeCompare(b, 'zh-CN'));
const firstSceneForName = new Map();
for (const scene of sceneMaster.scenes) for (const name of scene.cast || []) if (!firstSceneForName.has(name)) firstSceneForName.set(name, scene.scene_id);
const sourceLabelsById = Map.groupBy(sourceCastNames, resolveId);
const characters = recognition.characters.map((character) => ({ ...character, source_labels: sourceLabelsById.get(character.id) || [character.name], recognition_level: 'P7A_FROZEN_DETAIL' }));
for (const name of sourceCastNames) {
  if (resolveKnownId(name)) continue;
  const id = resolveId(name);
  if (characters.some((character) => character.id === id)) continue;
  const faction = classifyFaction(name);
  characters.push({
    id, name, aliases: [shortRole(name, faction)], faction, color: factionColors[faction],
    anchor: `先认场内职责与位置；首次出现在 ${firstSceneForName.get(name)}。`, prop: '随本场关键物与行动显示',
    shape: faction === 'suitors' ? '求婚者前景轮廓' : faction === 'otherworld' ? '异境／证词轮廓' : '按场内任务区分',
    first_appearance: `${firstSceneForName.get(name)} 首次进入 Graphic 阅读层。`, source_labels: [name], recognition_level: 'P7B_CONTEXT_ONLY'
  });
}
characters.sort((a, b) => a.id.localeCompare(b.id));

const dialoguePairs = (scene) => {
  const pairs = [];
  for (let index = 0; index < scene.blocks.length - 1; index += 1) {
    if (scene.blocks[index].type === 'character' && scene.blocks[index + 1].type === 'dialogue') pairs.push({ speaker: scene.blocks[index].text, text: scene.blocks[index + 1].text });
  }
  return pairs;
};
const actionSentences = (scene) => scene.blocks.filter((block) => block.type === 'action').flatMap((block) => clean(block.text).split(/(?<=[。！？])/u).map(clean).filter(Boolean));
const evenlySelect = (items, count) => {
  if (items.length <= count) return [...items];
  const indexes = new Set([0, items.length - 1]);
  for (let i = 1; indexes.size < count; i += 1) indexes.add(Math.round((i * (items.length - 1)) / (count - 1)));
  return [...indexes].sort((a, b) => a - b).slice(0, count).map((index) => items[index]);
};
const selectDialogue = (scene, prototypeScene) => prototypeScene?.essential_dialogue || evenlySelect(dialoguePairs(scene), Math.min(3, Math.max(2, dialoguePairs(scene).length)));
const selectNarrative = (scene, prototypeScene) => {
  if (prototypeScene?.narrative) return prototypeScene.narrative;
  const candidates = actionSentences(scene).filter((sentence) => sentence.length >= 8);
  return evenlySelect(candidates, Math.min(2, candidates.length));
};
const panelTarget = (scene) => {
  const complexity = Number(scene.complexity || 0);
  let target = complexity <= 3 ? 3 : complexity <= 4 ? 4 : complexity <= 6 ? 5 : 6;
  if (scene.fight || scene.stunt || scene.creature || ['MEDIUM', 'HIGH'].includes(scene.vfx)) target = Math.max(target, 6);
  return target;
};
function selectShots(sceneId, target) {
  const shots = shotsByScene.get(sceneId) || [];
  const chosen = evenlySelect(shots, Math.min(target, shots.length));
  const heroShots = shots.filter((shot) => heroByShot.has(shot.shot_id));
  for (const heroShot of heroShots) {
    if (chosen.some((shot) => shot.shot_id === heroShot.shot_id)) continue;
    const replaceIndex = chosen.findIndex((shot, index) => index > 0 && index < chosen.length - 1 && !heroByShot.has(shot.shot_id));
    if (replaceIndex >= 0) chosen.splice(replaceIndex, 1, heroShot);
  }
  return chosen.sort((a, b) => shots.indexOf(a) - shots.indexOf(b));
}
function boardCrop(record) {
  const columns = [20, 655, 1290];
  const rows = [86, 580];
  const column = record.index % 3;
  const row = Math.floor(record.index / 3);
  return { left: columns[column], top: rows[row] + 56, width: 600, height: 205 };
}
function panelType(shot) {
  if (shot.dramatic_purpose === 'GEOGRAPHY') return 'ESTABLISHING';
  if (shot.dramatic_purpose === 'EVIDENCE' || shot.insert) return 'INSERT_PROP';
  if (shot.dramatic_purpose === 'REVERSAL') return 'REVEAL';
  if (shot.dramatic_purpose === 'CONSEQUENCE') return shot.shot_size === 'CU' ? 'CLOSE_UP' : 'REACTION';
  if (shot.dramatic_purpose === 'HOOK') return 'CLIMAX';
  if (shot.dramatic_purpose === 'TECHNICAL_PLATE') return 'ENVIRONMENT';
  if (shot.shot_size === 'POV') return 'POV';
  if (['CU', 'MCU'].includes(shot.shot_size)) return 'CLOSE_UP';
  if (['MS2', 'MS3'].includes(shot.shot_size)) return 'TWO_SHOT';
  return shot.stunt ? 'ACTION' : 'TRANSITION';
}
const ratioFor = (type) => ({ INSERT_PROP:'1:1', CLOSE_UP:'4:3', REACTION:'4:3', TWO_SHOT:'3:2', ACTION:'16:9', REVEAL:'16:9', CLIMAX:'16:9', POV:'3:2', ESTABLISHING:'16:9', ENVIRONMENT:'16:9', TRANSITION:'3:2' }[type] || '16:9');
function visualForShot(shot) {
  const hero = heroByShot.get(shot.shot_id);
  if (hero) return {
    source_kind: 'P4_HIGH_FIDELITY', source_path: hero.output_path, public_path: `media/visual/hero/${path.basename(hero.output_path)}`,
    authority: `${hero.asset_id} APPROVED`, source_status: 'APPROVED', transform: null, visual_asset_id: hero.asset_id
  };
  const frame = frameByShot.get(shot.shot_id);
  if (frame) return {
    source_kind: 'STORYBOARD_DERIVED_PANEL', source_path: frame.board.path, public_path: `media/graphic/panels/${frame.frame_id}.webp`,
    authority: `P4 ${frame.board.classification} ${frame.frame_id}`, source_status: 'APPROVED_TECHNICAL', transform: { kind: 'extract_webp', crop: boardCrop(frame), quality: 82 }, visual_asset_id: frame.frame_id
  };
  const event = eventsByShot.get(shot.shot_id);
  if (!event) throw new Error(`Missing P5 animatic event for ${shot.shot_id}`);
  return {
    source_kind: 'ANIMATIC_DERIVED_PANEL', source_path: event.visual_path, public_path: `media/graphic/panels/${shot.shot_id}.webp`,
    authority: `P5 ANIMATIC CARD ${shot.shot_id}`, source_status: 'APPROVED_TECHNICAL', transform: { kind: 'extract_webp', crop: { left: 24, top: 42, width: 592, height: 188 }, quality: 82 }, visual_asset_id: shot.shot_id
  };
}

const allPanels = [];
const episodeRecords = [];
for (const sourceEpisode of sourceEpisodes) {
  const episodeId = sourceEpisode.id;
  const number = sourceEpisode.number;
  const card = cardByEpisode.get(episodeId);
  const prototype = prototypeByEpisode.get(episodeId);
  const movement = movementFor(number);
  const color = colorByEpisode.get(episodeId);
  const scenes = [];
  for (const sourceScene of sourceEpisode.scenes) {
    const sceneId = `${episodeId}-S${String(sourceScene.number).padStart(2, '0')}`;
    const master = sceneById.get(sceneId);
    const sceneCard = card.scene_cards.find((item) => item.scene_id === sceneId);
    const prototypeScene = prototypeSceneById.get(sceneId);
    if (!master || !sceneCard) throw new Error(`Missing scene authority for ${sceneId}`);
    const selectedDialogue = selectDialogue(sourceScene, prototypeScene);
    const narrative = selectNarrative(sourceScene, prototypeScene);
    const chosenShots = selectShots(sceneId, panelTarget(master));
    if (chosenShots.length < 3) throw new Error(`${sceneId} has insufficient P3 shots for Graphic rollout`);
    const dialogueSlots = new Map();
    for (const [index, quote] of selectedDialogue.entries()) {
      const slot = Math.min(chosenShots.length - 1, Math.round(((index + 1) * chosenShots.length) / (selectedDialogue.length + 1)) - 1);
      dialogueSlots.set(slot, quote);
    }
    const panels = chosenShots.map((shot, index) => {
      const visual = visualForShot(shot);
      const type = panelType(shot);
      const panel = {
        panel_id: `${sceneId}-PNL${String(index + 1).padStart(2, '0')}`, episode: episodeId, scene_id: sceneId, sequence: index + 1,
        panel_type: type, ratio: ratioFor(type), dramatic_purpose: shot.dramatic_purpose, shot_id: shot.shot_id,
        subject: shot.subject, visible_action: shot.blocking, caption: index === 0 ? narrative[0] || null : index === chosenShots.length - 1 ? narrative.at(-1) || null : null,
        dialogue: dialogueSlots.get(index) || null, silent: !dialogueSlots.has(index) && index > 0 && index < chosenShots.length - 1,
        alt: `${sourceScene.heading}：${shot.subject}，${shot.dramatic_purpose.toLowerCase()}叙事画面。`, continuity: shot.continuity,
        action_beat_ids: (actionBeatsByScene.get(sceneId) || []).map((beat) => beat.id), visual
      };
      allPanels.push(panel);
      return panel.panel_id;
    });
    const participants = master.cast.map((label) => ({ character_id: resolveId(label), display_name: label, identity_state: label.includes('/') ? label.split('/')[1] : null }));
    scenes.push({
      scene_id: sceneId, number: sourceScene.number, heading: sourceScene.heading, location: master.story_location, time: master.time_label,
      scene_function: sceneCard.function, cast: participants, conflict_goal: prototypeScene?.conflict_goal || sceneCard.summary,
      relation_tip: prototypeScene?.relation_tip || `本场主要关系轴：${master.cast.slice(0, 3).join('、')}；辅助层只显示此刻可公开的身份。`,
      space_tip: prototypeScene?.space_tip || `${master.story_location}；行动围绕${(master.props || []).slice(0, 2).join('、') || '人物距离'}展开。`,
      prop_tip: prototypeScene?.prop_tip || ((master.props || []).length ? `关键物：${master.props.slice(0, 3).join('、')}。` : '本场没有新增关键道具。'),
      narrative, essential_dialogue: selectedDialogue, consequence: prototypeScene?.irreversible_change || sceneCard.summary,
      panel_ids: panels, action_beat_ids: (actionBeatsByScene.get(sceneId) || []).map((beat) => beat.id), source_scene_index: sourceScene.number - 1
    });
  }
  const episodeCastIds = [...new Set(scenes.flatMap((scene) => scene.cast.map((entry) => entry.character_id)))];
  const locations = [...new Set(scenes.map((scene) => scene.location))];
  const episodeHeroes = heroesByEpisode.get(episodeId) || [];
  const coverHero = episodeHeroes.at(-1);
  const coverVisual = coverHero ? {
    path: `media/visual/hero/${path.basename(coverHero.output_path)}`, authority: `${coverHero.asset_id} APPROVED`, source_kind: 'P4_HIGH_FIDELITY',
    alt: `${episodeId}《${sourceEpisode.title}》批准的高精叙事画面。`
  } : {
    path: `media/visual/color/${episodeId}_COLOR_KEY.png`, authority: `P4 APPROVED COLOR KEY ${episodeId}`, source_kind: 'P4_COLOR_KEY',
    alt: `${episodeId}《${sourceEpisode.title}》的批准色彩脚本。`
  };
  const primaryId = resolveId(card.primary_character);
  const counterforceId = resolveId(card.counterforce_character);
  episodeRecords.push({
    artifact_class: 'ODYSSEY_P7B_GRAPHIC_EPISODE', schema_version: '2.0.0', episode: episodeId, number, title: sourceEpisode.title,
    source_path: sourceEpisode.artifact.path, source_sha256: sourceEpisode.artifact.sha256, source_books: sourceEpisode.artifact.source_books,
    runtime_seconds: sourceEpisode.artifact.estimated_runtime_seconds, story_arc_id: movement.id, story_stage: `${movement.title}｜第 ${number - movement.range[0] + 1} / ${movement.range[1] - movement.range[0] + 1} 集`,
    primary_character_id: primaryId, geography: locations, previously_on: number === 1 ? '特洛伊战争结束多年，伊萨卡的王仍未归来；他的家正被以求婚为名的人群占据。' : cardByEpisode.get(`EP${String(number - 1).padStart(2, '0')}`).ending_cliffhanger,
    core_conflict: prototype?.core_conflict || card.logline, cover_visual: coverVisual, cast: episodeCastIds,
    relationships: prototype?.relationships || [{ from: primaryId, to: counterforceId, label: '本集行动者 ↔ 主要阻力', spoiler: 'public' }],
    palette: { dominant: color.palette_hex[0], secondary: color.palette_hex[1], black: color.palette_hex[2], accent: color.palette_hex[3], skin_light: color.palette_hex[4], label: `${color.dominant_family} × ${color.secondary_family}` },
    recap_panel_ids: number === 1 ? [] : [], scenes, end_hook: prototype?.end_hook || card.ending_cliffhanger,
    previous_episode: number > 1 ? number - 1 : null, next_episode: number < 30 ? number + 1 : null, status: 'COMPLETE_P7B_GRAPHIC_EPISODE'
  });
}

for (const episode of episodeRecords) {
  if (episode.number > 1) {
    const previous = episodeRecords[episode.number - 2];
    episode.recap_panel_ids = previous.scenes.at(-1).panel_ids.slice(-2);
  }
}

const keyPropSpecs = [
  ['PROP-BOW','奥德修斯之弓',['弓']], ['PROP-AXES','十二把斧',['斧']], ['PROP-SCAR','伤疤',['伤疤']], ['PROP-BED','橄榄树婚床',['婚床','床']],
  ['PROP-SHIP','船与返乡载体',['船','木筏']], ['PROP-WEAPONS','武器与武器墙',['武器','长矛','盾','剑']], ['PROP-LOOM','织布与紫线',['织','紫线','寿衣']],
  ['PROP-DOOR','门、门闩与出口',['门','门闩','出口']], ['PROP-ARROWS','箭与箭袋',['箭']]
];
const propLedger = keyPropSpecs.map(([propId, name, needles]) => {
  const occurrences = sceneMaster.scenes.filter((scene) => (scene.props || []).some((prop) => needles.some((needle) => prop.includes(needle))));
  return { prop_id: propId, name, matching_terms: needles, first_appearance: occurrences[0]?.scene_id || null, scenes: occurrences.map((scene) => ({ scene_id: scene.scene_id, source_props: scene.props.filter((prop) => needles.some((needle) => prop.includes(needle))) })), visual_rule: '沿用 P3/P4/P5 已冻结的形态、custody 与状态变化；HTML 提示不替代画面连续性。' };
});

const queue = [];
for (const episode of episodeRecords) for (const scene of episode.scenes) {
  const panels = scene.panel_ids.map((id) => allPanels.find((panel) => panel.panel_id === id));
  if (panels.some((panel) => panel.visual.source_kind === 'P4_HIGH_FIDELITY')) continue;
  queue.push({ queue_id: `UPGRADE-${scene.scene_id}`, episode: episode.episode, scene_id: scene.scene_id, priority: scene.action_beat_ids.length ? 'HIGH' : Number(sceneById.get(scene.scene_id).complexity) >= 5 ? 'MEDIUM' : 'LOW', purpose: 'Future P8 high-fidelity replacement for one technical/animatic-derived anchor while preserving current complete Graphic reading coverage.', current_visual_status: 'COMPLETE_WITH_APPROVED_TECHNICAL_AUTHORITY', required_continuity_refs: ['P7B panel manifest', 'P4 visual bible', 'P3 scene/prop continuity', ...(scene.action_beat_ids || [])] });
}

const episodeManifest = {
  artifact_class: 'ODYSSEY_P7B_EPISODE_MANIFEST', schema_version: '2.0.0', authorization: 'USER_AUTHORIZED_WITHOUT_REAL_READER_EVIDENCE',
  real_reader_validation: 'NOT_CLAIMED', source_baseline_commit: '912cdd6715fe5ae4fe82418b30035440938a9c17',
  counts: { episodes: episodeRecords.length, scenes: episodeRecords.reduce((sum, episode) => sum + episode.scenes.length, 0), character_registry: characters.length },
  story_movements: formalMovements, episodes: episodeRecords, status: 'COMPLETE_30_EPISODE_GRAPHIC_NOVEL_SCRIPT_DATA'
};
const panelManifest = {
  artifact_class: 'ODYSSEY_P7B_PANEL_MANIFEST', schema_version: '2.0.0', source_baseline_commit: '912cdd6715fe5ae4fe82418b30035440938a9c17',
  counts: {
    panel_placements: allPanels.length, unique_visual_assets: new Set(allPanels.map((panel) => panel.visual.public_path)).size,
    high_fidelity_placements: allPanels.filter((panel) => panel.visual.source_kind === 'P4_HIGH_FIDELITY').length,
    storyboard_derived_placements: allPanels.filter((panel) => panel.visual.source_kind === 'STORYBOARD_DERIVED_PANEL').length,
    animatic_derived_placements: allPanels.filter((panel) => panel.visual.source_kind === 'ANIMATIC_DERIVED_PANEL').length,
    new_generated_assets: 0, exact_source_dialogue: allPanels.filter((panel) => panel.dialogue).length, action_previs_beats_bound: new Set(allPanels.flatMap((panel) => panel.action_beat_ids)).size
  },
  panels: allPanels, status: 'COMPLETE_P7B_PANEL_PLACEMENT_AUTHORITY'
};
const characterRegistry = { artifact_class: 'ODYSSEY_P7B_CHARACTER_REGISTRY', schema_version: '2.0.0', p7a_frozen_entries: recognition.characters.length, source_cast_labels: sourceCastNames.length, resolved_source_cast_labels: sourceCastNames.length, characters, status: 'COMPLETE_P7B_CHARACTER_ID_RESOLUTION' };
const propPayload = { artifact_class: 'ODYSSEY_P7B_PROP_VISUAL_LEDGER', schema_version: '2.0.0', props: propLedger, action_continuity: { authority: 'preproduction/odyssey_m1_p3/EP26_EP28_ACTION_PREVIS.json', beat_count: actionPrevis.beats.length, beat_ids: actionPrevis.beats.map((beat) => beat.id), door_geography: 'BOUND', arrow_state: 'BOUND', weapon_custody: 'BOUND' }, status: 'PASS_P7B_PROP_AND_ACTION_CONTINUITY_BINDING' };
const queuePayload = { artifact_class: 'ODYSSEY_P7B_NEW_PANEL_GENERATION_QUEUE', schema_version: '1.0.0', purpose: 'Optional P8 high-fidelity upgrades only; no entry is a missing P7B panel or placeholder.', graphic_completion_blocked: false, queue_count: queue.length, items: queue, status: 'NON_BLOCKING_FUTURE_RENDER_QUEUE' };

for (const [name, payload] of [
  ['P7B_CHARACTER_REGISTRY.json', characterRegistry], ['P7B_EPISODE_MANIFEST.json', episodeManifest], ['P7B_PANEL_MANIFEST.json', panelManifest],
  ['P7B_PROP_VISUAL_LEDGER.json', propPayload], ['P7B_NEW_PANEL_GENERATION_QUEUE.json', queuePayload]
]) await writeJson(name, payload);

console.log(JSON.stringify({ status: 'PASS_P7B_DATA_BUILD', episodes: episodeManifest.counts.episodes, scenes: episodeManifest.counts.scenes, panels: panelManifest.counts.panel_placements, characters: characterRegistry.characters.length, queue: queue.length }));
