# Construction Scraper - Test Sites List

## 🏗️ Quick Reference

This list provides real-world construction industry websites to test your scraper against. Organized by use case with difficulty ratings and notes.

---

## 🏛️ Government Permit Databases

### Federal Level

**1. Census Bureau Building Permits**
- URL: https://www.census.gov/construction/bps/
- Difficulty: ⭐⭐ (Medium - structured data)
- Data: National building permit statistics
- Selectors to try: `.data-table`, `.statistics`, `.permit-data`

**2. HUD Building Permits Database**
- URL: https://socds.huduser.gov/permits/
- Difficulty: ⭐⭐⭐ (Hard - may use frames/iframes)
- Data: County-level residential construction permits
- Note: Test iframe handling

**3. Data.gov Construction Permits**
- URL: https://catalog.data.gov/dataset/?tags=permits
- Difficulty: ⭐⭐ (Medium)
- Data: Various federal permit datasets
- Selectors: `.dataset-heading`, `.dataset-item`, `.resource-url-analytics`

### City/County Level (Great for testing selector variations)

**4. NYC Building Permits**
- URL: https://data.cityofnewyork.us/Housing-Development/DOB-Permit-Issuance/ipu4-2q9a
- Difficulty: ⭐⭐ (Medium)
- Data: NYC Department of Buildings permits
- Selectors: `.dataset-item`, `.table-responsive`

**5. Austin Building Permits**
- URL: https://data.austintexas.gov/Building-and-Development/Issued-Construction-Permits/3syk-w9eu
- Difficulty: ⭐⭐ (Medium)
- Data: Texas construction permits
- Good for testing date parsing

**6. Los Angeles Building Permits**
- URL: https://data.lacity.org/City-Infrastructure-Service-Requests/Building-and-Safety-Permit-Information-Old/yv23-pmwf
- Difficulty: ⭐⭐⭐ (Hard - complex filtering)
- Data: LA building permits with detailed info

**7. MyBuildingPermit (Multi-jurisdiction)**
- URL: https://permitsearch.mybuildingpermit.com/
- Difficulty: ⭐⭐⭐⭐ (Very Hard - dynamic forms)
- Data: Multiple city permit searches
- Note: Requires jurisdiction selection first

---

## 📊 Construction Project Databases

**8. BuildZoom**
- URL: https://www.buildzoom.com/contractor-search
- Difficulty: ⭐⭐⭐ (Hard - heavy JavaScript)
- Data: Contractor projects, permits, reviews
- Note: Test pattern for contractor directories

**9. Shovels.ai Permit Database**
- URL: https://www.shovels.ai/permit-database
- Difficulty: ⭐⭐⭐⭐ (Very Hard - requires auth/API)
- Data: 150M+ building permits nationwide
- Note: May require API access, good reference for data structure

**10. Dodge Construction Network**
- URL: https://www.construction.com
- Difficulty: ⭐⭐⭐⭐⭐ (Expert - paywall, complex auth)
- Data: Commercial construction project leads
- Note: Industry standard, reference only unless you have access

---

## 💰 Material Pricing & Suppliers

### Price Tracking Sites

**11. Procore Material Price Tracker**
- URL: https://www.procore.com/library/material-price-tracker
- Difficulty: ⭐ (Easy - well-structured)
- Data: Lumber, metal, cement, roofing prices by region
- Selectors: `.price-card`, `.material-price`, `.price-trend`
- **Perfect starter site - clean structure**

**12. Home Depot Building Materials**
- URL: https://www.homedepot.com/b/Building-Materials/N-5yc1vZas6p
- Difficulty: ⭐⭐⭐ (Hard - dynamic pricing, anti-bot)
- Data: Retail building material prices
- Selectors: `.price`, `.product-pod`, `.product__description`

**13. Lowe's Pro**
- URL: https://www.lowes.com/pl/Building-supplies/4294515390
- Difficulty: ⭐⭐⭐ (Hard - similar to Home Depot)
- Data: Building supplies with bulk pricing
- Note: Test bulk pricing pattern extraction

### Specialty Suppliers

**14. Builders FirstSource**
- URL: https://www.bldr.com
- Difficulty: ⭐⭐⭐ (Hard - regional pricing)
- Data: Structural building products
- Note: May require location/account

**15. Deslauriers Construction Materials**
- URL: https://deslinc.com
- Difficulty: ⭐⭐ (Medium - ecommerce)
- Data: Concrete construction materials
- Selectors: `.product-item`, `.price`, `.availability`

**16. Outpost Construction Supply**
- URL: https://www.outpostcs.com/categories/bulk-buy-discounts
- Difficulty: ⭐⭐ (Medium)
- Data: Bulk construction materials with pallet pricing
- Good for testing bulk/unit price extraction

**17. Master Wholesale**
- URL: https://www.masterwholesale.com/construction-materials.html
- Difficulty: ⭐⭐ (Medium)
- Data: Tile, waterproofing, cement products
- Test brand/manufacturer extraction

---

## 👷 Contractor Directories

**18. BuildZoom Contractor Search**
- URL: https://www.buildzoom.com/contractor-search
- Difficulty: ⭐⭐⭐ (Hard)
- Data: Licensed contractors, reviews, project history
- Selectors: `.contractor-card`, `.license-number`, `.rating`

**19. Angi (formerly Angie's List)**
- URL: https://www.angi.com/near-me/contractors/
- Difficulty: ⭐⭐⭐⭐ (Very Hard - heavy JavaScript)
- Data: Contractor profiles, ratings, service areas
- Note: Good for testing review extraction

**20. Better Business Bureau - Contractors**
- URL: https://www.bbb.org/search?find_country=USA&find_text=construction+contractors
- Difficulty: ⭐⭐⭐ (Hard)
- Data: Business ratings, complaints, contact info
- Test accreditation status extraction

---

## 🏢 Real Estate & Development

**21. LoopNet (Commercial Real Estate)**
- URL: https://www.loopnet.com/search/
- Difficulty: ⭐⭐⭐⭐ (Very Hard - paywall for details)
- Data: Commercial property listings, development projects
- Note: Reference for construction project sourcing

**22. CoStar (Commercial Data)**
- URL: https://www.costar.com
- Difficulty: ⭐⭐⭐⭐⭐ (Expert - subscription required)
- Data: Commercial real estate and construction data
- Note: Industry standard, reference only

---

## 📈 Industry News & Reports

**23. Construction Dive**
- URL: https://www.constructiondive.com/
- Difficulty: ⭐⭐ (Medium)
- Data: Construction industry news
- Selectors: `.article-title`, `.article-summary`, `.byline`
- Good for testing article/content extraction

**24. ENR (Engineering News-Record)**
- URL: https://www.enr.com/
- Difficulty: ⭐⭐⭐ (Hard - paywall)
- Data: Construction industry rankings, news
- Note: Test paywall detection

---

## 🧪 Testing Strategy by Difficulty

### Phase 1: Easy Sites (Learn Patterns) ⭐
Start here to validate your scraper works:
1. **Procore Material Price Tracker** - Clean, structured data
2. **Census Building Permits** - Government data, well-formatted
3. **Deslauriers** - Simple ecommerce structure

### Phase 2: Medium Sites (Pattern Adaptation) ⭐⭐
Test selector variations and dynamic content:
4. **NYC Building Permits** - Government portal
5. **Outpost Construction Supply** - Bulk pricing
6. **Construction Dive** - News/article extraction

### Phase 3: Hard Sites (Advanced Features) ⭐⭐⭐
Require wait strategies, JavaScript handling:
7. **BuildZoom** - Heavy JavaScript
8. **Home Depot** - Anti-bot measures
9. **Austin Building Permits** - Complex filtering

### Phase 4: Expert Sites (Production Readiness) ⭐⭐⭐⭐⭐
Ultimate tests for production deployment:
10. **MyBuildingPermit** - Multi-step forms
11. **Dodge Construction** - Paywall handling
12. **CoStar** - Enterprise-level anti-scraping

---

## 🎯 Recommended Testing Order

### For Provizual Demo (Show Working Patterns):

**Test Site #1: Procore Material Price Tracker** ⭐
```python
config = ScraperConfig(
    url="https://www.procore.com/library/material-price-tracker",
    selectors={
        "material_name": "h3.material-title, .product-name",
        "price": ".price-value, .current-price",
        "unit": ".price-unit, .uom",
        "region": ".region-name, .location",
        "trend": ".price-trend, .change-indicator"
    },
    screenshot=True
)
```
**Why**: Clean structure, public data, demonstrates successful pattern

**Test Site #2: Census Building Permits** ⭐⭐
```python
config = ScraperConfig(
    url="https://www.census.gov/construction/bps/",
    selectors={
        "permit_count": ".data-value, .statistic",
        "region": ".region-label, .geography",
        "date": ".period, .reporting-date",
        "category": ".permit-type, .construction-category"
    },
    wait_for=".data-loaded"
)
```
**Why**: Government data, tests wait strategies, demonstrates reliability

**Test Site #3: NYC Building Permits** ⭐⭐
```python
config = ScraperConfig(
    url="https://data.cityofnewyork.us/Housing-Development/DOB-Permit-Issuance/ipu4-2q9a",
    selectors={
        "permit_number": ".permit-id, td:nth-child(1)",
        "address": ".address, td:nth-child(3)",
        "work_type": ".work-type, td:nth-child(4)",
        "issue_date": ".issue-date, td:nth-child(5)"
    }
)
```
**Why**: Real city data, shows municipal portal pattern

---

## 🔧 Testing Best Practices

### Before Testing Each Site:

1. **Manual Inspection**: Open site in browser, inspect elements
2. **Identify Patterns**: Note CSS classes, data attributes, structure
3. **Check robots.txt**: Respect site's crawling preferences
4. **Test Selectors**: Use browser console to validate selectors
5. **Start Minimal**: Begin with 2-3 fields, expand gradually

### During Testing:

```python
# Example test workflow
async def test_site(url, selectors):
    scraper = ConstructionScraper()
    
    # Step 1: Validate selectors exist
    validation = await scraper.validate_selectors(url, selectors)
    print(f"Validation: {validation}")
    
    # Step 2: Test extraction
    config = ScraperConfig(url=url, selectors=selectors, screenshot=True)
    result = await scraper.scrape_pattern(config)
    
    # Step 3: Review results
    print(f"Success: {result.success}")
    print(f"Data: {json.dumps(result.data, indent=2)}")
    print(f"Errors: {result.errors}")
    
    await scraper.cleanup()
```

### What to Test For:

- ✅ **Selector accuracy**: Do selectors find correct elements?
- ✅ **Data completeness**: Are all expected fields extracted?
- ✅ **Error handling**: Graceful failures for missing elements?
- ✅ **Dynamic content**: Wait strategies work for JavaScript sites?
- ✅ **Rate limiting**: Respectful delays between requests?

---

## 📊 Expected Results Template

Document your tests in this format:

```markdown
### Test: [Site Name]
**URL**: [URL]
**Date**: [Test Date]
**Difficulty**: ⭐⭐⭐

**Selectors Tested**:
- field_1: `.selector-1`
- field_2: `.selector-2`

**Results**:
✅ Successfully extracted: field_1, field_2
⚠️ Partial extraction: field_3 (selector needs adjustment)
❌ Failed: field_4 (element not found)

**Notes**:
- Site uses heavy JavaScript, needed `wait_for` parameter
- Price format requires parsing (e.g., "$1,234.56" → 1234.56)
- Pagination detected at bottom of page

**Recommendations**:
- Add fallback selector for field_3: `.alternate-class`
- Implement price parsing function
- Add pagination support for full extraction
```

---

## 🚦 Red Flags to Watch For

**Legal/Ethical**:
- ❌ Login/paywall required (don't scrape private data)
- ❌ robots.txt disallows scraping
- ❌ Terms of service prohibit automated access

**Technical**:
- ⚠️ Aggressive rate limiting (adjust delays)
- ⚠️ CAPTCHA challenges (may need human intervention)
- ⚠️ Cloudflare protection (advanced anti-bot)

**Data Quality**:
- ⚠️ Inconsistent HTML structure across pages
- ⚠️ Missing data in source (can't extract what isn't there)
- ⚠️ JavaScript-rendered content (ensure proper wait)

---

## 💡 Pro Tips for Provizual Demo

**For your demo email, test these 3 sites and include results:**

1. **Procore Material Prices** (show success)
2. **NYC Building Permits** (show adaptation)
3. **Home Depot** (show error handling + fallback)

This demonstrates:
- ✅ Pattern works on clean sites
- ✅ Can adapt to different structures
- ✅ Handles complex sites with grace
- ✅ Production-ready error handling

**Screenshot Strategy**:
- Include screenshot showing successful extraction
- Show side-by-side: Original site vs Extracted data
- Demonstrates validation capability

---

## 🎯 Quick Start Command

Test the easiest site first:

```bash
cd provizual-scraper-demo
source venv/bin/activate
python examples.py
```

Or test specific site:

```python
from server import ConstructionScraper, ScraperConfig
import asyncio

async def quick_test():
    scraper = ConstructionScraper()
    config = ScraperConfig(
        url="https://www.procore.com/library/material-price-tracker",
        selectors={
            "material": "h3",
            "price": ".price"
        },
        screenshot=True
    )
    result = await scraper.scrape_pattern(config)
    print(result.data)
    await scraper.cleanup()

asyncio.run(quick_test())
```

---

**Remember**: The goal isn't to scrape every site perfectly. It's to demonstrate:
1. ✅ Pattern-based approach works
2. ✅ You can adapt selectors when sites change
3. ✅ Error handling is production-ready
4. ✅ You understand construction industry data

**For Provizual**: Focus on 3-5 well-documented test cases that show your methodology, not 50 half-tested sites.
