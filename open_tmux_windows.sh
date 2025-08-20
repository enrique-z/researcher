#!/bin/bash

# Get list of tmux sessions
sessions=$(tmux list-sessions -F "#{session_name}")

# Open a new iTerm window for each session
for session in $sessions; do
    osascript <<EOF
tell application "iTerm"
    create window with default profile
    tell current session of current window
        write text "tmux attach-session -t $session"
    end tell
end tell
EOF
    echo "Opened iTerm window for session: $session"
    # Small delay to prevent overwhelming iTerm
    sleep 0.5
done

echo "All tmux sessions now have their own iTerm windows!"
