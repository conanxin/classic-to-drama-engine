# Deployment

GitHub Actions runs `npm ci` and `npm run build` inside `site/`, uploads `site/dist`, and deploys through the official Pages action. The workflow has only `contents: read`, `pages: write` and `id-token: write` permissions.

Expected URL: <https://conanxin.github.io/classic-to-drama-engine/>.

If the workflow reports that Pages is not configured, the only manual action is:

1. Repository **Settings** → **Pages**.
2. Set **Source** to **GitHub Actions**.
3. Re-run **Deploy CTDE web archive**.

No FTP, server purchase or DNS change is required.

Vercel Git auto-deploy trigger verified on 2026-08-29.
