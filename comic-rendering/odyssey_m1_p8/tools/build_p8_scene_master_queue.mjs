import { readFile, writeFile, mkdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const outDir = path.resolve(here, '..');
const repoRoot = path.resolve(outDir, '..', '..');
const readJson = async (relative) => JSON.parse(await readFile(path.join(repoRoot, relative), 'utf8'));
const writeJson = async (name, value) => writeFile(path.join(outDir, name), `${JSON.stringify(value, null, 2)}\n`);

const episodes = await readJson('graphic-script/odyssey_m1_p7b/P7B_EPISODE_MANIFEST.json');
const panels = await readJson('graphic-script/odyssey_m1_p7b/P7B_PANEL_MANIFEST.json');
const look = await readJson('visual-development/odyssey_m1_p4/LOOKDEV_RENDER_MANIFEST.json');

const panelsByScene = Map.groupBy(panels.panels, (panel) => panel.scene_id);
const approvedHeroes = look.assets.filter((asset) => asset.status === 'APPROVED' && asset.asset_type === 'HERO_LOOKDEV_FRAME');
const heroesByScene = Map.groupBy(approvedHeroes, (asset) => asset.shot_id.match(/^EP\d{2}-S\d{2}/)?.[0]);
const principalReference = {
  odysseus: 'visual-development/odyssey_m1_p4/high_fidelity/characters/P4-CHAR-ODY-IDENTITY-V02.png',
  penelope: 'visual-development/odyssey_m1_p4/high_fidelity/characters/P4-CHAR-PEN-IDENTITY-V01.png',
  telemachus: 'visual-development/odyssey_m1_p4/high_fidelity/characters/P4-CHAR-TEL-IDENTITY-V01.png',
  athena: 'visual-development/odyssey_m1_p4/high_fidelity/characters/P4-CHAR-ATH-IDENTITY-V01.png'
};
const setReference = {
  S1: 'visual-development/odyssey_m1_p4/high_fidelity/sets/P4-SET-S1-ANCHOR-V01.png',
  S2: 'visual-development/odyssey_m1_p4/high_fidelity/sets/P4-SET-S2-ANCHOR-V01.png',
  S3: 'visual-development/odyssey_m1_p4/high_fidelity/sets/P4-SET-S3-ANCHOR-V01.png',
  S4: 'visual-development/odyssey_m1_p4/high_fidelity/sets/P4-SET-S4-ANCHOR-V01.png',
  S5: 'visual-development/odyssey_m1_p4/high_fidelity/sets/P4-SET-S5-ANCHOR-V01.png'
};
const goldMaster = {
  'EP01-S02':'comic-rendering/odyssey_m1_p8/master/gold-standard/P8-EP01-S02-PNL02-V01.png',
  'EP05-S05':'comic-rendering/odyssey_m1_p8/master/gold-standard/P8-EP05-S05-PNL06-V01.png',
  'EP10-S02':'comic-rendering/odyssey_m1_p8/master/gold-standard/P8-EP10-S02-PNL04-V01.png',
  'EP10-S04':'comic-rendering/odyssey_m1_p8/master/gold-standard/P8-EP10-S04-PNL04-V01.png',
  'EP13-S03':'comic-rendering/odyssey_m1_p8/master/gold-standard/P8-EP13-S03-PNL04-V01.png',
  'EP16-S04':'comic-rendering/odyssey_m1_p8/master/gold-standard/P8-EP16-S04-PNL02-V01.png',
  'EP19-S02':'comic-rendering/odyssey_m1_p8/master/gold-standard/P8-EP19-S02-PNL04-V01.png',
  'EP19-S04':'comic-rendering/odyssey_m1_p8/master/gold-standard/P8-EP19-S04-PNL02-V01.png',
  'EP25-S01':'comic-rendering/odyssey_m1_p8/master/gold-standard/P8-EP25-S01-PNL02-V02.png',
  'EP25-S05':'comic-rendering/odyssey_m1_p8/master/gold-standard/P8-EP25-S05-PNL04-V01.png',
  'EP27-S01':'comic-rendering/odyssey_m1_p8/master/gold-standard/P8-EP27-S01-PNL03-V01.png',
  'EP28-S02':'comic-rendering/odyssey_m1_p8/master/gold-standard/P8-EP28-S02-PNL04-V01.png',
  'EP30-S04':'comic-rendering/odyssey_m1_p8/master/gold-standard/P8-EP30-S04-PNL04-V01.png',
  'EP30-S05':'comic-rendering/odyssey_m1_p8/master/gold-standard/P8-EP30-S05-PNL04-V01.png'
};
const stateByEpisode = (episode) => episode <= 4 ? 'Ithaca stagnation' : episode <= 8 ? 'journey expansion' : episode <= 15 ? 'mythic otherness' : episode <= 24 ? 'return compression and disguise tension' : episode <= 28 ? 'recognition and reckoning' : 'restoration and civic closure';
const unitFrom = (scenePanels) => scenePanels[0]?.continuity?.match(/unit=([^;]+)/)?.[1]?.trim() || null;
const selectKeyPanel = (scenePanels) => {
  const order = ['CLIMAX','REVEAL','ACTION','CLOSE_UP','TWO_SHOT','ESTABLISHING','POV','REACTION','INSERT_PROP','TRANSITION','ENVIRONMENT'];
  return [...scenePanels].sort((a,b) => order.indexOf(a.panel_type) - order.indexOf(b.panel_type))[0];
};
const compact = (value, limit=320) => String(value || '').replace(/\s+/g,' ').trim().slice(0,limit);

await mkdir(path.join(outDir, 'candidate', 'scene-masters'), { recursive: true });
const queue = [];
for (const episode of episodes.episodes) {
  for (const scene of episode.scenes) {
    const scenePanels = panelsByScene.get(scene.scene_id) || [];
    const key = selectKeyPanel(scenePanels);
    const episodeNumber = Number(episode.number);
    const unit = unitFrom(scenePanels);
    let finalSource = null;
    let status = 'P8_RENDER_REQUIRED';
    let authority = null;
    if (goldMaster[scene.scene_id]) {
      finalSource = goldMaster[scene.scene_id];
      status = 'P8_GOLD_STANDARD_MASTER';
      authority = 'PASS_P8_GOLD_STANDARD_STYLE_LOCK';
    } else if ((heroesByScene.get(scene.scene_id) || []).length) {
      const hero = heroesByScene.get(scene.scene_id)[0];
      finalSource = hero.output_path;
      status = 'EXISTING_P4_HIGH_FIDELITY_MASTER';
      authority = `${hero.asset_id} APPROVED`;
    }
    const refs = [];
    for (const member of scene.cast) if (principalReference[member.character_id] && !refs.includes(principalReference[member.character_id])) refs.push(principalReference[member.character_id]);
    if (unit && setReference[unit] && refs.length < 3) refs.push(setReference[unit]);
    const sameEpisodeHero = approvedHeroes.find((hero) => hero.episode === episode.episode);
    if (sameEpisodeHero && refs.length < 3) refs.push(sameEpisodeHero.output_path);
    refs.push(`visual-development/odyssey_m1_p4/color_keys/${episode.episode}_COLOR_KEY.png`);
    const dedupedRefs = [...new Set(refs)].slice(0,4);
    const cast = scene.cast.map((member) => `${member.display_name}${member.identity_state ? ` (${member.identity_state})` : ''}`).join(', ');
    const visibleBeats = scenePanels.map((panel) => compact(panel.visible_action || panel.caption || panel.subject, 170)).filter(Boolean).slice(0,6);
    const prompt = `Create one publication-grade high-fidelity sequential graphic-novel scene master for ODYSSEY P8 ${scene.scene_id}, single 16:9 landscape image. This is final visual art, not a storyboard or contact sheet. Scene: ${scene.heading}. Location: ${scene.location}. Characters: ${cast}. Conflict: ${compact(scene.conflict_goal)}. Spatial authority: ${compact(scene.space_tip)}. Key prop authority: ${compact(scene.prop_tip)}. Key narrative beat: ${compact(key?.visible_action || key?.caption || scene.narrative?.[0])}. Consequence: ${compact(scene.consequence)}. Supporting beats that should be legible through layered blocking, props and reaction: ${visibleBeats.join(' / ')}. Preserve exact faces and costume states from all references. Follow the episode colour-key and the series state '${stateByEpisode(episodeNumber)}'. Cinematic mythic Mediterranean graphic-novel naturalism: tactile repaired lime plaster, salt, worked bronze, wool, linen, leather, olive wood, clay and human skin as appropriate. Prioritize causal action, relationship and recognition over spectacle. Use coherent screen direction, believable hands and anatomy, and one decisive sequential composition with enough detail for distinct crops. Keep faces, hands and key props safe inside the central 70 percent for 390px mobile crops. Reserve a clean lateral or upper negative-space band for HTML captions and speech bubbles. No text, letters, pseudo-writing, captions, speech bubbles, watermark, border, modern object, generic fantasy-game gloss, superhero style, anime drift, plastic skin or overprocessed HDR.`;
    queue.push({
      scene_master_id:`P8-${scene.scene_id}-MASTER`, episode:episode.episode, episode_number:episodeNumber, scene_id:scene.scene_id,
      title:episode.title, story_stage:episode.story_stage, location:scene.location, time:scene.time, cast:scene.cast,
      unit, panel_ids:scene.panel_ids, panel_count:scene.panel_ids.length, key_panel_id:key?.panel_id,
      p8_status:status, final_source_path:finalSource, authority, render_version:'V01',
      candidate_path:`comic-rendering/odyssey_m1_p8/candidate/scene-masters/P8-${scene.scene_id}-MASTER-V01.png`,
      final_master_path:`comic-rendering/odyssey_m1_p8/master/scene-masters/P8-${scene.scene_id}-MASTER-V01.png`,
      reference_assets:dedupedRefs, prompt
    });
  }
}
const counts = Object.fromEntries([...Map.groupBy(queue, (item) => item.p8_status)].map(([key,value]) => [key,value.length]));
if (queue.length !== 150) throw new Error(`Scene queue mismatch ${queue.length}`);
await writeJson('P8_SCENE_MASTER_QUEUE.json', { schema_version:'1.0.0', artifact_class:'P8_SCENE_MASTER_QUEUE', status:'READY', counts:{ total:150, ...counts }, scenes:queue });
console.log(JSON.stringify({ total:queue.length, ...counts }, null, 2));
