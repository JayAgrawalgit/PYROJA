#!/usr/bin/env bash
# ==============================================================================
# PYROJA Developer Workflow Automation
# Enforces: Validation -> Build -> Conventional Commit -> Push
# Rule: NEVER push or commit broken builds.
# ==============================================================================

set -euo pipefail

# Text formatting
BOLD="\033[1m"
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
BLUE="\033[0;34m"
NC="\033[0m"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo -e "${BLUE}${BOLD}=== PYROJA Developer Workflow Automation ===${NC}"

# 1. Argument parsing
COMMIT_MSG="${1:-}"
BUILD_APK=false

for arg in "$@"; do
    if [[ "$arg" == "--build-apk" ]]; then
        BUILD_APK=true
    fi
done

if [[ -z "$COMMIT_MSG" ]]; then
    echo -e "${RED}Error: Commit message required.${NC}"
    echo "Usage: ./scripts/workflow.sh \"<type>(<scope>): <subject>\" [--build-apk]"
    echo "Example: ./scripts/workflow.sh \"feat(cart): add bulk discount calculation\""
    exit 1
fi

# 2. Conventional Commit Regex Validation
CONVENTIONAL_REGEX="^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-zA-Z0-9_\.\-]+\))?: .+$"
if [[ ! "$COMMIT_MSG" =~ $CONVENTIONAL_REGEX ]]; then
    echo -e "${RED}Error: Commit message does not adhere to Conventional Commits standard.${NC}"
    echo -e "Format must be: ${BOLD}<type>(<scope>): <subject>${NC}"
    echo "Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert"
    echo "Provided: '$COMMIT_MSG'"
    exit 1
fi

echo -e "${YELLOW}Step 1: Running Pre-Commit Validations...${NC}"

# Validate Python Sync Service Tests
if [[ -x "sync-service/.venv/bin/python" ]]; then
    echo "Running sync-service test suite..."
    sync-service/.venv/bin/python -m pytest sync-service/tests/ -q
elif command -v pytest &> /dev/null; then
    echo "Running pytest..."
    pytest sync-service/tests/ -q
else
    echo -e "${YELLOW}Warning: pytest virtualenv not found; skipping python tests.${NC}"
fi

# Validate JavaScript syntax and synchronize version
if command -v node &> /dev/null; then
    echo "Synchronizing semantic version..."
    node tablet-app/scripts/sync-version.js
    echo "Validating JavaScript syntax..."
    node -c tablet-app/app.js
    node -c tablet-app/version.js
fi

# 3. Optional APK Build Validation
if [[ "$BUILD_APK" == true ]]; then
    echo -e "${YELLOW}Step 2: Building Android APK & Validating Native Build...${NC}"
    cd "$REPO_ROOT/tablet-app"
    npm run sync
    cd android
    export ANDROID_HOME="${ANDROID_HOME:-$HOME/Library/Android/sdk}"
    export JAVA_HOME="${JAVA_HOME:-/Applications/Android Studio.app/Contents/jbr/Contents/Home}"
    ./gradlew assembleDebug --no-daemon
    cp app/build/outputs/apk/debug/app-debug.apk "$REPO_ROOT/tablet-app/dist/pyroja-pos-debug.apk"
    cp app/build/outputs/apk/debug/app-debug.apk "$REPO_ROOT/tablet-app/dist/pyrowholesale-pos-debug.apk"
    cd "$REPO_ROOT"
    echo -e "${GREEN}✓ APK Built and copied to tablet-app/dist/${NC}"
fi

# 4. Check for unstaged/modified files
if [[ -z "$(git status --porcelain)" ]]; then
    echo -e "${YELLOW}Working tree clean. No changes to commit.${NC}"
    exit 0
fi

echo -e "${YELLOW}Step 3: Staging and Committing...${NC}"
git add -A
git commit -m "$COMMIT_MSG"

COMMIT_HASH=$(git rev-parse HEAD)
SHORT_HASH=$(git rev-parse --short HEAD)
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

echo -e "${GREEN}✓ Commit successful: ${BOLD}${SHORT_HASH}${NC} on branch ${BOLD}${CURRENT_BRANCH}${NC}"

# 5. Remote Push Handling
echo -e "${YELLOW}Step 4: Checking Git Remote...${NC}"
REMOTE_COUNT=$(git remote | wc -l | tr -d ' ')

if [[ "$REMOTE_COUNT" -gt 0 ]]; then
    REMOTE_NAME=$(git remote | head -n 1)
    echo "Remote '${REMOTE_NAME}' found. Attempting to push ${CURRENT_BRANCH}..."
    if git push "$REMOTE_NAME" "$CURRENT_BRANCH"; then
        echo -e "${GREEN}✓ Successfully pushed to ${REMOTE_NAME}/${CURRENT_BRANCH}${NC}"
    else
        echo -e "${YELLOW}Warning: git push failed (network or auth issue). Commit remains local.${NC}"
    fi
else
    echo -e "${YELLOW}Notice: No git remote configured. Push skipped.${NC}"
fi

echo -e "${BLUE}${BOLD}=== Workflow Complete ===${NC}"
echo -e "Commit: ${BOLD}${COMMIT_HASH}${NC}"
echo -e "Message: ${COMMIT_MSG}"
