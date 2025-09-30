#!/bin/bash

# Deployment script for Hugo Personal Blog
# Automates validation, building, and deployment process

set -e  # Exit on any error

echo "🚀 Starting deployment process..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
print_status "Checking prerequisites..."

if ! command -v hugo &> /dev/null; then
    print_error "Hugo is not installed. Please install Hugo Extended >= 0.115"
    exit 1
fi

if ! command -v git &> /dev/null; then
    print_error "Git is not installed. Please install Git"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3"
    exit 1
fi

# Check Hugo version
HUGO_VERSION=$(hugo version | grep -o 'v[0-9]\+\.[0-9]\+\.[0-9]\+' | head -1)
print_success "Hugo version: $HUGO_VERSION"

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    print_error "Not in a git repository"
    exit 1
fi

# Update git submodules
print_status "Updating git submodules..."
git submodule update --init --recursive
print_success "Submodules updated"

# Run content validation
print_status "Running content validation..."
if python3 validate_content.py > /dev/null 2>&1; then
    print_success "Content validation passed"
else
    print_warning "Content validation has warnings (continuing anyway)"
fi

# Run comprehensive tests
print_status "Running comprehensive tests..."
if python3 run_all_tests.py > /dev/null 2>&1; then
    print_success "All tests passed"
else
    print_warning "Some tests failed (check output for details)"
    # Don't exit on test failures, but show warning
fi

# Run SEO performance test
print_status "Running SEO & Performance analysis..."
if python3 seo_performance_test.py > /dev/null 2>&1; then
    print_success "SEO & Performance check passed"
else
    print_warning "SEO & Performance check has issues"
fi

# Clean previous build
print_status "Cleaning previous build..."
if [ -d "public" ]; then
    rm -rf public/*
fi
print_success "Build directory cleaned"

# Build the site
print_status "Building Hugo site..."
START_TIME=$(date +%s)

if hugo --minify --gc; then
    END_TIME=$(date +%s)
    BUILD_TIME=$((END_TIME - START_TIME))
    print_success "Site built successfully in ${BUILD_TIME}s"
else
    print_error "Hugo build failed"
    exit 1
fi

# Verify build output
print_status "Verifying build output..."

if [ ! -f "public/index.html" ]; then
    print_error "Build verification failed: index.html not found"
    exit 1
fi

if [ ! -f "public/sitemap.xml" ]; then
    print_error "Build verification failed: sitemap.xml not found"
    exit 1
fi

if [ ! -f "public/index.json" ]; then
    print_error "Build verification failed: search index not found"
    exit 1
fi

print_success "Build verification passed"

# Calculate build statistics
TOTAL_PAGES=$(find public -name "index.html" | wc -l)
TOTAL_SIZE=$(du -sh public | cut -f1)
INDEX_SIZE=$(du -sh public/index.html | cut -f1)

print_status "Build Statistics:"
echo "  📄 Total pages: $TOTAL_PAGES"
echo "  📦 Total size: $TOTAL_SIZE" 
echo "  🏠 Homepage size: $INDEX_SIZE"

# Check if this is a dry run
if [[ "$1" == "--dry-run" || "$1" == "-n" ]]; then
    print_warning "Dry run mode - not committing or pushing changes"
    print_success "Build completed successfully!"
    exit 0
fi

# Check git status
print_status "Checking git status..."
if [[ -n $(git status --porcelain) ]]; then
    print_status "Changes detected, preparing commit..."
    
    # Add all changes
    git add .
    
    # Create commit message
    COMMIT_MSG="Deploy: $(date '+%Y-%m-%d %H:%M:%S') - $TOTAL_PAGES pages"
    
    # Commit changes
    git commit -m "$COMMIT_MSG" || {
        print_warning "Nothing new to commit"
    }
    
    # Push to main branch
    print_status "Pushing to GitHub..."
    if git push origin main; then
        print_success "Pushed to GitHub successfully"
        print_success "GitHub Actions will deploy the site automatically"
    else
        print_error "Failed to push to GitHub"
        exit 1
    fi
else
    print_warning "No changes to commit"
fi

# Final success message
print_success "🎉 Deployment process completed!"
echo ""
echo "Next steps:"
echo "  1. Check GitHub Actions for deployment status"
echo "  2. Visit your site at: https://khairu-aqsara.github.io"  
echo "  3. Verify search functionality and responsive design"
echo "  4. Run Lighthouse audit for performance metrics"
echo ""
print_success "Happy blogging! 🚀"