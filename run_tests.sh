#!/bin/bash
# Test runner script for Notch Chatbot

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}Error: .env file not found${NC}"
    echo "Please create a .env file with OPENAI_API_KEY=your-key"
    exit 1
fi

# Function to run tests
run_test_category() {
    local category=$1
    local path=$2

    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}Running ${category} Tests${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

    for test_file in tests/${path}/*.py; do
        if [ -f "$test_file" ]; then
            echo -e "${YELLOW}Running: ${test_file}${NC}"
            if uv run python "$test_file"; then
                echo -e "${GREEN}✓ Passed${NC}\n"
            else
                echo -e "${RED}✗ Failed${NC}\n"
                return 1
            fi
        fi
    done
}

# Print header
echo -e "${GREEN}"
echo "╔════════════════════════════════════════╗"
echo "║     Notch Chatbot Test Suite          ║"
echo "╚════════════════════════════════════════╝"
echo -e "${NC}"

# Parse command line arguments
CATEGORY=${1:-all}

case $CATEGORY in
    unit)
        run_test_category "Unit" "unit"
        ;;
    integration)
        run_test_category "Integration" "integration"
        ;;
    demo)
        run_test_category "Demo" "demo"
        ;;
    all)
        run_test_category "Unit" "unit" && \
        run_test_category "Integration" "integration" && \
        run_test_category "Demo" "demo"
        ;;
    *)
        echo -e "${RED}Unknown test category: $CATEGORY${NC}"
        echo "Usage: ./run_tests.sh [unit|integration|demo|all]"
        exit 1
        ;;
esac

# Print summary
if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}✓ All tests passed!${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
else
    echo -e "\n${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${RED}✗ Some tests failed${NC}"
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
    exit 1
fi
