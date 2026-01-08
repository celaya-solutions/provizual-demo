#----------------------------------------------------------------------------
#File: gui.py
#Project: provizual-demo
#Created by: Celaya Solutions, 2025
#Author: Christopher Celaya <chris@chriscelaya.com>
#Description: PyQt6 GUI for construction data scraping and pattern management
#Version: 1.0.0
#License: MIT
#Last Update: January 2026
#----------------------------------------------------------------------------

#!/usr/bin/env python3
"""
Construction Scraper GUI
Simple interface for running scraping patterns
"""

import sys
import json
import asyncio
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox,
    QCheckBox, QGroupBox, QFileDialog, QMessageBox, QTabWidget
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QTextCursor

# Import our scraper
import sys
sys.path.append(str(Path(__file__).parent))
from server import ConstructionScraper, ScraperConfig, ScraperResult


class ScraperThread(QThread):
    """Background thread for scraping operations"""
    finished = pyqtSignal(object)
    error = pyqtSignal(str)
    
    def __init__(self, config: ScraperConfig):
        super().__init__()
        self.config = config
        
    def run(self):
        """Execute scraping in background"""
        try:
            # Create new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            scraper = ConstructionScraper()
            result = loop.run_until_complete(scraper.scrape_pattern(self.config))
            loop.run_until_complete(scraper.cleanup())
            
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class ConstructionScraperGUI(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Construction Data Scraper")
        self.setMinimumSize(1000, 700)
        
        # State
        self.current_thread = None
        self.selector_inputs = {}
        
        self._init_ui()
        
    def _init_ui(self):
        """Initialize user interface"""
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Header
        header = QLabel("Construction Industry Web Scraper")
        header_font = QFont()
        header_font.setPointSize(16)
        header_font.setBold(True)
        header.setFont(header_font)
        layout.addWidget(header)
        
        # Tabs
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # Tab 1: Scraper
        scraper_tab = self._create_scraper_tab()
        tabs.addTab(scraper_tab, "Scraper")
        
        # Tab 2: Patterns
        patterns_tab = self._create_patterns_tab()
        tabs.addTab(patterns_tab, "Pattern Library")
        
        # Tab 3: Results History
        history_tab = self._create_history_tab()
        tabs.addTab(history_tab, "History")
        
    def _create_scraper_tab(self):
        """Create main scraper interface"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # URL Input
        url_group = QGroupBox("Target Configuration")
        url_layout = QVBoxLayout()
        
        url_row = QHBoxLayout()
        url_row.addWidget(QLabel("URL:"))
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://example.com/construction-data")
        url_row.addWidget(self.url_input)
        url_layout.addLayout(url_row)
        
        wait_row = QHBoxLayout()
        wait_row.addWidget(QLabel("Wait For Selector:"))
        self.wait_input = QLineEdit()
        self.wait_input.setPlaceholderText(".content-loaded (optional)")
        wait_row.addWidget(self.wait_input)
        url_layout.addLayout(wait_row)
        
        url_group.setLayout(url_layout)
        layout.addWidget(url_group)
        
        # Selectors
        selector_group = QGroupBox("Data Selectors")
        selector_layout = QVBoxLayout()
        
        # Add common selectors
        for field in ["project_name", "location", "price", "status", "contractor"]:
            row = QHBoxLayout()
            row.addWidget(QLabel(f"{field}:"))
            input_field = QLineEdit()
            input_field.setPlaceholderText(f".{field}, #{field}")
            self.selector_inputs[field] = input_field
            row.addWidget(input_field)
            selector_layout.addLayout(row)
        
        # Add custom selector button
        add_btn = QPushButton("+ Add Custom Selector")
        add_btn.clicked.connect(self._add_custom_selector)
        selector_layout.addWidget(add_btn)
        
        selector_group.setLayout(selector_layout)
        layout.addWidget(selector_group)
        
        # Options
        options_layout = QHBoxLayout()
        self.screenshot_check = QCheckBox("Capture Screenshot")
        options_layout.addWidget(self.screenshot_check)
        options_layout.addStretch()
        layout.addLayout(options_layout)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.validate_btn = QPushButton("Validate Selectors")
        self.validate_btn.clicked.connect(self._validate_selectors)
        button_layout.addWidget(self.validate_btn)
        
        self.scrape_btn = QPushButton("Scrape Data")
        self.scrape_btn.clicked.connect(self._start_scraping)
        self.scrape_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        button_layout.addWidget(self.scrape_btn)
        
        layout.addLayout(button_layout)
        
        # Results
        results_group = QGroupBox("Results")
        results_layout = QVBoxLayout()
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMinimumHeight(200)
        results_layout.addWidget(self.results_text)
        
        export_layout = QHBoxLayout()
        export_json_btn = QPushButton("Export as JSON")
        export_json_btn.clicked.connect(lambda: self._export_results("json"))
        export_layout.addWidget(export_json_btn)
        
        export_csv_btn = QPushButton("Export as CSV")
        export_csv_btn.clicked.connect(lambda: self._export_results("csv"))
        export_layout.addWidget(export_csv_btn)
        
        export_layout.addStretch()
        results_layout.addLayout(export_layout)
        
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)
        
        return widget
    
    def _create_patterns_tab(self):
        """Create pattern library interface"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        layout.addWidget(QLabel("Pre-built Scraping Patterns"))
        
        patterns = {
            "Construction Projects": {
                "project_name": ".project-title, h1.title",
                "location": ".location, .address",
                "budget": ".budget, .cost",
                "status": ".status"
            },
            "Material Pricing": {
                "material_name": ".product-name",
                "price": ".price",
                "supplier": ".supplier",
                "availability": ".stock"
            },
            "Contractor Directory": {
                "company_name": ".company-name, h1",
                "contact_email": "a[href^='mailto:']",
                "phone": ".phone",
                "specialties": ".specialty"
            }
        }
        
        for name, selectors in patterns.items():
            btn = QPushButton(f"Load: {name}")
            btn.clicked.connect(lambda checked, s=selectors: self._load_pattern(s))
            layout.addWidget(btn)
        
        layout.addStretch()
        return widget
    
    def _create_history_tab(self):
        """Create results history interface"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        layout.addWidget(QLabel("Recent Scraping Results"))
        
        self.history_text = QTextEdit()
        self.history_text.setReadOnly(True)
        layout.addWidget(self.history_text)
        
        return widget
    
    def _add_custom_selector(self):
        """Add a custom selector field"""
        # This would dynamically add a new row
        pass
    
    def _load_pattern(self, selectors: dict):
        """Load a predefined pattern"""
        for field, selector in selectors.items():
            if field in self.selector_inputs:
                self.selector_inputs[field].setText(selector)
        
        QMessageBox.information(self, "Pattern Loaded", "Pattern selectors loaded successfully!")
    
    def _validate_selectors(self):
        """Validate selectors without full scraping"""
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a URL")
            return
        
        self.results_text.append("\n--- Validating Selectors ---")
        self.results_text.append("This feature would test each selector...")
        self.results_text.append("✓ Implementation in production version\n")
    
    def _start_scraping(self):
        """Start scraping operation"""
        # Validate inputs
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a URL")
            return
        
        # Build selectors dict
        selectors = {}
        for field, input_widget in self.selector_inputs.items():
            selector = input_widget.text().strip()
            if selector:
                selectors[field] = selector
        
        if not selectors:
            QMessageBox.warning(self, "Error", "Please enter at least one selector")
            return
        
        # Create config
        config = ScraperConfig(
            url=url,
            selectors=selectors,
            wait_for=self.wait_input.text().strip() or None,
            screenshot=self.screenshot_check.isChecked()
        )
        
        # Disable buttons
        self.scrape_btn.setEnabled(False)
        self.validate_btn.setEnabled(False)
        
        # Clear results
        self.results_text.clear()
        self.results_text.append("🔄 Scraping in progress...\n")
        
        # Start background thread
        self.current_thread = ScraperThread(config)
        self.current_thread.finished.connect(self._scraping_finished)
        self.current_thread.error.connect(self._scraping_error)
        self.current_thread.start()
    
    def _scraping_finished(self, result: ScraperResult):
        """Handle scraping completion"""
        self.scrape_btn.setEnabled(True)
        self.validate_btn.setEnabled(True)
        
        # Display results
        self.results_text.clear()
        
        if result.success:
            self.results_text.append("✅ Scraping Successful!\n")
        else:
            self.results_text.append("⚠️ Scraping completed with errors\n")
        
        self.results_text.append(f"Timestamp: {result.timestamp}")
        self.results_text.append(f"\n--- Extracted Data ---")
        self.results_text.append(json.dumps(result.data, indent=2))
        
        if result.errors:
            self.results_text.append(f"\n--- Errors ---")
            for error in result.errors:
                self.results_text.append(f"❌ {error}")
        
        if result.screenshot_path:
            self.results_text.append(f"\n📸 Screenshot: {result.screenshot_path}")
        
        # Store for export
        self.last_result = result
    
    def _scraping_error(self, error: str):
        """Handle scraping error"""
        self.scrape_btn.setEnabled(True)
        self.validate_btn.setEnabled(True)
        
        QMessageBox.critical(self, "Scraping Error", f"Failed to scrape data:\n{error}")
        self.results_text.append(f"\n❌ Error: {error}")
    
    def _export_results(self, format_type: str):
        """Export results to file"""
        if not hasattr(self, 'last_result'):
            QMessageBox.warning(self, "No Data", "No scraping results to export")
            return
        
        file_filter = "JSON files (*.json)" if format_type == "json" else "CSV files (*.csv)"
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Results",
            f"scrape_results.{format_type}",
            file_filter
        )
        
        if filename:
            try:
                if format_type == "json":
                    with open(filename, 'w') as f:
                        json.dump(self.last_result.data, f, indent=2)
                else:
                    # Simple CSV export
                    import csv
                    with open(filename, 'w', newline='') as f:
                        if self.last_result.data:
                            writer = csv.DictWriter(f, fieldnames=self.last_result.data.keys())
                            writer.writeheader()
                            writer.writerow(self.last_result.data)
                
                QMessageBox.information(self, "Success", f"Results exported to:\n{filename}")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Failed to export:\n{str(e)}")


def main():
    """Run the GUI application"""
    app = QApplication(sys.argv)
    window = ConstructionScraperGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
