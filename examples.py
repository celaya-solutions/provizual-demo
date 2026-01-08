#----------------------------------------------------------------------------
#File: examples.py
#Project: provizual-demo
#Created by: Celaya Solutions, 2025
#Author: Christopher Celaya <chris@chriscelaya.com>
#Description: Example usage patterns for construction data extraction and scraping
#Version: 1.0.0
#License: MIT
#Last Update: January 2026
#----------------------------------------------------------------------------

#!/usr/bin/env python3
"""
Construction Scraper Examples
Demonstrates real-world usage patterns for construction data extraction
"""

import asyncio
import json
from server import ConstructionScraper, ScraperConfig


async def example_1_construction_projects():
    """
    Example 1: Scraping construction project listings
    Common use case: Building project database from public listings
    """
    print("\n" + "="*60)
    print("EXAMPLE 1: Construction Project Listings")
    print("="*60)
    
    scraper = ConstructionScraper()
    
    # Example configuration for a typical construction project site
    config = ScraperConfig(
        url="https://example-construction-projects.com",
        selectors={
            "project_name": ".project-title, h1.name, .listing-title",
            "project_type": ".project-type, .category, .classification",
            "location": ".location, .address, .project-location",
            "budget": ".budget, .estimated-cost, .project-value",
            "contractor": ".contractor, .gc-name, .general-contractor",
            "status": ".status, .project-status, .phase",
            "completion_date": ".completion-date, .end-date, .target-date"
        },
        wait_for=".project-listings",  # Wait for dynamic content
        screenshot=True,
        timeout=30000
    )
    
    print("\nConfiguration:")
    print(f"  URL: {config.url}")
    print(f"  Selectors: {len(config.selectors)} fields")
    print(f"  Screenshot: {config.screenshot}")
    
    print("\n⏳ Scraping in progress...")
    result = await scraper.scrape_pattern(config)
    
    if result.success:
        print("✅ Scraping successful!")
        print("\nExtracted Data:")
        print(json.dumps(result.data, indent=2))
    else:
        print("⚠️ Scraping completed with errors:")
        for error in result.errors:
            print(f"  ❌ {error}")
    
    await scraper.cleanup()
    return result


async def example_2_material_pricing():
    """
    Example 2: Tracking building material prices
    Use case: Monitor price changes across multiple suppliers
    """
    print("\n" + "="*60)
    print("EXAMPLE 2: Material Pricing Tracker")
    print("="*60)
    
    scraper = ConstructionScraper()
    
    # Multiple supplier sites to check
    suppliers = [
        {
            "name": "Supplier A",
            "url": "https://supplier-a.com/materials",
            "selectors": {
                "material_name": ".product-name",
                "price": ".price-display",
                "unit": ".unit-measure",
                "availability": ".stock-status"
            }
        },
        {
            "name": "Supplier B", 
            "url": "https://supplier-b.com/catalog",
            "selectors": {
                "material_name": "h2.product",
                "price": ".cost",
                "unit": ".uom",
                "availability": ".in-stock"
            }
        }
    ]
    
    results = []
    
    for supplier in suppliers:
        print(f"\n📊 Checking {supplier['name']}...")
        
        config = ScraperConfig(
            url=supplier["url"],
            selectors=supplier["selectors"],
            screenshot=False
        )
        
        result = await scraper.scrape_pattern(config)
        results.append({
            "supplier": supplier["name"],
            "data": result.data,
            "success": result.success
        })
        
        # Be respectful with rate limiting
        await asyncio.sleep(2)
    
    print("\n📋 Price Comparison Results:")
    print(json.dumps(results, indent=2))
    
    await scraper.cleanup()
    return results


async def example_3_selector_adaptation():
    """
    Example 3: Adapting patterns when selectors change
    Use case: Site updates HTML structure, need to update selectors
    """
    print("\n" + "="*60)
    print("EXAMPLE 3: Pattern Adaptation (Site Structure Change)")
    print("="*60)
    
    scraper = ConstructionScraper()
    
    # Scenario: Site changed from .old-class to .new-class
    print("\n📝 Original Pattern (no longer works):")
    old_config = ScraperConfig(
        url="https://construction-permits.gov",
        selectors={
            "permit_number": ".permit-id",  # Old selector
            "project_address": ".address",   # Old selector
            "issue_date": ".date-issued"     # Old selector
        }
    )
    print(json.dumps(old_config.selectors, indent=2))
    
    print("\n🔄 Adapted Pattern (updated selectors):")
    new_config = ScraperConfig(
        url="https://construction-permits.gov",
        selectors={
            # Use multiple fallback selectors
            "permit_number": ".permit-number, .permit-id, [data-permit]",
            "project_address": ".project-address, .address, .location",
            "issue_date": ".issued-date, .date-issued, .permit-date"
        }
    )
    print(json.dumps(new_config.selectors, indent=2))
    
    print("\n⏳ Testing adapted pattern...")
    result = await scraper.scrape_pattern(new_config)
    
    if result.success:
        print("✅ Adapted pattern works!")
        print(f"   Extracted {len(result.data)} fields successfully")
    else:
        print("⚠️ Some selectors still need adjustment:")
        for error in result.errors:
            print(f"  ❌ {error}")
    
    await scraper.cleanup()
    return result


async def example_4_error_handling():
    """
    Example 4: Robust error handling for production
    Use case: Handle common failure scenarios gracefully
    """
    print("\n" + "="*60)
    print("EXAMPLE 4: Production Error Handling")
    print("="*60)
    
    scraper = ConstructionScraper()
    
    # Test multiple scenarios
    test_cases = [
        {
            "name": "Valid Site",
            "url": "https://example.com",
            "expected": "success"
        },
        {
            "name": "Invalid Selector",
            "url": "https://example.com",
            "selectors": {
                "nonexistent": ".this-class-does-not-exist-xyz123"
            },
            "expected": "partial_failure"
        },
        {
            "name": "Timeout Scenario",
            "url": "https://very-slow-site.example.com",
            "timeout": 5000,  # Short timeout to trigger failure
            "expected": "timeout"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n🧪 Test Case {i}: {test['name']}")
        
        config = ScraperConfig(
            url=test.get("url", "https://example.com"),
            selectors=test.get("selectors", {"title": "h1"}),
            timeout=test.get("timeout", 30000)
        )
        
        try:
            result = await scraper.scrape_pattern(config)
            
            print(f"   Status: {'✅ Success' if result.success else '⚠️ Failed'}")
            print(f"   Errors: {len(result.errors)}")
            print(f"   Data fields: {len(result.data)}")
            
            if result.errors:
                print("   Error details:")
                for error in result.errors[:3]:  # Show first 3 errors
                    print(f"     - {error}")
                    
        except Exception as e:
            print(f"   💥 Exception: {str(e)}")
        
        await asyncio.sleep(1)
    
    await scraper.cleanup()


async def example_5_batch_processing():
    """
    Example 5: Batch processing multiple URLs
    Use case: Daily scraping job for market intelligence
    """
    print("\n" + "="*60)
    print("EXAMPLE 5: Batch Processing (Daily Market Intelligence)")
    print("="*60)
    
    scraper = ConstructionScraper()
    
    # Simulate daily scraping job
    target_sites = [
        "https://permits.city-a.gov/recent",
        "https://permits.city-b.gov/new-permits",
        "https://permits.city-c.gov/applications"
    ]
    
    all_results = []
    
    print(f"\n📅 Processing {len(target_sites)} sites...")
    
    for idx, url in enumerate(target_sites, 1):
        print(f"\n[{idx}/{len(target_sites)}] {url}")
        
        config = ScraperConfig(
            url=url,
            selectors={
                "permit_type": ".type, .permit-type",
                "applicant": ".applicant, .company",
                "value": ".value, .estimated-cost",
                "status": ".status"
            }
        )
        
        result = await scraper.scrape_pattern(config)
        all_results.append({
            "url": url,
            "timestamp": result.timestamp,
            "success": result.success,
            "data": result.data
        })
        
        # Rate limiting between requests
        await asyncio.sleep(3)
    
    print("\n📊 Batch Processing Summary:")
    successful = sum(1 for r in all_results if r["success"])
    print(f"  Total sites processed: {len(all_results)}")
    print(f"  Successful: {successful}")
    print(f"  Failed: {len(all_results) - successful}")
    
    # Save batch results
    output_file = f"/tmp/batch_results_{all_results[0]['timestamp']}.json"
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\n💾 Results saved to: {output_file}")
    
    await scraper.cleanup()
    return all_results


async def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("CONSTRUCTION SCRAPER - USAGE EXAMPLES")
    print("Demonstrating Provizual-style workflows")
    print("="*60)
    
    examples = [
        ("Construction Project Listings", example_1_construction_projects),
        ("Material Pricing Tracker", example_2_material_pricing),
        ("Pattern Adaptation", example_3_selector_adaptation),
        ("Error Handling", example_4_error_handling),
        ("Batch Processing", example_5_batch_processing),
    ]
    
    for name, example_func in examples:
        try:
            await example_func()
        except Exception as e:
            print(f"\n❌ Example '{name}' failed: {str(e)}")
        
        print("\n" + "-"*60)
        await asyncio.sleep(1)
    
    print("\n✅ All examples completed!")
    print("\nNext Steps:")
    print("  1. Review extracted data formats")
    print("  2. Customize selectors for your target sites")
    print("  3. Integrate with your data pipeline")
    print("  4. Set up monitoring and alerting")


if __name__ == "__main__":
    print("\n" + "🏗️ " * 20)
    print("CONSTRUCTION DATA SCRAPER - EXAMPLES")
    print("🏗️ " * 20)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏸️  Examples interrupted by user")
    except Exception as e:
        print(f"\n\n💥 Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
