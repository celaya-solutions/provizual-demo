#----------------------------------------------------------------------------
#File: server.py
#Project: provizual-demo
#Created by: Celaya Solutions, 2025
#Author: Christopher Celaya <chris@chriscelaya.com>
#Description: MCP Server for pattern-based web scraping with Playwright and LLM integration
#Version: 1.0.0
#License: MIT
#Last Update: January 2026
#----------------------------------------------------------------------------

#!/usr/bin/env python3
"""
Construction Data Scraper MCP Server
Demonstrates pattern-based web scraping for construction industry data
Built for Provizual-style workflows with Playwright + LLM integration
"""

import asyncio
import json
import logging
from typing import Any, Optional
from datetime import datetime

from mcp.server import Server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
from pydantic import BaseModel, Field
from playwright.async_api import async_playwright, Browser, Page

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("construction-scraper")

# Initialize MCP Server
app = Server("construction-scraper")


class ScraperConfig(BaseModel):
    """Configuration for a scraping pattern"""
    url: str = Field(description="Target URL to scrape")
    selectors: dict[str, str] = Field(
        description="CSS selectors for data extraction",
        default_factory=dict
    )
    wait_for: Optional[str] = Field(
        default=None,
        description="Selector to wait for before extraction"
    )
    screenshot: bool = Field(
        default=False,
        description="Capture screenshot for validation"
    )
    timeout: int = Field(
        default=30000,
        description="Page load timeout in milliseconds"
    )


class ScraperResult(BaseModel):
    """Structured result from scraping operation"""
    success: bool
    data: dict[str, Any]
    screenshot_path: Optional[str] = None
    errors: list[str] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    metadata: dict[str, Any] = Field(default_factory=dict)


class ConstructionScraper:
    """
    Pattern-based web scraper for construction industry sites.
    Demonstrates Provizual's core scraping workflow needs.
    """
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.playwright = None
        
    async def initialize(self):
        """Initialize Playwright browser"""
        if not self.playwright:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=True,
                args=['--disable-blink-features=AutomationControlled']
            )
            logger.info("Browser initialized")
    
    async def cleanup(self):
        """Cleanup browser resources"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
            
    async def scrape_pattern(self, config: ScraperConfig) -> ScraperResult:
        """
        Execute scraping pattern based on configuration.
        This mimics the 'copy and adapt existing patterns' workflow.
        """
        await self.initialize()
        errors = []
        data = {}
        screenshot_path = None
        
        try:
            page = await self.browser.new_page()
            
            # Set viewport and user agent
            await page.set_viewport_size({"width": 1920, "height": 1080})
            await page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            
            logger.info(f"Navigating to {config.url}")
            response = await page.goto(
                config.url,
                wait_until="domcontentloaded",
                timeout=config.timeout
            )
            
            if response and response.status >= 400:
                errors.append(f"HTTP {response.status}: {response.status_text}")
            
            # Wait for dynamic content if specified
            if config.wait_for:
                try:
                    await page.wait_for_selector(
                        config.wait_for,
                        timeout=config.timeout,
                        state="visible"
                    )
                except Exception as e:
                    errors.append(f"Wait failed: {str(e)}")
            
            # Extract data using configured selectors
            for key, selector in config.selectors.items():
                try:
                    elements = await page.query_selector_all(selector)
                    if len(elements) == 1:
                        # Single element - extract text or attribute
                        text = await elements[0].text_content()
                        data[key] = text.strip() if text else None
                    elif len(elements) > 1:
                        # Multiple elements - extract as list
                        texts = []
                        for elem in elements:
                            text = await elem.text_content()
                            if text:
                                texts.append(text.strip())
                        data[key] = texts
                    else:
                        data[key] = None
                        errors.append(f"Selector '{selector}' found no elements")
                except Exception as e:
                    errors.append(f"Failed to extract '{key}': {str(e)}")
                    data[key] = None
            
            # Capture screenshot if requested
            if config.screenshot:
                screenshot_path = f"/tmp/screenshot_{datetime.now().timestamp()}.png"
                await page.screenshot(path=screenshot_path, full_page=True)
                logger.info(f"Screenshot saved: {screenshot_path}")
            
            # Collect metadata
            metadata = {
                "url": config.url,
                "title": await page.title(),
                "response_status": response.status if response else None,
                "selectors_used": list(config.selectors.keys()),
            }
            
            await page.close()
            
            return ScraperResult(
                success=len(errors) == 0,
                data=data,
                screenshot_path=screenshot_path,
                errors=errors,
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"Scraping failed: {str(e)}")
            return ScraperResult(
                success=False,
                data={},
                errors=[str(e)]
            )


# Global scraper instance
scraper = ConstructionScraper()


@app.list_resources()
async def list_resources() -> list[Resource]:
    """List available scraping patterns and templates"""
    return [
        Resource(
            uri="pattern://construction-project",
            name="Construction Project Pattern",
            mimeType="application/json",
            description="Pattern for scraping construction project listings"
        ),
        Resource(
            uri="pattern://material-pricing",
            name="Material Pricing Pattern",
            mimeType="application/json",
            description="Pattern for scraping building material prices"
        ),
        Resource(
            uri="pattern://contractor-info",
            name="Contractor Information Pattern",
            mimeType="application/json",
            description="Pattern for scraping contractor/supplier data"
        ),
    ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    """Return scraping pattern templates"""
    patterns = {
        "pattern://construction-project": {
            "description": "Extract construction project data",
            "selectors": {
                "project_name": ".project-title, h1.title",
                "project_type": ".project-type, .category",
                "location": ".location, .address",
                "budget": ".budget, .cost",
                "status": ".status, .project-status",
                "contractor": ".contractor, .gc-name",
                "completion_date": ".completion, .end-date"
            },
            "wait_for": ".project-details",
            "example_urls": [
                "https://www.construction.com/projects",
                "https://www.dodge.construction/projects"
            ]
        },
        "pattern://material-pricing": {
            "description": "Extract building material pricing data",
            "selectors": {
                "material_name": ".product-name, h2.title",
                "price": ".price, .cost",
                "unit": ".unit, .uom",
                "supplier": ".supplier, .vendor",
                "availability": ".stock, .availability",
                "last_updated": ".updated, .date"
            },
            "wait_for": ".pricing-table",
        },
        "pattern://contractor-info": {
            "description": "Extract contractor/supplier information",
            "selectors": {
                "company_name": ".company-name, h1",
                "contact_email": "a[href^='mailto:']",
                "phone": ".phone, .contact-number",
                "address": ".address, .location",
                "specialties": ".specialty, .services",
                "certifications": ".certification, .license"
            },
        }
    }
    
    pattern = patterns.get(uri, {"error": "Pattern not found"})
    return json.dumps(pattern, indent=2)


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available scraping tools"""
    return [
        Tool(
            name="scrape_with_pattern",
            description="""
            Execute web scraping using a defined pattern.
            This tool demonstrates the core Provizual workflow:
            - Copy existing selector patterns
            - Adapt to new data sources
            - Validate scraped results
            - Handle common failure modes
            
            Returns structured data ready for database insertion.
            """,
            inputSchema={
                "type": "object",
                "required": ["url", "selectors"],
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Target URL to scrape"
                    },
                    "selectors": {
                        "type": "object",
                        "description": "CSS selectors mapping field names to selectors",
                        "additionalProperties": {"type": "string"}
                    },
                    "wait_for": {
                        "type": "string",
                        "description": "Optional selector to wait for before extraction"
                    },
                    "screenshot": {
                        "type": "boolean",
                        "description": "Capture screenshot for validation",
                        "default": False
                    }
                }
            }
        ),
        Tool(
            name="validate_scraper",
            description="""
            Test a scraper pattern against a URL without full extraction.
            Useful for debugging selector changes and site updates.
            Returns what elements would be found by each selector.
            """,
            inputSchema={
                "type": "object",
                "required": ["url", "selectors"],
                "properties": {
                    "url": {"type": "string"},
                    "selectors": {
                        "type": "object",
                        "additionalProperties": {"type": "string"}
                    }
                }
            }
        ),
        Tool(
            name="extract_with_ai",
            description="""
            Use LLM to intelligently extract data when selectors fail.
            Fallback strategy for dynamic sites or structural changes.
            Analyzes page content and extracts requested fields semantically.
            """,
            inputSchema={
                "type": "object",
                "required": ["url", "fields"],
                "properties": {
                    "url": {"type": "string"},
                    "fields": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of fields to extract (e.g., ['price', 'title'])"
                    }
                }
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent | ImageContent | EmbeddedResource]:
    """Execute scraping tools"""
    
    if name == "scrape_with_pattern":
        config = ScraperConfig(**arguments)
        result = await scraper.scrape_pattern(config)
        
        response_parts = [
            TextContent(
                type="text",
                text=f"""
# Scraping Result

**Status:** {'✓ Success' if result.success else '✗ Failed'}
**URL:** {config.url}
**Timestamp:** {result.timestamp}

## Extracted Data
```json
{json.dumps(result.data, indent=2)}
```

## Metadata
```json
{json.dumps(result.metadata, indent=2)}
```
""" + (f"\n## Errors\n" + "\n".join(f"- {e}" for e in result.errors) if result.errors else "")
            )
        ]
        
        return response_parts
        
    elif name == "validate_scraper":
        await scraper.initialize()
        page = await scraper.browser.new_page()
        
        try:
            await page.goto(arguments["url"], wait_until="domcontentloaded")
            validation_results = {}
            
            for key, selector in arguments["selectors"].items():
                elements = await page.query_selector_all(selector)
                validation_results[key] = {
                    "selector": selector,
                    "found_count": len(elements),
                    "status": "✓ Found" if elements else "✗ Not Found"
                }
            
            await page.close()
            
            return [TextContent(
                type="text",
                text=f"""
# Selector Validation

**URL:** {arguments['url']}

## Results
```json
{json.dumps(validation_results, indent=2)}
```
"""
            )]
            
        except Exception as e:
            return [TextContent(type="text", text=f"Validation failed: {str(e)}")]
            
    elif name == "extract_with_ai":
        return [TextContent(
            type="text",
            text="""
# AI-Powered Extraction

This tool would integrate with an LLM to semantically extract data
when traditional selectors fail. Implementation would:

1. Fetch page HTML/content
2. Send to LLM with extraction prompt
3. Parse structured response
4. Validate against expected fields

For production, integrate with Claude API or local model.
"""
        )]
    
    return [TextContent(type="text", text="Unknown tool")]


async def main():
    """Run the MCP server"""
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        logger.info("Construction Scraper MCP Server starting...")
        try:
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
        finally:
            await scraper.cleanup()
            logger.info("Server shutdown complete")


if __name__ == "__main__":
    asyncio.run(main())
