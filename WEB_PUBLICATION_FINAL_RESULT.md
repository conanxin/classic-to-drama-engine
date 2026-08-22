# CTDE-WEB-02 Public Web Archive — Final Result

status:
PASS_CTDE_WEB_ARCHIVE_DEPLOYED_AND_LIVE_VERIFIED

baseline_commit:
478fd10f5b115c70f7b4b8ce5146ae2b6c6d37e5

phase_start_commit:
a233bfe5bea569cf07587b4894bc7ddb0553d67f

deployment_commit:
c03587dcb14f254c76563c6f46bd8805bc7a4629

web_framework:
Astro 7.2.4 + TypeScript + static generation + Pagefind 1.5.2 + deterministic CJK/English index

public_url:
https://conanxin.github.io/classic-to-drama-engine/

routes:
94/94 PASS

episode_count:
30

scene_count:
150

script_reader:
PASS — 30/30 published; EP01, EP10, EP19, EP25, EP27, EP29 and EP30 live-read with complete scenes, actions, character cues, dialogue and navigation

published_document_count:
18

published_image_count:
254 approved originals + 508 responsive WebP derivatives

published_video_count:
32

search_documents:
61 deterministic records + 93 Pagefind pages

live_route_crawl:
PASS — 94 routes, 802 assets and 32 video Range responses; 0 persistent HTTP, redirect, canonical, content-type or broken-reference failures

search:
PASS — 13 required Chinese/English queries live verified

visual_archive:
PASS — APPROVED only; rejected targets HF19/HF29/HF34/HF39/HF43/HF44 promoted occurrences 0

storyboards:
PASS — technical labelling, lazy delivery, board and episode navigation, keyboard lightbox

teaser:
PASS — P5 90-second Pitch Teaser and P4 teaser both explicitly PREVIS; play/pause/seek and Range delivery verified

animatics:
PASS — 30 entries, on-demand video attachment, required episode sample playback and seeking verified

desktop_QA:
PASS — 1440×900 and 1920×1080 reading and archive layouts

mobile_QA:
PASS — 390×844; no page overflow; responsive menu/images and usable EP27 dialogue measure

accessibility_QA:
PASS — semantic shell, skip link/focus, stateful reader controls, keyboard storyboard, native video controls, contrast and reduced motion

privacy_QA:
PASS — 0 local absolute paths, credentials, tokens or environment-path disclosures

SEO_QA:
PASS — robots, sitemap, canonical, Open Graph and unique page titles on the GitHub Pages subpath

build_result:
PASS — `npm run verify`, `npm run build`, Astro check and dist publication verifier

Pages_workflow:
- workflow: `Deploy CTDE web archive`
- initial enablement run: `32538248457` — blocked before build because Pages was not yet enabled
- first rerun: shallow-checkout history blocker
- repair: `.github/workflows/deploy-site.yml` uses `fetch-depth: 0`
- first successful deployment run: `32540231080`
- CTDE-WEB-02 deployment run: `32544769018`
- CTDE-WEB-02 run result: build SUCCESS; deploy SUCCESS

deployment_status:
LIVE_VERIFIED

publication_manifest_sha256:
a6d0dc4b9725b2af2415f2fe88c476f2c6b1c9da6105b577aeea0e7d8a15a317

asset_publication_manifest_sha256:
30236349d4573db6c928254b7cd60b5ae494af95414d5188a875bf50f4b00659

web_artifact_manifest_sha256:
428f83b87e7fdb5d2eea0673ffa1f43a0f208cb79c8d3e22c8fdc0d20ee8f405

live_deployment_QA_report:
site/LIVE_DEPLOYMENT_QA_REPORT.md

issue_register:
site/LIVE_SITE_ISSUE_REGISTER.md

issues_found:
7

issues_fixed_or_recovered:
7

unresolved_product_issues:
0

V2_modified:
0

P3_modified:
0

P4_modified:
0

P5_modified:
0

Runtime_modified:
0

P6_status:
PAUSED_BY_USER

P6_actions:
0

actor_outreach:
0

vendor_outreach:
0

real_world_research:
0

payments:
0

final_commit:
The deployment commit is recorded above. The metadata-only closeout commit is intentionally reported from Git after this self-referential result file is committed.

origin_main:
Must equal the metadata-only closeout commit after normal push; exact SHA is reported from Git outside this self-referential artifact.

working_tree:
Must be `CLEAN` after the closeout push; final verification is reported from Git outside this self-referential artifact.

## Historical Status Transition

The initial CTDE-WEB-01 result correctly stopped at `PASS_CTDE_WEB_ARCHIVE_READY_FOR_PAGES_ENABLEMENT`. After repository Pages enablement, a rerun exposed a shallow-checkout history assumption. Commit `a233bfe5bea569cf07587b4894bc7ddb0553d67f` fixed that workflow with `fetch-depth: 0`; run `32540231080` first deployed the archive successfully. CTDE-WEB-02 then audited, hardened and redeployed the public site at commit `c03587dcb14f254c76563c6f46bd8805bc7a4629`, with successful run `32544769018` and final live verification.

P6 remains paused. No casting, location, vendor, financing, outreach or payment work was performed.
