#!/bin/bash
# 🛑 Stop Background Job Bot
cd "$(dirname "$0")"

PID_FILE="bot.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
        echo "🛑 Stopping Job Bot process (PID: $PID)..."
        kill "$PID"
        rm -f "$PID_FILE"
        echo "✅ Bot stopped."
        exit 0
    fi
fi

# Fallback check
PID=$(pgrep -f "python3 live_bot.py")
if [ -n "$PID" ]; then
    echo "🛑 Stopping Job Bot process (PID: $PID)..."
    kill "$PID"
    rm -f "$PID_FILE"
    echo "✅ Bot stopped."
else
    echo "ℹ️ No Job Bot process is currently running."
    rm -f "$PID_FILE"
fi
