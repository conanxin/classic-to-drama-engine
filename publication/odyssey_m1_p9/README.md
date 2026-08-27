# P9 deterministic publication build

From the repository root:

```bash
python3 -m venv /tmp/p9-venv
/tmp/p9-venv/bin/pip install -r publication/odyssey_m1_p9/requirements.txt
/tmp/p9-venv/bin/python publication/odyssey_m1_p9/tools/p9_publication.py model
/tmp/p9-venv/bin/python publication/odyssey_m1_p9/tools/p9_publication.py gold
/tmp/p9-venv/bin/python publication/odyssey_m1_p9/tools/p9_publication.py export
/tmp/p9-venv/bin/python publication/odyssey_m1_p9/tools/p9_publication.py verify
```

`model` writes the tracked page/turn/volume authorities. `gold` creates an internal representative proof. `export` creates release-only PDF/EPUB/CBZ files under `exports/`. `verify` renders and validates all formal outputs and refreshes tracked QA reports/manifests.

The build expects Noto Sans CJK SC on the host and uses the frozen P7B/P8 manifests plus accepted P8 web visual files. It does not modify predecessor artifacts.
