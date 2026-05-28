#!/usr/bin/env bash
set -e

echo "=== FilmFight Smoke Tests ==="

# 1. Django system checks (ignore deployment warnings)
echo "--- System checks ---"
python3 manage.py check 2>&1

# 2. Start server once, run all curl tests, kill it
echo "--- Starting server ---"
python3 manage.py runserver --noreload &
PID=$!
sleep 3

FAILED=0

check() {
    local url=$1 label=$2
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null || echo "000")
    if [ "$HTTP_CODE" = "200" ]; then
        echo "  PASS — $label"
    else
        echo "  FAIL — $label (HTTP $HTTP_CODE)"
        FAILED=1
    fi
}

check "http://127.0.0.1:8000/" "Homepage"
check "http://127.0.0.1:8000/profile/peepop123/" "Profile page (peepop123)"
check "http://127.0.0.1:8000/profile/david/" "Profile page (david)"
check "http://127.0.0.1:8000/compare/?user_a=peepop123&user_b=david" "Compare page"

kill $PID 2>/dev/null
wait $PID 2>/dev/null

if [ "$FAILED" = "1" ]; then
    echo "=== Some Tests FAILED ==="
    exit 1
fi
echo "=== All Tests Passed ==="
