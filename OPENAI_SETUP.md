# OpenAI setup for PressureTest

This build can run without OpenAI. If `OPENAI_API_KEY` is not set, use the manual copy/paste fallback in Brand & Territory Snapshot.

To enable the silent AI deep dive locally:

```bash
export OPENAI_API_KEY="paste-your-key-here"
streamlit run app.py
```

Optional model override:

```bash
export OPENAI_MODEL="gpt-4o-mini"
```

The OpenAI deep dive searches for brand, territory, closure, market withdrawal, competition, and outer-market expansion signals. Pasted manual notes feed the same scoring engine.
