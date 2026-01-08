#!/bin/bash
# Construction Scraper - Setup Script
# Automated installation and configuration

set -e

echo "🏗️  Construction Data Scraper - Setup"
echo "======================================"
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "📋 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    echo "Please install Python 3.9 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✓ Found Python $PYTHON_VERSION${NC}"

# Create virtual environment
echo ""
echo "🔧 Creating virtual environment..."
if [ -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment already exists${NC}"
    read -p "Do you want to recreate it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3 -m venv venv
    fi
else
    python3 -m venv venv
fi
echo -e "${GREEN}✓ Virtual environment ready${NC}"

# Activate virtual environment
echo ""
echo "⚡ Activating virtual environment..."
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✓ Python dependencies installed${NC}"

# Install Playwright browsers
echo ""
echo "🌐 Installing Playwright browsers..."
playwright install chromium
echo -e "${GREEN}✓ Playwright browsers installed${NC}"

# Create necessary directories
echo ""
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p screenshots
mkdir -p exports
echo -e "${GREEN}✓ Directories created${NC}"

# Check for environment variables
echo ""
echo "🔐 Checking environment configuration..."
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cat > .env << 'EOF'
# Construction Scraper Configuration

# Optional: Anthropic API key for AI-powered extraction
ANTHROPIC_API_KEY=

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/scraper.log

# Scraper Settings
DEFAULT_TIMEOUT=30000
MAX_RETRIES=3
RATE_LIMIT_DELAY=2

# Screenshot Settings
SCREENSHOT_DIR=screenshots
SCREENSHOT_ENABLED=false

# Export Settings
EXPORT_DIR=exports
EOF
    echo -e "${GREEN}✓ .env file created${NC}"
    echo -e "${YELLOW}⚠️  Please edit .env to add your API keys if needed${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

# Test installation
echo ""
echo "🧪 Testing installation..."
python3 -c "
import sys
try:
    from playwright.async_api import async_playwright
    from mcp.server import Server
    from pydantic import BaseModel
    print('✓ All core dependencies imported successfully')
    sys.exit(0)
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Installation test passed${NC}"
else
    echo -e "${RED}❌ Installation test failed${NC}"
    exit 1
fi

# Instructions for Claude Desktop
echo ""
echo "📝 Setup complete! Next steps:"
echo ""
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Run the GUI application:"
echo "   python gui.py"
echo ""
echo "3. Or run the MCP server:"
echo "   python server.py"
echo ""
echo "4. To integrate with Claude Desktop:"
echo "   - Open: ~/Library/Application Support/Claude/claude_desktop_config.json"
echo "   - Add the configuration from: claude_desktop_config.json"
echo "   - Update the path to point to this directory"
echo "   - Restart Claude Desktop"
echo ""
echo "5. Try the examples:"
echo "   python examples.py"
echo ""
echo -e "${GREEN}Happy scraping! 🏗️${NC}"
