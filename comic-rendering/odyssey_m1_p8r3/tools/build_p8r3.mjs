import { createHash } from 'node:crypto';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const phaseRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const repoRoot = path.resolve(phaseRoot, '../..');
const relative = (absolute) => path.relative(repoRoot, absolute).replaceAll(path.sep, '/');
const readJson = async (value) => JSON.parse(await readFile(path.join(repoRoot, value), 'utf8'));
const sha256 = (bytes) => createHash('sha256').update(bytes).digest('hex');
const fileIdentity = async (value) => {
  const bytes = await readFile(path.join(repoRoot, value));
  return { path:value, bytes:bytes.length, sha256:sha256(bytes) };
};

await mkdir(phaseRoot, { recursive:true });

const authorities = {
  episodes:'graphic-script/odyssey_m1_p7b/P7B_EPISODE_MANIFEST.json',
  panels:'graphic-script/odyssey_m1_p7b/P7B_PANEL_MANIFEST.json',
  visuals:'comic-rendering/odyssey_m1_p8/P8_WEB_VISUAL_MANIFEST.json',
  ep01_r1:'comic-rendering/odyssey_m1_p8r1/P8R1_EP01_COMIC_GRAMMAR.json',
  ep01_r2:'comic-rendering/odyssey_m1_p8r2/P8R2_EP01_FINAL_GRAMMAR.json'
};
const episodeManifest = await readJson(authorities.episodes);
const panelManifest = await readJson(authorities.panels);
const visualManifest = await readJson(authorities.visuals);
const ep01R1 = await readJson(authorities.ep01_r1);
const ep01R2 = await readJson(authorities.ep01_r2);
const panelById = new Map(panelManifest.panels.map((panel) => [panel.panel_id, panel]));

if (episodeManifest.counts.episodes !== 30 || episodeManifest.counts.scenes !== 150) throw new Error('P8R3 episode authority is not 30/150');
if (panelManifest.counts.panel_placements !== 643 || panelManifest.panels.length !== 643) throw new Error('P8R3 panel authority is not 643');
if (visualManifest.counts.panel_slots !== 643 || visualManifest.panels.length !== 643) throw new Error('P8R3 visual authority is not 643');
if (ep01R2.status !== 'PASS_EP01_FINAL_COMIC_GRAMMAR_LOCK') throw new Error('P8R3 gold standard is not locked');

function chooseComposition(scene, sceneIndex) {
  const panels = scene.panel_ids.map((id) => panelById.get(id));
  const types = new Set(panels.map((panel) => panel.panel_type));
  const highAction = panels.length >= 5 || types.has('ACTION') || types.has('CLIMAX');
  if (sceneIndex === 4) return 'intimate-cliffhanger';
  if (types.has('INSERT_PROP')) return 'intimate-prop-triptych';
  if (highAction) return sceneIndex % 2 === 0 ? 'crowd-action-mosaic' : 'establish-reaction-pair';
  if (['ESTABLISHING','ENVIRONMENT','POV'].includes(panels[0]?.panel_type)) return 'establish-reaction-pair';
  return 'threshold-dialogue-sequence';
}

function presentationFor(panel, panelIndex, sceneIndex, panelCount) {
  const hasDialogue = Boolean(panel.dialogue);
  const last = panelIndex === panelCount - 1;
  let textRole = 'SILENT_BEAT';
  if (hasDialogue && panel.panel_type === 'REACTION') textRole = 'SPEECH_REACTION';
  else if (hasDialogue && ['ACTION','INSERT_PROP'].includes(panel.panel_type)) textRole = 'SPEECH_ACTION';
  else if (hasDialogue) textRole = 'SPEECH';
  else if (panel.panel_type === 'REACTION') textRole = 'SILENT_REACTION';
  else if (panel.panel_type === 'INSERT_PROP') textRole = 'SILENT_INSERT';
  else if (panel.panel_type === 'ACTION') textRole = 'SILENT_ACTION';
  else if (last && sceneIndex === 4) textRole = 'CLIFFHANGER_ACTION';
  else if (panel.caption) textRole = 'NARRATION_CAPTION';

  const alignments = ['left-under','right-under','left-overlay','right-overlay'];
  const dialogueAlign = hasDialogue ? alignments[(panelIndex + sceneIndex) % alignments.length] : 'none';
  const wide = panelIndex === 0 || last || ['ESTABLISHING','ENVIRONMENT','ACTION','CLIMAX','REVEAL','POV'].includes(panel.panel_type);
  return { text_role:textRole, dialogue_align:dialogueAlign, width:wide ? 'wide' : 'medium' };
}

const sceneCompositions = {};
const panelPresentations = {};
const episodeSummaries = [];
for (const episode of episodeManifest.episodes) {
  let episodeReaction = 0;
  let episodeInsert = 0;
  for (const [sceneIndex, scene] of episode.scenes.entries()) {
    sceneCompositions[scene.scene_id] = episode.episode === 'EP01'
      ? ep01R1.scene_compositions[scene.scene_id]
      : chooseComposition(scene, sceneIndex);
    for (const [panelIndex, panelId] of scene.panel_ids.entries()) {
      const panel = panelById.get(panelId);
      const ep01Presentation = ep01R2.panel_presentation_overrides[panelId] || ep01R1.panel_presentations[panelId];
      const presentation = episode.episode === 'EP01'
        ? ep01Presentation
        : presentationFor(panel, panelIndex, sceneIndex, scene.panel_ids.length);
      if (!presentation) throw new Error(`Missing presentation for ${panelId}`);
      panelPresentations[panelId] = presentation;
      if (presentation.text_role.includes('REACTION')) episodeReaction += 1;
      if (presentation.text_role.includes('INSERT') || panel.panel_type === 'INSERT_PROP') episodeInsert += 1;
    }
  }
  episodeSummaries.push({
    episode:episode.episode,
    scenes:episode.scenes.length,
    panels:episode.scenes.reduce((count, scene) => count + scene.panel_ids.length, 0),
    reaction_beats:episodeReaction,
    insert_beats:episodeInsert,
    compositions:[...new Set(episode.scenes.map((scene) => sceneCompositions[scene.scene_id]))]
  });
}

if (Object.keys(sceneCompositions).length !== 150) throw new Error('P8R3 scene grammar coverage is not 150');
if (Object.keys(panelPresentations).length !== 643) throw new Error('P8R3 panel presentation coverage is not 643');
for (const [panelId, value] of Object.entries(ep01R1.panel_presentations)) {
  const expected = ep01R2.panel_presentation_overrides[panelId] || value;
  if (JSON.stringify(panelPresentations[panelId]) !== JSON.stringify(expected)) throw new Error(`EP01 gold standard drift: ${panelId}`);
}

const authorityIdentities = {};
for (const [key, value] of Object.entries(authorities)) authorityIdentities[key] = await fileIdentity(value);
const reactionBeats = Object.entries(panelPresentations).filter(([, value]) => value.text_role.includes('REACTION')).map(([id]) => id);
const insertBeats = panelManifest.panels.filter((panel) => panel.panel_type === 'INSERT_PROP').map((panel) => panel.panel_id);
const grammar = {
  artifact_class:'ODYSSEY_P8R3_SERIES_COMIC_READING_GRAMMAR',
  schema_version:'1.0.0',
  repair_id:'ODYSSEY-P8R3',
  status:'PASS_P8R3_GRAMMAR_AUTHORITY_GENERATED',
  human_authorization:{
    exact_quote:'EP01_FINAL_COMIC_GRAMMAR: APPROVED_FOR_SERIES_PROPAGATION',
    gold_standard:'EP01 live P8R2 final comic grammar',
    propagation_scope:'EP02-EP30'
  },
  authorities:authorityIdentities,
  coverage:{ episodes:30, scenes:150, panel_slots:643, script_source_layers:150, episode_covers:30, cliffhangers:30 },
  rules:{
    story_first:true,
    panel_sequence_authoritative:true,
    art_preview_slots:643,
    panel_sized_empty_text_rectangles_allowed:0,
    text_containers_intrinsic_height:true,
    speech_caption_separated:true,
    source_layer_default:'collapsed',
    relationship_context_default:'collapsed',
    cast_level_default:'GLANCE',
    mobile_single_stream:true,
    raster_text_allowed:0,
    exact_source_dialogue_required:true,
    narrative_events_may_change:false
  },
  counts:{
    reaction_beats:reactionBeats.length,
    insert_beats:insertBeats.length,
    new_visual_assets:0,
    reused_accepted_visual_slots:643
  },
  episode_summaries:episodeSummaries,
  scene_compositions:sceneCompositions,
  panel_presentations:panelPresentations,
  source_modifications:{ V2:0, P3:0, P4:0, P5:0, Runtime:0, P7B_narrative_authority:0, P8_visual_authority:0, P8R1_visual_authority:0, P8R2_gold_standard:0 },
  P6_status:'PAUSED_BY_USER'
};

const grammarPath = path.join(phaseRoot, 'P8R3_SERIES_COMIC_GRAMMAR.json');
await writeFile(grammarPath, `${JSON.stringify(grammar, null, 2)}\n`);

const report = `# ODYSSEY-P8R3 Series Comic Grammar Propagation\n\nStatus: \`P8R3_GRAMMAR_AUTHORITY_READY\`\n\n## Human authorization\n\n\`EP01_FINAL_COMIC_GRAMMAR: APPROVED_FOR_SERIES_PROPAGATION\`\n\nEP01 P8R2 remains the sole gold standard. P8R3 derives presentation only for EP02-EP30 and does not change narrative slots, visual selection, captions, dialogue, source layers, scene order, or episode order.\n\n## Coverage\n\n- Episodes: 30 / 30\n- Scenes: 150 / 150\n- Narrative visual slots: 643 / 643\n- Accepted visuals reused: 643\n- Newly generated visuals: 0\n- Reaction beats: ${reactionBeats.length}\n- Insert-prop beats: ${insertBeats.length}\n- Scene compositions: ${new Set(Object.values(sceneCompositions)).size}\n- Collapsed source layers: 150\n- Comic cliffhangers: 30\n\n## Propagation contract\n\nEvery episode uses a story-first art cover, four-person GLANCE cast entry, optional deeper identity and relationship help, intrinsic-height text, distinct semantic speech and narration, real accepted-art previews under lazy responsive images, content-aware panel composition, compact consequence/source controls, and an image-led final cliffhanger. Mobile collapses every scene into one continuous narrative stream.\n\n## Evidence boundary\n\nThis is a presentation propagation. It creates no visual art and makes no real-reader claim. V2, P3, P4, P5, Runtime, P7B narrative authority, P8 visual authority, and the human-approved EP01 gold standard remain unchanged.\n`;
await writeFile(path.join(phaseRoot, 'P8R3_PROPAGATION_REPORT.md'), report);

const optional = ['P8R3_INDEPENDENT_VERIFICATION.md','P8R3_FINAL_RESULT.md'];
const artifactPaths = [relative(new URL(import.meta.url).pathname), relative(grammarPath), relative(path.join(phaseRoot, 'P8R3_PROPAGATION_REPORT.md'))];
for (const name of optional) {
  try { await readFile(path.join(phaseRoot, name)); artifactPaths.push(relative(path.join(phaseRoot, name))); } catch { /* closeout artifacts are added after live QA */ }
}
const artifacts = await Promise.all(artifactPaths.sort().map(fileIdentity));
const manifest = {
  artifact_class:'ODYSSEY_P8R3_ARTIFACT_MANIFEST',
  schema_version:'1.0.0',
  status:'P8R3_ARTIFACTS_FROZEN',
  artifact_count:artifacts.length,
  artifacts
};
await writeFile(path.join(phaseRoot, 'P8R3_ARTIFACT_MANIFEST.json'), `${JSON.stringify(manifest, null, 2)}\n`);

console.log(JSON.stringify({
  status:grammar.status,
  episodes:30,
  scenes:150,
  panels:643,
  reaction_beats:reactionBeats.length,
  insert_beats:insertBeats.length,
  compositions:new Set(Object.values(sceneCompositions)).size,
  artifact_manifest_sha256:sha256(await readFile(path.join(phaseRoot, 'P8R3_ARTIFACT_MANIFEST.json')))
}));
