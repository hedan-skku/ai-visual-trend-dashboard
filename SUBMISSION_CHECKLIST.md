# Submission Checklist

Upload these files and folders to GitHub:

- `app.py`
- `README.md`
- `requirements.txt`
- `.streamlit/config.toml`
- `data/`
- `assets/`
- `PRESENTATION_NOTES.md`
- `streamlit-preview.png`
- `representative-works-preview.png`
- `creative-strategy-preview.png`
- `real-references-preview.png`

Do not submit runtime/helper files:

- `streamlit_8510.log`
- `dashboard_watchdog.log`
- `dashboard_launchagent.log`
- `dashboard_launchagent.err.log`
- `start_dashboard.sh`
- `keep_dashboard_alive.sh`
- `com.hada.ai-visual-dashboard*.plist`

Before submitting, run:

```bash
streamlit run app.py
```

Then confirm:

- Homepage loads.
- `22,050` prompt signals appears.
- `AI Toolchain Snapshot` appears.
- `Representative Works` opens.
- `Creative Strategy` opens.
- `Real References` opens.
