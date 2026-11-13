#!/bin/bash
# 🤖 Run Job Auto-Apply Bot in Background
cd "$(dirname "$0")"

PID_FILE="bot.pid"
LOG_FILE="bot.log"

if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
    echo "⚠️ Job Bot is already running in background (PID: $(cat "$PID_FILE"))."
    echo "To view live logs: tail -f bot.log"
    echo "To stop: ./stop_bot.sh"
    exit 0
fi

echo "🚀 Starting Job Auto-Apply Bot & Web Dashboard in background..."
PYTHONUNBUFFERED=1 nohup python3 -u server.py > "$LOG_FILE" 2>&1 &
echo $! > "$PID_FILE"
echo "✅ Bot started successfully (PID: $(cat "$PID_FILE"))!"
echo "📁 Live logs streaming to: $LOG_FILE"
echo "To stop anytime, run: ./stop_bot.sh"
