# CTDE-WEB-01 Public Web Archive — Final Result

status:
PASS_CTDE_WEB_ARCHIVE_READY_FOR_PAGES_ENABLEMENT

baseline_commit:
478fd10f5b115c70f7b4b8ce5146ae2b6c6d37e5

web_framework:
Astro 7.2.4 + TypeScript + static generation + Pagefind 1.5.2 + deterministic CJK substring index

routes:
94

episode_count:
30

scene_count:
150

published_document_count:
18

published_image_count:
254 approved originals

responsive_image_derivatives:
254 WebP files / 7,164,612 bytes

published_video_count:
32

search_documents:
61 deterministic CJK records + 93 Pagefind pages

build_result:
PASS — 0 errors / 0 warnings / 0 hints; independent publication verifier PASS

browser_QA:
PASS — production static server, desktop route matrix, script reader, search, teaser, storyboard lightbox

mobile_QA:
PASS — 390x844 route matrix, zero page overflow, responsive menu/images, scroll-contained tables

accessibility_QA:
PASS — semantic shell, heading order, skip link/focus, alt, native video controls, reduced motion

Pages_workflow:
- workflow: `.github/workflows/deploy-site.yml`
- run: `https://github.com/conanxin/classic-to-drama-engine/actions/runs/32538248457`
- result: BLOCKED_AT_OFFICIAL_CONFIGURE_PAGES
- exact external cause: GitHub Pages site is not enabled/configured for GitHub Actions; REST Pages lookup returned 404.
- site install/build steps were not reached in GitHub Actions.
- this does not override the independently completed local production build.

deployment_status:
READY_FOR_PAGES_ENABLEMENT

public_url:
https://conanxin.github.io/classic-to-drama-engine/ (expected; not live until Pages enablement)

publication_manifest_sha256:
a6d0dc4b9725b2af2415f2fe88c476f2c6b1c9da6105b577aeea0e7d8a15a317

asset_publication_manifest_sha256:
30236349d4573db6c928254b7cd60b5ae494af95414d5188a875bf50f4b00659

web_artifact_manifest_sha256:
b8a6b4c6d191b5ad2d32067ab378e1cb1d4c1daf810dd22a03ec6703a74f9e2f

web_QA_report_sha256:
f1fd757cb29f072c30b453d7cef56a6e92ce4adfb8e8386aeaac154fbf9d1d8a

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
RESOLVE_FROM_GIT_HEAD_AFTER_THIS_RESULT_IS_COMMITTED

origin_main:
TO_BE_VERIFIED_AFTER_FINAL_PUSH

working_tree:
TO_BE_VERIFIED_CLEAN_AFTER_FINAL_PUSH

## Only remaining external publication action

Repository **Settings** → **Pages** → set **Source** to **GitHub Actions**, then re-run **Deploy CTDE web archive**.

No FTP, server purchase, custom domain or DNS change is required.
