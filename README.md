# ResearchFlow

ResearchFlow is a professional AI-powered research workspace that automatically searches sources, extracts evidence, drafts reports, reviews them, and publishes final revisions.

## Features

- 🔍 **Intelligent Web Search** - Finds credible sources using Tavily API
- 📄 **Smart Content Extraction** - Scrapes and cleans web content
- ✍️ **AI Report Writing** - Generates structured research reports
- 🔎 **Automated Review** - Critiques reports for quality and accuracy
- ♻️ **Iterative Refinement** - Revises reports based on feedback
- 📊 **Live Progress Tracking** - Visual pipeline with real-time updates
- 🎨 **Dark Professional UI** - Clean, modern interface

## Flow

```
Topic Brief → Search → Scrape → Draft → Review → Revise → Final Report
```

## Quick Start

### Local Development

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd Multi-Agent-System
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**

Create a `.env` file:
```env
TAVILY_API_KEY=your_tavily_api_key
MISTRAL_API_KEY=your_mistral_api_key
```

4. **Run the app**
```bash
streamlit run app.py
```

### Get API Keys

- **Tavily API**: https://tavily.com (for web search)
- **Mistral API**: https://console.mistral.ai (for AI models)

## Project Structure

```
.
├── app.py                  # Streamlit entrypoint
├── agents.py               # Agent and chain definitions
├── tools.py                # Web search and scraping tools
├── researchflow/
│   ├── app.py              # Main UI and workflow
│   ├── ui.py               # UI components
│   ├── service.py          # Pipeline execution
│   ├── theme.py            # Styling and theme
│   ├── config.py           # App configuration
│   └── env.py              # Environment helper
├── requirements.txt        # Python dependencies
└── DEPLOYMENT.md           # Deployment guide
```

## Tech Stack

- **LangChain** - Agent and chain orchestration
- **LangGraph** - Agent execution framework
- **Mistral AI** - Language model (mistral-small-latest)
- **Tavily** - Web search API
- **BeautifulSoup4** - Web scraping
- **Streamlit** - Web interface

## Deployment

Deploy to Streamlit Cloud in minutes. See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

**Quick Deploy:**
1. Push to GitHub
2. Connect at https://share.streamlit.io
3. Set Python version to 3.11 (automatic with runtime.txt)
4. Add API keys in Secrets settings
5. Deploy!

**Important Files for Deployment:**
- `runtime.txt` - Specifies Python 3.11
- `packages.txt` - System dependencies (libxml2, libxslt, zlib)
- `requirements.txt` - Python dependencies (pinned versions)
