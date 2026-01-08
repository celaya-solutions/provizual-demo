# Construction Scraper Demo - Project Structure

```
construction-scraper-demo/
│
├── 📄 README.md                          # Comprehensive documentation
├── 📄 EMAIL_COVER_LETTER.md             # Email template for Provizual
├── 📄 LICENSE                            # MIT License
├── 📄 .gitignore                         # Git ignore rules
│
├── 🐍 server.py                          # Main MCP server (400+ lines)
│   ├── ConstructionScraper class
│   ├── ScraperConfig & ScraperResult models
│   ├── Pattern-based extraction logic
│   ├── MCP protocol implementation
│   ├── Tools: scrape_with_pattern, validate_scraper, extract_with_ai
│   └── Resource management (pattern library)
│
├── 🖥️ gui.py                             # Desktop GUI application (350+ lines)
│   ├── PyQt6 interface
│   ├── Pre-built pattern loading
│   ├── Real-time scraping with progress
│   ├── Results export (JSON/CSV)
│   └── Background threading for async operations
│
├── 📚 examples.py                        # 5 Working examples (300+ lines)
│   ├── Example 1: Construction project listings
│   ├── Example 2: Material pricing tracker
│   ├── Example 3: Pattern adaptation workflow
│   ├── Example 4: Production error handling
│   └── Example 5: Batch processing
│
├── 📦 requirements.txt                   # Python dependencies
│   ├── mcp (MCP protocol)
│   ├── playwright (Browser automation)
│   ├── pydantic (Data validation)
│   ├── PyQt6 (GUI framework)
│   ├── anthropic (Claude API)
│   └── beautifulsoup4, pandas, etc.
│
├── ⚙️ setup.sh                           # Automated installation script
│   ├── Python version check
│   ├── Virtual environment creation
│   ├── Dependency installation
│   ├── Playwright browser setup
│   └── Directory structure creation
│
├── 🔧 claude_desktop_config.json        # MCP server configuration
│   └── Ready to copy into Claude Desktop settings
│
├── 🧠 ai_extraction_prompt.md           # System prompt for LLM extraction
│   ├── Semantic understanding guidelines
│   ├── Construction industry context
│   ├── Output format specifications
│   └── Error handling strategies
│
└── 📐 architecture.md                    # System architecture diagrams
    ├── Overall system architecture
    ├── Data flow: Pattern-based scraping
    ├── Error handling flow
    ├── Pattern adaptation workflow
    ├── Integration options
    ├── Data pipeline
    └── Provizual integration path

Generated during runtime:
├── 📁 logs/                              # Application logs
├── 📁 screenshots/                       # Validation screenshots
└── 📁 exports/                           # Exported data (JSON/CSV)
```

## Key Features by File

### server.py (Core Engine)
- **ConstructionScraper class**: Async Playwright automation
- **Pattern-based extraction**: Configurable CSS selectors
- **MCP protocol**: Tools, resources, and server lifecycle
- **Error resilience**: Graceful handling of selector failures
- **Screenshot validation**: Visual QA artifacts
- **Metadata tracking**: URLs, timestamps, success rates

### gui.py (User Interface)
- **Tab-based interface**: Scraper, Patterns, History
- **Pattern library**: Pre-built construction industry patterns
- **Real-time execution**: Background threading for async scraping
- **Export functionality**: JSON and CSV formats
- **Visual feedback**: Progress indicators and result display

### examples.py (Documentation Through Code)
- **5 real-world scenarios**: Construction projects, pricing, contractors
- **Error handling demos**: Timeout, selector failures, site changes
- **Batch processing**: Multiple URLs with rate limiting
- **Pattern adaptation**: Shows how to update selectors
- **Production patterns**: Logging, monitoring, alerting hooks

### ai_extraction_prompt.md (Intelligence Layer)
- **Semantic extraction**: LLM-powered data extraction
- **Industry knowledge**: Construction-specific context
- **Fallback strategy**: When CSS selectors fail
- **Confidence scoring**: Validation of extracted data

### architecture.md (System Design)
- **Mermaid diagrams**: Visual system architecture
- **Integration paths**: How to connect with Provizual
- **Data flows**: Request → Scrape → Validate → Store
- **Deployment options**: MCP, Docker, AWS Lambda

## Technology Stack

**Core Technologies:**
- Python 3.9+
- Playwright (Browser automation)
- MCP Protocol (AI integration)
- Pydantic (Data validation)

**Optional Components:**
- PyQt6 (Desktop GUI)
- Anthropic API (LLM extraction)
- Docker (Containerization)

**Construction Industry Context:**
- Project listing patterns
- Material pricing patterns
- Contractor directory patterns
- Permit data patterns

## Lines of Code

| File | Lines | Purpose |
|------|-------|---------|
| server.py | 437 | MCP server implementation |
| gui.py | 368 | Desktop GUI application |
| examples.py | 304 | Working demonstrations |
| README.md | 500+ | Comprehensive documentation |
| ai_extraction_prompt.md | 180+ | LLM integration guide |
| architecture.md | 200+ | System design diagrams |
| **Total** | **~2000** | **Production-ready system** |

## What Makes This Special

1. **Complete System**: Not a code snippet—a full working application
2. **Production Ready**: Error handling, logging, monitoring, deployment
3. **Construction Focused**: Industry-specific patterns and examples
4. **Multiple Interfaces**: MCP server, GUI, Python API
5. **AI-Powered**: LLM fallback when selectors fail
6. **Well Documented**: Every file thoroughly explained
7. **Easy Setup**: One command installation

## Running the Project

```bash
# 1. Setup (one time)
./setup.sh

# 2. Activate environment
source venv/bin/activate

# 3. Choose your interface:

# Option A: Desktop GUI
python gui.py

# Option B: MCP Server
python server.py

# Option C: Run examples
python examples.py

# Option D: Direct Python usage
python
>>> from server import ConstructionScraper, ScraperConfig
>>> # Your code here
```

## Integration Timeline

**Week 1**: Setup and pattern migration
- Install and configure
- Convert existing NestJS patterns to Python equivalents
- Test on Provizual's target sites

**Week 2**: Team training and validation
- Train QA team on GUI interface
- Document pattern adaptation workflow
- Build validation test suite

**Week 3**: Production deployment
- Deploy MCP server alongside NestJS backend
- Configure monitoring and alerting
- Schedule automated scraping jobs

**Week 4**: Optimization and expansion
- Performance tuning
- Add new construction data sources
- Implement AI extraction for dynamic sites

## Questions This Project Answers

✅ Can you work with Playwright? → Full implementation included  
✅ Can you adapt scraping patterns? → 5 examples demonstrating this  
✅ Can you handle errors gracefully? → Error handling throughout  
✅ Can you build production systems? → Deployment-ready architecture  
✅ Do you understand construction data? → Industry-specific patterns  
✅ Can you work independently? → Built this entire system in one day  
✅ Can you collaborate with teams? → GUI for non-technical users  

## Next Steps

1. **Review the code**: Start with README.md, then server.py
2. **Run the examples**: `python examples.py`
3. **Try the GUI**: `python gui.py`
4. **Read the architecture**: See how it integrates with Provizual
5. **Contact me**: Discuss implementation details

---

**Built by Christopher Celaya**  
*Demonstrating Provizual-ready skills before the interview*
