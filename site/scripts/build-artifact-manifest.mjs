import { createHash } from 'node:crypto';
import { readFile, readdir, stat, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
async function filesUnder(directory, excluded = () => false) {
  const output=[];
  async function walk(current){for(const name of (await readdir(current)).sort()){const target=path.join(current,name);const relative=path.relative(root,target).replaceAll(path.sep,'/');if(excluded(relative))continue;const info=await stat(target);if(info.isDirectory())await walk(target);else output.push({path:relative,bytes:info.size,sha256:sha(await readFile(target))});}}
  await walk(path.join(root,directory)); return output;
}
const source = await filesUnder('.', (relative) => /^(node_modules|dist|public\/media|\.astro)\//.test(relative) || relative === 'WEB_ARTIFACT_MANIFEST.json' || relative.startsWith('design/concepts/'));
const concepts = await filesUnder('design/concepts');
const dist = await filesUnder('dist', (relative)=>relative.startsWith('dist/media/'));
const responsiveMedia = await filesUnder('dist/media', (relative)=>path.basename(relative).includes('.') && !relative.endsWith('-w720.webp'));
const publicAssets = JSON.parse(await readFile(path.join(root,'content/ASSET_PUBLICATION_MANIFEST.json'),'utf8'));
const canonical = (entries) => entries.map((item)=>`${item.sha256}  ${item.path}\n`).join('');
const manifest = {
  artifact_class:'CTDE_WEB_ARTIFACT_MANIFEST', schema_version:'1.0.0', baseline_commit:'478fd10f5b115c70f7b4b8ce5146ae2b6c6d37e5',
  framework:'Astro 7 static + Pagefind', source_files:source, design_concepts:concepts,
  build:{file_count:dist.length,canonical_sha256:sha(canonical(dist)),files:dist},
  public_media:{asset_count:publicAssets.asset_count,total_bytes:publicAssets.total_bytes,manifest_sha256:sha(await readFile(path.join(root,'content/ASSET_PUBLICATION_MANIFEST.json')))},
  responsive_media:{file_count:responsiveMedia.length,total_bytes:responsiveMedia.reduce((sum,item)=>sum+item.bytes,0),canonical_sha256:sha(canonical(responsiveMedia))},
  exclusions:['node_modules','dist media duplicates','Astro cache','temporary screenshots']
};
await writeFile(path.join(root,'WEB_ARTIFACT_MANIFEST.json'),`${JSON.stringify(manifest,null,2)}\n`);
console.log(JSON.stringify({status:'PASS_WEB_ARTIFACT_MANIFEST',source_files:source.length,build_files:dist.length,build_sha256:manifest.build.canonical_sha256}));
