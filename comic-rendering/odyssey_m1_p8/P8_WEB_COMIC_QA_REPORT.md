# P8 Web Comic QA Report

Status: **BLOCKED_P8_LIVE_BROWSER_POLICY_VERIFICATION**

- Final visual mapping: 643 / 643
- Episode covers: 30 / 30
- Web derivatives: 643 WebP files
- Raster text contamination: 0 intended; dialogue and captions remain semantic HTML
- Public technical storyboard / animatic as primary comic art: 0
- 390px crop-safe audit: PASS
- Responsive publication integration: PASS (`npm run check`, `npm run verify`, `npm run build`)
- Static routes built: 128
- Search pages indexed: 127
- P8 dist verification: PASS, 643 / 643 final-art paths
- Script routes: PASS, 30 / 30 unchanged
- Graphic routes: PASS, 30 / 30
- GitHub Pages build: PASS
- GitHub Pages deploy: PASS
- Deployment commit: `de5c43eea6e809cf0bbc7b8c6ede78cd9f89d2d5`
- Successful workflow run: `32973636849`
- Public URL: `https://conanxin.github.io/classic-to-drama-engine/`

## Live browser boundary

The Codex in-app browser attempted the public HTTPS URL three times, including a fresh tab after the successful deployment. Each attempt was denied before navigation because the admin-enforced browser security policy could not be verified. The same policy also denied localhost. No alternate browser surface, direct fetch, or indirect route was used to bypass that control.

Consequently, online desktop/mobile screenshots, interactive character-assist checks, and visual live-route confirmation remain unclaimed. GitHub independently reports both build and deploy successful, but that is not substituted for live visual QA.

Manual closeout requires opening the deployed routes below at 1440×900 and 390×844, confirming P8 art loads with no horizontal overflow, then resuming P8 with that evidence:

- `/episodes/01/graphic/`
- `/episodes/10/graphic/`
- `/episodes/19/graphic/`
- `/episodes/27/graphic/`
- `/episodes/29/graphic/`
- `/episodes/30/graphic/`
