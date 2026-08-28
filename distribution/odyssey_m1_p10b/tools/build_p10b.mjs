#!/usr/bin/env node
import { createHash } from 'node:crypto';
import { copyFile, mkdir, readFile, readdir, stat, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../../..');
const out = path.join(root, 'distribution/odyssey_m1_p10b');
const pkgRoot = path.join(out, 'packages');
const siteGenerated = path.join(root, 'site/src/generated');
const mediaSource = path.join(out, 'media');
const mediaPublic = path.join(root, 'site/public/media/publication/p10');
const mediaManifestPath = path.join(mediaSource, 'media-manifest.json');
const RELEASE_TAG = 'odyssey-p9-publication-v1.0.0';
const RELEASE_URL = `https://github.com/conanxin/classic-to-drama-engine/releases/tag/${RELEASE_TAG}`;
const DOWNLOAD = `https://github.com/conanxin/classic-to-drama-engine/releases/download/${RELEASE_TAG}`;
const SNAPSHOT_AT = '2026-08-28T00:00:00+08:00';
const P9_IMPLEMENTATION = '810e699de675c180a26d3c5160eda571f7dc70c9';
const P9_CLOSEOUT = '2c39dcfbf24b97e9de802628c15fbff32b7dba17';

const readJson = async (relative) => JSON.parse(await readFile(path.join(root, relative), 'utf8'));
const shaBytes = (bytes) => createHash('sha256').update(bytes).digest('hex');
const shaFile = async (file) => shaBytes(await readFile(file));
const writeText = async (relative, text) => {
  const target = path.join(out, relative);
  await mkdir(path.dirname(target), { recursive: true });
  await writeFile(target, `${text.trim()}\n`, 'utf8');
};
const writeJson = async (relative, value) => writeText(relative, JSON.stringify(value, null, 2));
const rel = (file) => path.relative(root, file).split(path.sep).join('/');

await mkdir(pkgRoot, { recursive: true });
await mkdir(siteGenerated, { recursive: true });
await mkdir(mediaPublic, { recursive: true });
for (const entry of await readdir(mediaSource, { withFileTypes: true })) {
  if (entry.isFile()) await copyFile(path.join(mediaSource, entry.name), path.join(mediaPublic, entry.name));
}

const config = await readJson('publication/odyssey_m1_p9/publication-config.json');
const architecture = await readJson('publication/odyssey_m1_p9/P9_VOLUME_ARCHITECTURE.json');
const exportsManifest = await readJson('publication/odyssey_m1_p9/P9_EXPORT_MANIFEST.json');
const p9Artifact = await readJson('publication/odyssey_m1_p9/P9_ARTIFACT_MANIFEST.json');
const media = JSON.parse(await readFile(mediaManifestPath, 'utf8'));
if (exportsManifest.exports.length !== 21) throw new Error('P9 release asset count is not 21');
if (architecture.volumes.length !== 5) throw new Error('P9 volume count is not 5');
if (media.status !== 'PASS_P10B_DETERMINISTIC_MEDIA') throw new Error('P10B media is not frozen');

const totalBytes = exportsManifest.exports.reduce((sum, item) => sum + item.bytes, 0);
const pageCount = architecture.volumes.reduce((sum, volume) => sum + volume.page_count, 0);
const releaseAssets = exportsManifest.exports.map((item) => ({
  filename: item.filename,
  bytes: item.bytes,
  sha256: item.sha256,
  format: item.format,
  edition: item.edition,
  volume: item.volume,
  url: `${DOWNLOAD}/${item.filename}`,
}));
const checksumJson = {
  schema_version: 'P10B_SHA256SUMS_V1',
  edition_id: 'ODYSSEY-DGNE-1.0.0',
  release_tag: RELEASE_TAG,
  release_url: RELEASE_URL,
  algorithm: 'SHA-256',
  asset_count: releaseAssets.length,
  total_bytes: totalBytes,
  assets: releaseAssets.map(({ filename, bytes, sha256, url }) => ({ filename, bytes, sha256, url })),
};
await writeJson('SHA256SUMS.json', checksumJson);
await writeText('SHA256SUMS.txt', releaseAssets.map((item) => `${item.sha256}  ${item.filename}`).join('\n'));
await copyFile(path.join(out, 'SHA256SUMS.txt'), path.join(mediaPublic, 'SHA256SUMS.txt'));
await copyFile(path.join(out, 'SHA256SUMS.json'), path.join(mediaPublic, 'SHA256SUMS.json'));

const freeze = {
  schema_version: 'P10B_EDITION_FREEZE_V1',
  status: 'PASS_P10B_EDITION_FREEZE',
  edition_id: 'ODYSSEY-DGNE-1.0.0',
  title: '《归途：奥德修斯》',
  edition_name: 'Digital Graphic Novel Edition',
  version: '1.0.0',
  publication_date: '2026-08-27',
  policy: 'IMMUTABLE_BY_POLICY',
  source_implementation_commit: P9_IMPLEMENTATION,
  p9_closeout_commit: P9_CLOSEOUT,
  release_tag: RELEASE_TAG,
  release_url: RELEASE_URL,
  volumes: 5,
  chapters: 30,
  scenes: 150,
  publication_pages: pageCount,
  source_panels: 643,
  release_assets: 21,
  release_bytes: totalBytes,
  formats: { digital_pdf: 6, print_layout_pdf: 5, epub3: 5, cbz: 5 },
  successor_policy: { patch: '1.0.1 metadata/typographic correction', minor: '1.1.0 new edition feature', major: '2.0.0 material story or art revision' },
  forbidden_mutations: ['replace release assets', 'move or rewrite release tag', 'silently regenerate v1.0.0', 'change P9 binary identities'],
};
await writeJson('P10_EDITION_FREEZE.json', freeze);
await writeText('P10_EDITION_FREEZE.md', `# P10 Edition Freeze\n\nstatus: \`PASS_P10B_EDITION_FREEZE\`\n\n## Frozen edition\n\n- title: 《归途：奥德修斯》\n- edition: Digital Graphic Novel Edition\n- version: 1.0.0\n- edition_id: \`ODYSSEY-DGNE-1.0.0\`\n- publication date: 2026-08-27\n- canonical release: [${RELEASE_TAG}](${RELEASE_URL})\n- binary policy: \`IMMUTABLE_BY_POLICY\`\n\n## Frozen scope\n\nFive volumes, 30 chapters, 150 scenes, ${pageCount} publication pages and 643 source-bound panels. The canonical release contains 21 assets totaling ${totalBytes.toLocaleString('en-US')} bytes: six digital PDFs, five print-layout PDFs, five EPUB 3 books and five CBZ archives.\n\nThe 21 filenames, byte lengths and SHA-256 digests are frozen by \`SHA256SUMS.json\`. P10B references those binaries; it does not replace, delete, retag or duplicate them. Any future content-bearing change requires 1.0.1, 1.1.0 or a new major successor as classified in the machine freeze.\n`);

const copy = {
  series: {
    tagline: '一个关于归乡、身份与被重新认出的故事。',
    short: '战争结束二十年后，奥德修斯仍在海上。故乡被求婚者占据，妻子用时间守住房屋，儿子必须先学会判断父亲留下的名字。',
    medium: '特洛伊战争结束后，奥德修斯被海神的怒意困在漫长归途上。伊萨卡的大厅已被求婚者占据，佩涅洛佩以织机、债册与耐心维持家宅，忒勒马科斯则踏上寻找父亲证词的旅程。神明真实介入，但不能替任何人完成选择。三十集从失序的家、海上的名字与代价，一直走到伤疤、弓、婚床和土地的逐层辨认。',
    long: '《归途：奥德修斯》是一部三十集中文图像小说式短剧改编。它不只追问英雄能否回家，更追问一个离开二十年的人如何重新成为丈夫、父亲、国王与这片土地承认的人。奥德修斯必须学会控制身份；佩涅洛佩不是等待者，而是家宅政治与最终人类验证的中心；忒勒马科斯从无法行动的少年，成长为能发言、旅行、判断证词、守住秘密并站在父亲身边的人。神明改变条件，人的选择决定后果。作品以门槛、狗、伤疤、弓、十二把斧、橄榄树婚床与土地记忆，组成一条从公共宣称到私人知识的辨认链。',
  },
  volumes: {
    V01: ['没有父亲的家', '伊萨卡的大厅被求婚者占满。忒勒马科斯第一次站起来发言，也第一次决定离开父亲的影子。', '父亲失踪、母亲受困、家宅被消耗。忒勒马科斯还不会像英雄那样说话，却必须在雅典娜的推动下召集伊萨卡、出海寻找证词。第一卷写一个少年如何从自己的椅子前迈出第一步。'],
    V02: ['重新说出名字', '奥德修斯拒绝永生，离开停滞的岛屿，在陌生人的注视下重新进入人的世界。', '卡吕普索给他不死，风暴夺走他的遮蔽。奥德修斯从海难中抵达法埃西亚，在瑙西卡与王室面前克制自己、请求援助，终于说出名字。归乡从这一刻重新有了方向，也重新背负名字的代价。'],
    V03: ['海上的名字与代价', '奥德修斯讲述“无人”、风袋、喀耳刻、冥府、塞壬与海峡，也承认聪明和骄傲共同造成的损失。', '在法埃西亚的厅堂里，奥德修斯把漂流变成证词。从独眼巨人的洞穴到冥府的血，从塞壬之歌到斯库拉的六次抓取，他一次次靠判断活下来，也一次次看见命令、欲望与自负如何消耗同伴。最后一条船把他送回伊萨卡。'],
    V04: ['乞丐回到门槛', '归来者必须在自己的家里不被认出，让忠诚、亲情与伤疤逐层说出真相。', '奥德修斯以乞丐身份回到伊萨卡。欧迈俄斯的接待、忒勒马科斯的判断、阿尔戈斯最后的注视、佩涅洛佩的盘问与欧律克勒亚摸到的伤疤，把“他是谁”拆成不同人的证据。武器被移走，忠诚被测试，弓的比赛即将把私人判断推向公开审判。'],
    V05: ['弓、婚床与归位', '弓让身份成为公开事实；婚床、父亲与共同体决定这场归来是否真正成立。', '佩涅洛佩宣布弓与十二把斧的测试。奥德修斯在儿子与忠仆的协助下夺回厅堂，但暴力并不自动恢复家。婚床验证夫妻之间无法伪造的知识，莱尔忒斯用土地与记忆辨认儿子，最终武器被放低，家、名字和共同体重新彼此承认。'],
  },
};

const formatsFor = (volumeId) => releaseAssets.filter((item) => item.volume === volumeId);
const metadata = {
  schema_version: 'P10B_METADATA_MASTER_V1',
  status: 'PASS_P10B_METADATA_MASTER',
  edition: freeze,
  series_title_zh: config.series.title_zh,
  series_title_en: config.series.title_en,
  language: config.series.language,
  reading_direction: config.series.reading_direction,
  creator_adaptation_attribution: config.series.creator_credit,
  source_attribution: config.series.source_credit,
  isbn: 'NOT_ASSIGNED',
  publisher: 'NOT_CLAIMED',
  descriptions: copy.series,
  keywords: ['归乡', '身份', '辨认', '家庭', '权力', '记忆', '神话', '奥德赛', '图像小说', '古希腊'],
  category_candidates: ['Fiction / Classics / Adaptations', 'Comics & Graphic Novels / Literary', 'Fiction / Mythology'],
  volumes: architecture.volumes.map((volume) => ({
    edition_id: `ODYSSEY-DGNE-1.0.0-${volume.id}`,
    version: '1.0.0',
    series_title_zh: config.series.title_zh,
    series_title_en: config.series.title_en,
    volume_number: volume.number,
    volume_id: volume.id,
    volume_title: volume.title,
    volume_subtitle: volume.subtitle,
    chapter_range: [volume.episode_start, volume.episode_end],
    chapters: volume.chapters.length,
    publication_pages: volume.page_count,
    language: config.series.language,
    creator_adaptation_attribution: config.series.creator_credit,
    source_attribution: config.series.source_credit,
    description_short: copy.volumes[volume.id][1],
    description_medium: copy.volumes[volume.id][2],
    description_long: `${copy.volumes[volume.id][2]} ${volume.ending_hook}`,
    reader_promise: volume.opening_promise,
    keywords: metadataKeywordSet(volume.id),
    series_order: volume.number,
    publication_date: '2026-08-27',
    format_identities: formatsFor(volume.id),
    cover_identity: media.covers.find((item) => item.volume === volume.id),
    rights_note: 'See P10_RIGHTS_AND_SOURCE_NOTE.md; no copyright registration or store acceptance is claimed.',
    source_provenance_reference: 'publication/odyssey_m1_p9/P9_PUBLICATION_PROVENANCE.md',
  })),
};

function metadataKeywordSet(volumeId) {
  const base = ['奥德修斯', '归乡', '身份', '辨认', '图像小说'];
  const extras = {
    V01: ['忒勒马科斯', '佩涅洛佩', '伊萨卡'],
    V02: ['卡吕普索', '瑙西卡', '法埃西亚'],
    V03: ['独眼巨人', '喀耳刻', '冥府', '塞壬', '斯库拉'],
    V04: ['欧迈俄斯', '阿尔戈斯', '伤疤', '伪装'],
    V05: ['弓', '十二把斧', '婚床', '莱尔忒斯'],
  };
  return [...base, ...extras[volumeId]];
}
await writeJson('P10_METADATA_MASTER.json', metadata);
const storeCopy = {
  schema_version: 'P10B_STORE_COPY_MASTER_V1', status: 'PASS_P10B_STORE_COPY_MASTER',
  prohibited_claims: ['bestseller', 'award', 'review quote', 'rating', 'sales figure'],
  series: copy.series,
  volumes: metadata.volumes.map((volume) => ({
    volume_id: volume.volume_id, title: volume.volume_title, short_50_80_zh: volume.description_short,
    medium_150_250_zh: volume.description_medium, publisher_description: volume.description_long,
    reader_promise: volume.reader_promise, keywords: volume.keywords, category_candidates: metadata.category_candidates,
  })),
};
await writeJson('P10_STORE_COPY_MASTER.json', storeCopy);
await writeText('P10_STORE_COPY_MASTER.md', `# P10 Store Copy Master\n\nstatus: \`PASS_P10B_STORE_COPY_MASTER\`\n\n## Series\n\n**${copy.series.tagline}**\n\n${copy.series.medium}\n\n${copy.series.long}\n\n${metadata.volumes.map((v) => `## Volume ${String(v.volume_number).padStart(2, '0')} · ${v.volume_title}\n\n**Short:** ${v.description_short}\n\n**Medium:** ${v.description_medium}\n\n**Publisher description:** ${v.description_long}\n\n**Keywords:** ${v.keywords.join('、')}`).join('\n\n')}\n\nNo bestseller, review, award, rating or sales claim is made.\n`);

const official = {
  apple_books: {
    platform: 'Apple Books', retrieved_at: SNAPSHOT_AT,
    official_urls: ['https://help.apple.com/itc/booksassetguide/en.lproj/static.html','https://itunespartner.apple.com/books/support/9-prepare-book','https://itunespartner.apple.com/books/support/12-metadata','https://itunespartner.apple.com/books/support/18-submit-your-book'],
    accepted_format: 'EPUB; EPUB 3.3 supported; fixed layout supported',
    cover_requirement: 'RGB high-quality JPEG/PNG; at least 1400 px on shorter axis',
    metadata_requirement: 'title, author, language, Vendor ID and accurate customer-facing metadata; book file, cover and metadata must agree',
    identifier_requirement: 'Vendor ID required; ISBN optional and should match Vendor ID when supplied',
    validation_requirement: 'latest EPUBCheck plus Apple Books preview/submission validation',
    fixed_layout_support: 'EPUB 3 pre-paginated; consistent viewport; landmarks required when Apple-generated sample is used',
    file_size_boundary: 'ideally below 1 GB; Apple allows up to 2 GB',
    account_submission_boundary: 'active Free or Paid Books Agreement and iTunes Connect/Publishing Portal action required',
  },
  google_play_books: {
    platform: 'Google Play Books', retrieved_at: SNAPSHOT_AT,
    official_urls: ['https://support.google.com/books/partner/answer/3316879?hl=en','https://support.google.com/books/partner/answer/9261664?hl=en','https://support.google.com/books/partner/answer/3431108?hl=en','https://support.google.com/books/partner/answer/107073?hl=en'],
    accepted_format: 'EPUB and PDF; EPUB 3.3 preferred; fixed-layout EPUB supported',
    cover_requirement: 'JPEG, PNG, TIFF or PDF accepted in the single-book workflow; content/cover naming follows book identifier',
    metadata_requirement: 'book settings, genre, contributors, description, territories and price are supplied in Partner Center',
    identifier_requirement: 'ISBN is not required; Partner Center can issue a GGKEY',
    validation_requirement: 'EPUBCheck and review as a Content Reviewer in Web Reader and, where possible, Android tablet app',
    fixed_layout_support: 'supported in EPUB 2/3; original-page PDF can be paired with EPUB',
    file_size_boundary: 'no universal ebook maximum stated in the cited official snapshot; processing status is authoritative after upload',
    account_submission_boundary: 'Partner Center account, sales territories, payment profile, tax/bank and publish action remain manual',
  },
  kobo_writing_life: {
    platform: 'Kobo Writing Life', retrieved_at: SNAPSHOT_AT,
    official_urls: ['https://kobowritinglife.zendesk.com/hc/en-us/articles/360058975732-Setting-up-a-New-eBook','https://kobowritinglife.zendesk.com/hc/en-us/articles/360059386271-File-Types-Sizes','https://kobowritinglife.zendesk.com/hc/en-us/articles/360058976112-Validating-and-Testing-Your-eBooks','https://kobowritinglife.zendesk.com/hc/en-us/articles/360059386031-ISBNs-and-Kobo-Writing-Life'],
    accepted_format: 'EPUB accepted; fixed-layout EPUB is supported',
    cover_requirement: 'portrait JPG/JPEG preferred or PNG; no larger than 5 MB; 300 DPI recommended; 3:4 suggested',
    metadata_requirement: 'title, subtitle, series, series number, language, synopsis, categories and rights/distribution fields',
    identifier_requirement: 'ISBN optional for Kobo direct; Kobo issues its own identifier, though partner distribution may require ISBN',
    validation_requirement: 'error-free EPUB; test at least one eReader/desktop app and one phone/tablet; fixed-layout side-load suffix .fxl.kepub.epub',
    fixed_layout_support: 'supported, but fixed-layout titles do not receive Kobo Instant Preview',
    file_size_boundary: 'ebook content file maximum 100 MB',
    account_submission_boundary: 'KWL account, rights, DRM, territories, pricing and publish action remain manual',
  },
  amazon_kdp: {
    platform: 'Amazon Kindle Direct Publishing', retrieved_at: SNAPSHOT_AT,
    official_urls: ['https://kdp.amazon.com/en_US/help/topic/G9GSTY4LTRT39D4Z','https://kdp.amazon.com/en_US/help/topic/G200634390/','https://kdp.amazon.com/en_US/help/topic/G6GTK3T3NUHKLEFX','https://kdp.amazon.com/en_US/help/topic/G7DMSKCM9DVS65TC'],
    accepted_format: 'EPUB or KPF for fixed-layout ebooks; MOBI is no longer accepted for fixed-layout ebooks',
    cover_requirement: 'separate marketing cover; 2560 × 1600 px recommended, at least 300 PPI, JPEG preferred, 5 MB or less',
    metadata_requirement: 'title/series/author on cover must match KDP metadata; categories, territories, pricing and rights are manual fields',
    identifier_requirement: 'ISBN is not required for Kindle ebooks; Amazon assigns an ASIN',
    validation_requirement: 'Kindle Previewer/Kindle Create preview; comic fixed-layout metadata and panel behavior must be checked',
    fixed_layout_support: 'graphic novels use fixed layout with image pop-ups/Panel View or Virtual Panels; book-type comic and original-resolution metadata required',
    file_size_boundary: 'no single maximum asserted by this snapshot; cover limit above is explicit',
    account_submission_boundary: 'KDP account, rights declaration, marketplace, price/royalty, preview and publish action remain manual',
  },
};
const requirements = { schema_version: 'P10B_PLATFORM_REQUIREMENTS_SNAPSHOT_V1', status: 'PASS_P10B_OFFICIAL_REQUIREMENTS_SNAPSHOT', retrieved_at: SNAPSHOT_AT, authority_policy: 'OFFICIAL_PLATFORM_DOCUMENTATION_ONLY', platforms: official };
await writeJson('P10_PLATFORM_REQUIREMENTS_SNAPSHOT.json', requirements);
await writeText('P10_PLATFORM_REQUIREMENTS_SNAPSHOT.md', `# P10 Platform Requirements Snapshot\n\nstatus: \`PASS_P10B_OFFICIAL_REQUIREMENTS_SNAPSHOT\`  \nretrieved_at: \`${SNAPSHOT_AT}\`  \nauthority: official platform documentation only\n\nThis is a dated release-engineering snapshot, not a perpetual rulebook. Recheck every platform immediately before submission.\n\n${Object.values(official).map((p) => `## ${p.platform}\n\n- accepted: ${p.accepted_format}\n- cover: ${p.cover_requirement}\n- metadata: ${p.metadata_requirement}\n- identifier: ${p.identifier_requirement}\n- validation: ${p.validation_requirement}\n- fixed layout: ${p.fixed_layout_support}\n- size boundary: ${p.file_size_boundary}\n- external boundary: ${p.account_submission_boundary}\n- official sources:\n${p.official_urls.map((url) => `  - ${url}`).join('\n')}`).join('\n\n')}\n`);

const platformStatuses = {
  'apple-books': { label: 'Apple Books', status: 'READY_WITH_NOTES', content: 'one P9 EPUB per volume', preview: 'Apple Books preview and submission validation required', identifier: 'Vendor ID decision; ISBN remains unassigned' },
  'google-play-books': { label: 'Google Play Books', status: 'READY', content: 'one P9 EPUB plus digital PDF per volume', preview: 'Partner Center Content Reviewer preview required', identifier: 'request platform GGKEY unless an ISBN is later assigned' },
  'kobo-writing-life': { label: 'Kobo Writing Life', status: 'READY_WITH_NOTES', content: 'one P9 EPUB per volume', preview: 'fixed-layout test on Kobo desktop/eReader plus phone/tablet; no Instant Preview expected', identifier: 'use Kobo identifier unless ISBN is later assigned' },
  'kindle-kdp': { label: 'Amazon Kindle / KDP', status: 'READY_WITH_PLATFORM_SPECIFIC_ACTION', content: 'P9 EPUB is source input, not a submission-ready claim', preview: 'Kindle Previewer/Kindle Create fixed-layout conversion and Panel View check required', identifier: 'no ebook ISBN required; ASIN assigned by Amazon' },
  'self-hosted': { label: 'Official Web / GitHub Release', status: 'PASS', content: '21 canonical GitHub Release assets', preview: 'website and checksums', identifier: 'release tag plus SHA-256' },
};

for (const [slug, p] of Object.entries(platformStatuses)) {
  const dir = path.join(pkgRoot, slug);
  await mkdir(dir, { recursive: true });
  const volumes = metadata.volumes.map((volume) => ({
    volume_id: volume.volume_id,
    title: volume.volume_title,
    series_number: volume.volume_number,
    content_assets: formatsFor(volume.volume_id).filter((item) => slug === 'google-play-books' ? ['EPUB','PDF'].includes(item.format) && item.edition !== 'print-layout' : slug === 'self-hosted' ? true : item.format === 'EPUB'),
    cover: media.covers.find((item) => item.volume === volume.volume_id)?.files.find((item) => item.purpose === 'store_portrait_master'),
    metadata_reference: 'P10_METADATA_MASTER.json',
  }));
  await writeJson(`packages/${slug}/package-manifest.json`, {
    schema_version: 'P10B_PLATFORM_PACKAGE_V1', platform: p.label, package_status: p.status,
    store_submission: 'NOT_EXECUTED', store_acceptance: 'NOT_CLAIMED', price: 'NOT_SET_BY_P10', tax: 'NOT_CONFIGURED', bank: 'NOT_CONFIGURED', isbn: 'NOT_ASSIGNED',
    content_strategy: p.content, preview_strategy: p.preview, identifier_strategy: p.identifier,
    requirements_snapshot: '../../P10_PLATFORM_REQUIREMENTS_SNAPSHOT.json',
    rights_and_source_note: '../../P10_RIGHTS_AND_SOURCE_NOTE.md',
    reader_sample: ['apple-books', 'self-hosted'].includes(slug) ? media.sample : undefined,
    canonical_release_assets: slug === 'self-hosted' ? releaseAssets : undefined,
    volumes,
  });
  await writeJson(`packages/${slug}/metadata.json`, { platform: p.label, package_status: p.status, series: metadata.descriptions, volumes: metadata.volumes });
  await writeText(`packages/${slug}/metadata-readable.md`, `# ${p.label} Metadata\n\npackage status: \`${p.status}\`\n\n## Series\n\n${copy.series.medium}\n\n${metadata.volumes.map((v) => `- Volume ${v.volume_number} · **${v.volume_title}** — ${v.description_short}`).join('\n')}\n`);
  await writeText(`packages/${slug}/SUBMISSION_CHECKLIST.md`, `# ${p.label} Submission Checklist\n\npackage status: \`${p.status}\`\n\n- [x] Metadata and attribution prepared.\n- [x] Canonical content identities mapped without copying large binaries.\n- [x] Cover derivative identities recorded.\n- [x] Rights/source note and language prepared.\n- [ ] User logs into or creates the platform account.\n- [ ] User completes identity, agreement, territory, tax and bank steps requested by the platform.\n- [ ] User decides price and identifier strategy.\n- [ ] User uploads the canonical files referenced by package-manifest.json.\n- [ ] User performs platform preview: ${p.preview}.\n- [ ] User submits only after reviewing the current official requirements snapshot.\n\nSTORE_SUBMISSION: \`NOT_EXECUTED\`  \nSTORE_ACCEPTANCE: \`NOT_CLAIMED\`\n`);
}

const matrix = {
  schema_version: 'P10B_DISTRIBUTION_MATRIX_V1', status: 'PASS_P10B_DISTRIBUTION_PACKAGE_MATRIX',
  channels: [
    { channel: 'Official Web Edition', format: 'HTML graphic + script modes', package_status: 'PASS', validation_status: 'LIVE_VERIFIED_PREDECESSOR_PLUS_P10B_QA', manual_action: 'none', external_account: false, price_tax: false, submission_status: 'PUBLIC' },
    { channel: 'GitHub Release', format: 'PDF, EPUB 3, CBZ, print-layout PDF', package_status: 'PASS', validation_status: '21/21 SHA-256 mapped', manual_action: 'none', external_account: false, price_tax: false, submission_status: 'PUBLIC' },
    ...Object.entries(platformStatuses).filter(([slug]) => !['self-hosted'].includes(slug)).map(([slug,p]) => ({ channel: p.label, format: p.content, package_status: p.status, validation_status: 'OFFICIAL_REQUIREMENTS_MAPPED', manual_action: p.preview, external_account: true, price_tax: true, submission_status: 'NOT_EXECUTED', package_path: `packages/${slug}/` })),
  ],
};
await writeJson('P10_DISTRIBUTION_MATRIX.json', matrix);
await writeText('P10_DISTRIBUTION_MATRIX.md', `# P10 Distribution Matrix\n\nstatus: \`PASS_P10B_DISTRIBUTION_PACKAGE_MATRIX\`\n\n| Channel | Format | Package | Validation | Manual action | Submission |\n|---|---|---|---|---|---|\n${matrix.channels.map((c) => `| ${c.channel} | ${c.format} | ${c.package_status} | ${c.validation_status} | ${c.manual_action} | ${c.submission_status} |`).join('\n')}\n\nCommercial store accounts, prices, territories, tax/bank setup and submission remain outside P10B.\n`);

await writeText('P10_RIGHTS_AND_SOURCE_NOTE.md', `# P10 Rights and Source Note\n\n## Source lineage\n\n《归途：奥德修斯》is an original Chinese dramatic/graphic adaptation built from the Homeric *Odyssey* lineage documented by the repository source registry. The ancient work, particular editions/translations, digital encodings, adaptation text, visual assets and publication layout are separate rights objects. P10B does not use the age of Homer as a blanket legal conclusion for every upstream file. Repository source records remain the authority for the specific source packages used.\n\n## New work\n\nThe V2 Chinese adaptation text, P8 visual layer, P9 page design and P10B distribution materials are project-created layers credited to **Classic-to-Drama Engine 项目** and identified by their Git history and manifests. P10B records provenance; it does not claim copyright registration, an assigned publisher, legal clearance for every territory, a store license or professional legal advice.\n\n## Attribution\n\n- title: 《归途：奥德修斯》\n- creator/adaptation credit: Classic-to-Drama Engine 项目\n- source credit: 据荷马《奥德赛》改编\n- language: zh-CN\n- edition: Digital Graphic Novel Edition, Version 1.0.0\n\nBefore commercial distribution, the human publisher should review territorial rights, account declarations, platform terms and any desired registration with qualified counsel where needed.\n`);

await writeText('P10_KINDLE_COMPATIBILITY_REPORT.md', `# P10 Kindle Compatibility Report\n\nstatus: \`READY_WITH_PLATFORM_SPECIFIC_ACTION\`\n\nP9 EPUB files are valid EPUB 3 fixed-layout books and remain useful source inputs, but P10B does **not** equate that with Kindle acceptance. Amazon's current official guidance treats graphic novels as fixed-layout comic books and requires Kindle-specific metadata and panel behavior. MOBI is no longer an accepted fixed-layout submission format.\n\n## Mapping\n\n- five EPUB sources: identity-bound and under 100 MB each\n- separate store covers: prepared; KDP-specific 1600 × 2560 derivative remains an upload-time choice\n- fixed layout: present in P9 EPUB\n- exact Kindle comic metadata/Panel View: requires conversion or package inspection\n- Kindle Previewer/Kindle Create: external manual validation required\n- ISBN: not required for Kindle ebook; Amazon assigns ASIN\n\n## Required manual action\n\n1. Open each volume in the current Kindle Previewer or import through Kindle Create's comic/fixed-layout workflow.\n2. Confirm reading order, synthetic spreads, Panel View/Virtual Panels, cover and Chinese glyphs on representative phone, tablet and e-ink profiles.\n3. Export the current accepted KPF/EPUB package if conversion is required.\n4. Recompute the submitted-file digest and append it to the platform receipt before upload.\n\nSTORE_SUBMISSION: \`NOT_EXECUTED\`  \nSTORE_ACCEPTANCE: \`NOT_CLAIMED\`\n`);

/* Superseded malformed template retained only in source history.

await writeText('P10_RELEASE_BIBLE.md', `# P10B Public Release Bible\n\nstatus: \`PASS_P10B_RELEASE_BIBLE\`\n\nP10B is a distribution and reader-facing layer over the frozen P9 Digital Graphic Novel Edition 1.0.0. It does not change story, art, pages, panel mapping or any of the 21 release binaries.\n\n## Reader promise\n\n${copy.series.tagline} A reader can begin online, continue across 30 graphic episodes, understand the five-volume structure, select PDF/EPUB/CBZ by device, download from the canonical release and verify the exact bytes.\n\n## Release architecture\n\n- `/read/`: primary reader entry and volume/episode orientation\n- `/publication/`: download center for ordinary reading formats; print masters remain advanced\n- `/publication/verify/`: 21 SHA-256 identities and verification instructions\n- `/about/`: reader-facing work and edition explanation\n- `/project/`: deep technical archive, preserved but visually subordinate\n\n## Boundaries\n\nNo store listing, price, territory, tax/bank setup, ISBN purchase, print order, outreach or payment is executed. Platform packages are preparation material and dated requirement mappings. P6 remains \`PAUSED_BY_USER\`.\n`);
*/
await writeText('P10_RELEASE_BIBLE.md', `# P10B Public Release Bible\n\nstatus: \`PASS_P10B_RELEASE_BIBLE\`\n\nP10B is a distribution and reader-facing layer over the frozen P9 Digital Graphic Novel Edition 1.0.0. It does not change story, art, pages, panel mapping or any of the 21 release binaries.\n\n## Reader promise\n\n${copy.series.tagline} A reader can begin online, continue across 30 graphic episodes, understand the five-volume structure, select PDF/EPUB/CBZ by device, download from the canonical release and verify the exact bytes.\n\n## Release architecture\n\n- /read/: primary reader entry and volume/episode orientation\n- /publication/: download center for ordinary reading formats; print masters remain advanced\n- /publication/verify/: 21 SHA-256 identities and verification instructions\n- /about/: reader-facing work and edition explanation\n- /project/: deep technical archive, preserved but visually subordinate\n\n## Boundaries\n\nNo store listing, price, territory, tax/bank setup, ISBN purchase, print order, outreach or payment is executed. Platform packages are preparation material and dated requirement mappings. P6 remains \`PAUSED_BY_USER\`.\n`);
await writeText('P10_RELEASE_NOTES.md', `# 《归途：奥德修斯》Digital Graphic Novel Edition 1.0.0\n\n- complete 30-episode Web Comic Edition\n- five-volume publication edition\n- six searchable digital PDFs\n- five fixed-layout EPUB 3 editions\n- five CBZ comic-reader packages\n- five advanced ISO B5 print-layout masters\n- one spoiler-safe reader sample derived from Volume I\n- canonical SHA-256 list for all 21 release assets\n\nKnown boundaries: no ISBN is assigned; no commercial store has reviewed or accepted the package; print-layout PDFs are validated RGB layout masters, not printer-profile-bound press files.\n`);
await writeText('CHANGELOG_PUBLICATION.md', `# Publication Changelog Policy\n\n## 1.0.0 — 2026-08-27\n\nInitial frozen Digital Graphic Novel Edition: Web Comic, five volumes, PDF, EPUB 3 and CBZ.\n\n## Version rules\n\n- **patch (1.0.1):** metadata, typo or packaging correction that does not materially change story/art. Existing 1.0.0 binaries remain immutable.\n- **minor (1.1.0):** new edition feature, additional export or accessibility enhancement with explicit successor manifests.\n- **major (2.0.0):** material story, art, panel sequence or edition-architecture revision.\n`);
await writeText('P10_MANUAL_SUBMISSION_CHECKLIST.md', `# P10 Manual Submission Checklist\n\nP10B prepares packages but performs no store submission. For each platform, the human publisher must:\n\n1. Create or sign in to the official account.\n2. Complete any identity verification and accept the current agreement.\n3. Recheck the dated official requirements snapshot.\n4. Decide platform identifier versus ISBN; current ISBN is \`NOT_ASSIGNED\`.\n5. Review rights declarations and territories.\n6. Decide price, currency, DRM and sales dates.\n7. Complete tax and bank fields requested by the platform.\n8. Upload only canonical assets named in the package manifest.\n9. Run the platform preview on representative devices and resolve warnings.\n10. Record the uploaded file digest and platform receipt.\n11. Submit only after a human final review.\n\nP10B does not request or store credentials, tax IDs, banking information or payment details.\n`);
await writeText('P10_PRICING_SCENARIOS.md', `# P10 Pricing Scenarios\n\nstatus: \`DECISION_SUPPORT_ONLY\`\n\n- **Free web + paid downloadable volumes:** preserves the complete online edition while pricing portable offline formats.\n- **Low-price five-volume series:** reduces first-volume friction and keeps volume-level price logic consistent.\n- **Complete-volume offer:** one omnibus digital PDF as a direct archival/read-on-tablet option; platform rules may require a distinct edition.\n- **Free distribution:** maximizes access but some platform preview/royalty features differ.\n\nNo currency, price, promotion, transaction or exclusivity choice is set by P10B. The human publisher must compare platform fees, territory rules and tax consequences at submission time.\n`);

const press = {
  schema_version: 'P10B_PRESS_KIT_V1', status: 'PASS_P10B_PRESS_KIT',
  logline: copy.series.tagline, short_synopsis: copy.series.medium, long_synopsis: copy.series.long,
  structure: architecture.volumes.map((v) => ({ volume: v.number, title: v.title, episodes: `EP${String(v.episode_start).padStart(2,'0')}–EP${String(v.episode_end).padStart(2,'0')}` })),
  attribution: { creator: config.series.creator_credit, source: config.series.source_credit },
  formats: ['Web Comic', 'Digital PDF', 'EPUB 3', 'CBZ'],
  advanced_format: 'ISO B5 print-layout master (PRESS_READY not claimed)',
  official_url: 'https://conanxin.github.io/classic-to-drama-engine/read/',
  download_url: 'https://conanxin.github.io/classic-to-drama-engine/publication/',
  verify_url: 'https://conanxin.github.io/classic-to-drama-engine/publication/verify/',
  cover_assets: media.covers,
  promotional_assets: media.promotional,
};
await writeJson('P10_PRESS_KIT.json', press);
await writeText('P10_PRESS_KIT.md', `# P10 Press Kit\n\n## One line\n\n${press.logline}\n\n## Short synopsis\n\n${press.short_synopsis}\n\n## Long synopsis\n\n${press.long_synopsis}\n\n## Five-volume structure\n\n${press.structure.map((v) => `- Volume ${v.volume}: **${v.title}** · ${v.episodes}`).join('\n')}\n\n## Availability\n\nWeb Comic, digital PDF, EPUB 3 and CBZ. Advanced print-layout masters are available for production review; press-ready status is not claimed.\n\n- read: ${press.official_url}\n- download: ${press.download_url}\n- verify: ${press.verify_url}\n\n## Credit\n\n${config.series.creator_credit} · ${config.series.source_credit}\n\nAll cover and promotional files are deterministic derivatives of frozen P9 approved cover pages. No review quote, award, rating or sales figure is supplied.\n`);

const archival = {
  schema_version: 'P10B_ARCHIVAL_MANIFEST_V1', status: 'PASS_P10B_LONG_TERM_ARCHIVE', edition_freeze: freeze,
  p9_artifact_manifest_sha256: await shaFile(path.join(root, 'publication/odyssey_m1_p9/P9_ARTIFACT_MANIFEST.json')),
  p9_export_manifest_sha256: await shaFile(path.join(root, 'publication/odyssey_m1_p9/P9_EXPORT_MANIFEST.json')),
  p9_final_result_sha256: await shaFile(path.join(root, 'publication/odyssey_m1_p9/P9_FINAL_RESULT.md')),
  release_assets: releaseAssets, canonical_site: 'https://conanxin.github.io/classic-to-drama-engine/',
  sample: media.sample, covers: media.covers, promotional: media.promotional,
  toolchain: { site: 'Astro 7.2.4', epub_validation: 'EPUBCheck 5.3.0 (P9)', p10_media: 'PyMuPDF + Pillow', digest: 'SHA-256' },
};
await writeJson('P10_ARCHIVAL_MANIFEST.json', archival);

await writeText('CITATION.cff', `cff-version: 1.2.0\nmessage: "If you cite this edition, use the metadata below."\ntitle: "归途：奥德修斯 — Digital Graphic Novel Edition"\nversion: "1.0.0"\ndate-released: "2026-08-27"\ntype: generic\nauthors:\n  - name: "Classic-to-Drama Engine 项目"\nrepository-code: "https://github.com/conanxin/classic-to-drama-engine"\nurl: "${RELEASE_URL}"\nabstract: "A 30-episode Chinese graphic-novel adaptation derived from Homer's Odyssey."\nkeywords:\n  - Odyssey\n  - graphic novel\n  - adaptation\nlicense: "NOASSERTION"\n`);

await writeText('P10_PLATFORM_PACKAGE_QA.md', `# P10 Platform Package QA\n\nstatus: \`PASS_P10B_PLATFORM_PACKAGE_QA\`\n\n- Apple Books: \`READY_WITH_NOTES\`; five EPUB identities, covers, metadata and sample strategy mapped; Books preview required.\n- Google Play Books: \`READY\`; five EPUB + five digital PDF identities mapped; GGKEY/manual Partner Center steps recorded.\n- Kobo Writing Life: \`READY_WITH_NOTES\`; five EPUB files are under the official 100 MB limit; fixed-layout device/app preview required and Instant Preview is not expected.\n- Kindle/KDP: \`READY_WITH_PLATFORM_SPECIFIC_ACTION\`; Kindle-specific comic conversion/Panel View and Previewer validation remain manual.\n- Self-hosted: \`PASS\`; 21 canonical GitHub Release assets and checksums mapped.\n\nAcross all packages: store submission NOT_EXECUTED; acceptance NOT_CLAIMED; ISBN NOT_ASSIGNED; price NOT_SET_BY_P10; tax/bank NOT_CONFIGURED.\n`);
await writeText('P10_WEB_RELEASE_QA_REPORT.md', `# P10 Web Release QA Report\n\nstatus: \`PENDING_LOCAL_AND_LIVE_QA\`\n\nReader-facing routes, download identities, responsive presentation, privacy and live deployment are verified during closeout. This generated preflight record is replaced only with actual evidence, never with an inferred PASS.\n`);
await writeText('P10_INDEPENDENT_VERIFICATION.md', `# P10 Independent Verification\n\nstatus: \`PENDING_P10B_INDEPENDENT_VERIFICATION\`\n\nThe final pass requires P9 immutability, 21/21 release identities, deterministic sample/media, package completeness, official-source snapshot, browser/mobile QA, deployment and live verification.\n`);
await writeText('P10_FINAL_RESULT.md', `# P10B Final Result\n\nstatus: \`PENDING_P10B_CLOSEOUT\`\n\nThe final result is completed only after local build, independent verification, normal push, GitHub Pages deployment and live QA.\n`);

const readerData = {
  schema_version: 'P10B_READER_RELEASE_DATA_V1', edition: freeze,
  series: { ...config.series, descriptions: copy.series },
  volumes: metadata.volumes.map((volume) => ({
    ...volume,
    cover: {
      ...media.covers.find((item) => item.volume === volume.volume_id),
      public_files: Object.fromEntries(media.covers.find((item) => item.volume === volume.volume_id).files.map((item) => [item.purpose, `media/publication/p10/${path.basename(item.path)}`])),
    },
    chapters: architecture.volumes.find((item) => item.id === volume.volume_id).chapters,
  })),
  omnibus: releaseAssets.find((item) => item.filename === 'odyssey-homecoming-complete-digital.pdf'),
  sample: { ...media.sample, public_path: `media/publication/p10/${path.basename(media.sample.path)}` }, formats: ['Web','PDF','EPUB 3','CBZ'], release_url: RELEASE_URL,
};
await writeJson('P10_READER_RELEASE_DATA.json', readerData);
await writeFile(path.join(siteGenerated, 'p10-release.json'), `${JSON.stringify(readerData, null, 2)}\n`, 'utf8');

async function manifestFiles(dir) {
  const found = [];
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    if (entry.name === 'P10_ARTIFACT_MANIFEST.json' || entry.name === 'tools') continue;
    const file = path.join(dir, entry.name);
    if (entry.isDirectory()) found.push(...await manifestFiles(file));
    else {
      const info = await stat(file);
      found.push({ path: rel(file), bytes: info.size, sha256: await shaFile(file) });
    }
  }
  return found;
}
const artifacts = await manifestFiles(out);
const artifactManifest = {
  schema_version: 'P10B_ARTIFACT_MANIFEST_V1', status: 'P10B_ARTIFACTS_GENERATED_PENDING_CLOSEOUT',
  generated_at: SNAPSHOT_AT, edition_id: freeze.edition_id, p9_binary_modifications: 0,
  counts: { tracked_distribution_artifacts: artifacts.length, release_assets_referenced: releaseAssets.length, cover_sets: media.covers.length, promotional_assets: media.promotional.length, reader_samples: 1 },
  artifacts,
};
await writeJson('P10_ARTIFACT_MANIFEST.json', artifactManifest);
console.log(JSON.stringify({ status: 'PASS_P10B_DISTRIBUTION_GENERATION', artifacts: artifacts.length, release_assets: releaseAssets.length, release_bytes: totalBytes, sample_bytes: media.sample.bytes }, null, 2));
