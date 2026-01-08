# Construction Data Scraper
**Production-Ready MCP Server for Construction Industry Web Scraping**

Built specifically to demonstrate pattern-based scraping workflows for construction tech companies like Provizual.

---

## 🎯 What This Solves

Construction companies need to extract data from hundreds of sources:
- **Project listings** from government sites and construction databases
- **Material pricing** from supplier websites that change frequently
- **Contractor information** from directories and review sites
- **Permit data** from municipal portals

This MCP server provides:
✅ **Pattern-based scraping** - Copy/adapt selector patterns for new sites  
✅ **Playwright integration** - Handle JavaScript-heavy modern sites  
✅ **Error resilience** - Graceful handling of selector changes and failures  
✅ **LLM fallback** - AI-powered extraction when selectors break  
✅ **GUI interface** - Non-technical team members can run scrapers  
✅ **MCP protocol** - Integrates with Claude Desktop, IDEs, automation tools

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         Client Applications             │
│  (Claude Desktop, Custom Tools, APIs)   │
└──────────────┬──────────────────────────┘
               │ MCP Protocol
┌──────────────▼──────────────────────────┐
│       Construction Scraper Server       │
│  • Pattern Management                   │
│  • Playwright Browser Automation        │
│  • Selector Validation                  │
│  • Data Extraction & Structuring        │
└──────────────┬──────────────────────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
    ▼          ▼          ▼
┌────────┐ ┌────────┐ ┌──────────┐
│Website │ │Website │ │ Website  │
│   A    │ │   B    │ │    C     │
└────────┘ └────────┘ └──────────┘
```

---

## 🚀 Quick Start

### Installation

```bash
# Clone or download this repository
cd provizual-scraper-demo

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### Usage Options

#### 1. **MCP Server Mode** (Integrate with Claude Desktop)

Add to your MCP settings (`~/Library/Application Support/Claude/claude_desktop_config.json` on Mac):

```json
{
  "mcpServers": {
    "construction-scraper": {
      "command": "python",
      "args": ["/path/to/provizual-scraper-demo/server.py"]
    }
  }
}
```

Restart Claude Desktop. You can now ask:
- "Use the construction-scraper to extract project data from [URL]"
- "Validate selectors for material pricing at [site]"

#### 2. **GUI Mode** (For Non-Technical Users)

```bash
python gui.py
```

Opens a desktop application where team members can:
- Load pre-built scraping patterns
- Enter URLs and customize selectors
- Run scrapers with one click
- Export results as JSON or CSV

#### 3. **Direct Python Integration**

```python
from server import ConstructionScraper, ScraperConfig
import asyncio

async def scrape_example():
    scraper = ConstructionScraper()
    
    config = ScraperConfig(
        url="https://example.com/projects",
        selectors={
            "project_name": ".project-title",
            "location": ".location",
            "budget": ".cost"
        },
        screenshot=True
    )
    
    result = await scraper.scrape_pattern(config)
    print(result.data)
    await scraper.cleanup()

asyncio.run(scrape_example())
```

---

## 📋 Available Tools

### 1. `scrape_with_pattern`
Execute web scraping using defined CSS selectors.

**Input:**
```json
{
  "url": "https://construction-site.com/data",
  "selectors": {
    "field_name": ".css-selector"
  },
  "wait_for": ".content-loaded",
  "screenshot": false
}
```

**Output:**
- Structured JSON data
- Validation metadata
- Error reports
- Optional screenshots

### 2. `validate_scraper`
Test selectors without full data extraction. Perfect for debugging when sites change their HTML structure.

### 3. `extract_with_ai`
LLM-powered fallback extraction when traditional selectors fail. Uses Claude API to semantically understand page content.

---

## 🎨 Pre-Built Patterns

### Construction Projects
Extract project listings from construction databases:
```json
{
  "project_name": ".project-title, h1.title",
  "project_type": ".project-type, .category",
  "location": ".location, .address",
  "budget": ".budget, .cost",
  "status": ".status, .project-status",
  "contractor": ".contractor, .gc-name",
  "completion_date": ".completion, .end-date"
}
```

### Material Pricing
Track building material costs across suppliers:
```json
{
  "material_name": ".product-name, h2.title",
  "price": ".price, .cost",
  "unit": ".unit, .uom",
  "supplier": ".supplier, .vendor",
  "availability": ".stock, .availability"
}
```

### Contractor Information
Build contractor/supplier databases:
```json
{
  "company_name": ".company-name, h1",
  "contact_email": "a[href^='mailto:']",
  "phone": ".phone, .contact-number",
  "address": ".address, .location",
  "specialties": ".specialty, .services",
  "certifications": ".certification, .license"
}
```

---

## 🔧 Real-World Usage Patterns

### Pattern Adaptation (Core Provizual Workflow)

1. **Start with existing pattern:**
   ```python
   # Load construction project pattern
   base_selectors = {
       "project_name": ".project-title",
       "location": ".location"
   }
   ```

2. **Adapt for new site:**
   ```python
   # Site uses different classes
   adapted_selectors = {
       "project_name": ".title, h1.project-heading",
       "location": ".project-location, .address"
   }
   ```

3. **Validate before production:**
   ```bash
   # Test with validate_scraper tool
   # Verify element counts and content
   ```

4. **Run and monitor:**
   ```bash
   # Execute scraping
   # Check for errors
   # Screenshot for QA validation
   ```

### Handling Site Changes

When a site updates their HTML structure:

```python
# Old selector stops working
old_selector = {"price": ".product-price"}

# Update selector to new structure
new_selector = {"price": ".price-display, .cost"}

# Or use multiple fallback selectors
fallback_selector = {"price": ".price, .cost, [data-price]"}
```

The scraper automatically tries multiple selectors in sequence.

### Error Recovery

```python
result = await scraper.scrape_pattern(config)

if not result.success:
    # Log errors for investigation
    for error in result.errors:
        logger.error(f"Selector issue: {error}")
    
    # Fall back to AI extraction
    ai_result = await extract_with_ai(url, fields=["price", "name"])
```

---

## 🧪 Testing & Validation

### Selector Testing
```bash
# Test selectors without full scraping
python -c "
from server import ConstructionScraper
import asyncio

async def test():
    scraper = ConstructionScraper()
    # Validation logic here
    await scraper.cleanup()

asyncio.run(test())
"
```

### Integration Testing
```bash
# Run against test sites
pytest tests/test_scraper.py

# Test specific patterns
pytest tests/test_patterns.py -k "construction_projects"
```

---

## 📊 Data Export Formats

### JSON (Structured)
```json
{
  "project_name": "Downtown Convention Center",
  "location": "Dallas, TX",
  "budget": "$45,000,000",
  "contractor": "ABC Construction",
  "status": "In Progress"
}
```

### CSV (Spreadsheet-Ready)
```csv
project_name,location,budget,contractor,status
Downtown Convention Center,"Dallas, TX",$45000000,ABC Construction,In Progress
```

### Database Integration
Direct insertion into PostgreSQL, MySQL, SQLite:
```python
import pandas as pd
from sqlalchemy import create_engine

df = pd.DataFrame([result.data])
engine = create_engine('postgresql://user:pass@localhost/construction_db')
df.to_sql('projects', engine, if_exists='append')
```

---

## 🔐 Best Practices

### Rate Limiting
```python
config = ScraperConfig(
    url=target_url,
    selectors=selectors,
    timeout=30000  # Adjust based on site
)

# Add delays between requests
await asyncio.sleep(2)
```

### User-Agent Rotation
```python
# Implemented in server.py
await page.set_extra_http_headers({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)..."
})
```

### Error Handling
- Graceful selector failures
- Screenshot capture for debugging
- Detailed error logging
- Automatic retry logic (implementable)

---

## 🏢 Production Deployment

### Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN playwright install --with-deps chromium

COPY . .
CMD ["python", "server.py"]
```

### AWS Lambda (Serverless)
Use AWS Lambda with Playwright for scheduled scraping:
```python
# lambda_handler.py
from server import ConstructionScraper, ScraperConfig

def lambda_handler(event, context):
    # Scraping logic here
    pass
```

### Monitoring & Alerts
```python
# Add monitoring hooks
if not result.success:
    send_slack_alert(f"Scraper failed: {result.errors}")
```

---

## 📈 Provizual Integration Path

### Phase 1: Pattern Library
1. Document existing NestJS scraper patterns
2. Convert to Python/Playwright equivalents
3. Add to pattern library in `server.py`

### Phase 2: Testing Framework
1. Implement automated selector validation
2. Build regression testing for site changes
3. Create pattern performance metrics

### Phase 3: Production Integration
1. Deploy as microservice alongside NestJS backend
2. Expose REST API for scraper execution
3. Integrate with existing data pipeline

### Phase 4: Team Enablement
1. Train QA team on pattern adaptation
2. Deploy GUI for non-technical users
3. Build monitoring dashboard

---

## 🤝 Why This Fits Provizual

**Direct Alignment:**
- ✅ TypeScript/JavaScript experience → Python is syntactically similar
- ✅ Playwright expertise → Same browser automation tool
- ✅ Pattern-based workflow → Exactly matches job description
- ✅ NestJS background → Easy to integrate with existing backend
- ✅ QA mindset → Built-in validation and testing tools

**Immediate Value:**
- Ready-to-use patterns for construction data sources
- GUI for team collaboration
- MCP protocol for AI-assisted development
- Production-ready error handling

**Growth Potential:**
- Foundation for automated testing suite
- Scales to handle multiple sites simultaneously
- Extensible pattern library system
- Integration with CI/CD pipelines

---

## 📞 Contact

**Christopher Celaya**  
Industrial Electrical Technician | AI Research Engineer  
Celaya Solutions | El Paso, TX
  
**Research:** celayasolutions.com

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

Built to demonstrate practical construction tech solutions.  
Inspired by real-world web scraping challenges in construction data extraction.  
Designed for immediate integration into production environments like Provizual.

---

**Note to Provizual Team:**

This project demonstrates not just technical skills, but **understanding of your exact workflow**:
- Pattern-based scraping (your core operational model)
- Playwright + TypeScript ecosystem (your tech stack)
- Error handling for production reliability (your business requirement)
- Team-friendly tools for QA collaboration (your job posting emphasis)

I built this specifically to show I already understand what you need.
