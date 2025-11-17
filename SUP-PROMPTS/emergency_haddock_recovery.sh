#!/bin/bash

# Emergency HADDOCK3 Recovery Script
# Use when processes hang with 0% CPU usage (deadlock detection)

# Usage: ./emergency_haddock_recovery.sh

echo "🚨 HADDOCK3 Emergency Recovery Script"
echo "======================================"
echo "Detecting and recovering from HADDOCK3 deadlocks..."
echo

# Function to check for deadlocked processes
check_deadlocks() {
    local deadlocked_processes=()

    # Check for HADDOCK3 processes with 0% CPU
    while IFS= read -r line; do
        if [[ -n "$line" ]]; then
            pid=$(echo "$line" | awk '{print $2}')
            cpu=$(echo "$line" | awk '{print $3}')
            command=$(echo "$line" | awk '{print $8,$9,$10,$11,$12}')

            # Check if CPU is effectively 0.0% (allowing for rounding)
            if [[ "$cpu" == "0.0" || "$cpu" == "0.1" ]]; then
                deadlocked_processes+=("$pid:$command")
            fi
        fi
    done <<< "$(ps aux | grep haddock3 | grep -v grep | grep -v "grep haddock3")"

    echo "${deadlocked_processes[@]}"
}

# Function to get process start time
get_process_start() {
    local pid=$1
    ps -o lstart= -p "$pid" 2>/dev/null | head -1
}

# Function to check if process has been running too long
process_running_too_long() {
    local pid=$1
    local start_time=$(get_process_start "$pid")

    # Get current time in seconds since epoch
    local current_time=$(date +%s)

    # Get process start time in seconds (approximate)
    local start_seconds=$(date -d "$start_time" +%s 2>/dev/null)

    if [[ $? -eq 0 && $start_seconds -gt 0 ]]; then
        local runtime=$((current_time - start_seconds))
        # If running for more than 30 minutes
        if [[ $runtime -gt 1800 ]]; then
            return 0  # True, running too long
        fi
    fi

    return 1  # False, not running too long or couldn't determine
}

# Function to analyze log files
analyze_logs() {
    local log_dirs=($(find . -name "log" -type f 2>/dev/null | head -10))
    local stale_logs=()

    for log_file in "${log_dirs[@]}"; do
        if [[ -f "$log_file" ]]; then
            # Check if log file is older than 60 minutes
            local log_age=$(( ($(date +%s) - $(stat -f %m "$log_file" 2>/dev/null || echo 0)) / 60 ))
            if [[ $log_age -gt 60 ]]; then
                local latest_entry=$(tail -1 "$log_file" 2>/dev/null)
                stale_logs+=("$log_file:$log_age minutes:$latest_entry")
            fi
        fi
    done

    echo "${stale_logs[@]}"
}

# Function to safely kill processes
safe_kill_processes() {
    local pids=("$@")

    if [[ ${#pids[@]} -eq 0 ]]; then
        echo "✅ No deadlocked processes to kill"
        return 0
    fi

    echo "🔨 Killing deadlocked HADDOCK3 processes..."

    for pid in "${pids[@]}"; do
        if kill -0 "$pid" 2>/dev/null; then
            echo "   Killing PID $pid..."

            # Try graceful kill first
            kill -TERM "$pid" 2>/dev/null
            sleep 5

            # If still exists, force kill
            if kill -0 "$pid" 2>/dev/null; then
                echo "   Force killing PID $pid..."
                kill -9 "$pid" 2>/dev/null
            fi

            echo "   ✅ Process $pid terminated"
        else
            echo "   ⚠️  Process $pid already terminated"
        fi
    done

    # Verify all killed
    sleep 2
    local remaining=$(ps aux | grep haddock3 | grep -v grep | wc -l)
    if [[ $remaining -eq 0 ]]; then
        echo "✅ All HADDOCK3 processes terminated successfully"
    else
        echo "⚠️  Some processes may still be running"
    fi
}

# Function to provide recovery recommendations
provide_recommendations() {
    local deadlock_detected=$1
    local stale_log_detected=$2

    echo ""
    echo "📋 RECOVERY RECOMMENDATIONS:"
    echo "==========================="

    if [[ "$deadlock_detected" == "true" ]]; then
        echo "🔧 DEADLOCK DETECTED - ACTIONS TAKEN:"
        echo "   • Deadlocked HADDOCK3 processes terminated"
        echo "   • System resources freed"
        echo ""
        echo "🎯 NEXT STEPS:"
        echo "   1. Validate your protein structures:"
        echo "      ./validate_structure_before_haddock.py protein_target.pdb"
        echo "   2. Check for the 3 failure categories:"
        echo "      - Category 1: Broken/Truncated structures (<90 atoms)"
        echo "      - Category 2: Oversized proteins (>2500 atoms)"
        echo "      - Category 3: Placeholder files (~5 atoms)"
        echo "   3. Reference guides:"
        echo "      - HADDOCK3_PREPROCESSING_VALIDATION_CHECKLIST.md"
        echo "      - HADDOCK3_DEADLOCK_TROUBLESHOOTING_GUIDE.md"
        echo "      - HADDOCK3_DOMAIN_EXTRACTION_GUIDE.md"
    else
        echo "✅ NO DEADLOCKS DETECTED"
        echo "   • All HADDOCK3 processes appear healthy"
        echo "   • CPU usage is normal"
    fi

    if [[ "$stale_log_detected" == "true" ]]; then
        echo ""
        echo "⚠️  STALE LOG FILES DETECTED:"
        echo "   • Some log files haven't been updated for >60 minutes"
        echo "   • May indicate slow progress or hidden issues"
        echo "   • Monitor progress or consider validation check"
    fi

    echo ""
    echo "🛡️ PREVENTION TIPS:"
    echo "   • ALWAYS validate structures before HADDOCK3 execution"
    echo "   • Use proven atom count range: 90-2107 atoms"
    echo "   • Extract domains for proteins >2500 atoms"
    echo "   • Never use placeholder files with <10 atoms"
    echo ""
    echo "📞 For detailed troubleshooting:"
    echo "   • Review: HADDOCK3_DEADLOCK_TROUBLESHOOTING_GUIDE.md"
    echo "   • Run validation: ./validate_structure_before_haddock.py"
}

# Main execution
main() {
    echo "🔍 Checking for HADDOCK3 deadlocks..."

    # Check for deadlocked processes
    local deadlock_info=($(check_deadlocks))
    local deadlock_pids=()

    local deadlock_detected="false"
    local stale_log_detected="false"

    if [[ ${#deadlock_info[@]} -gt 0 ]]; then
        echo ""
        echo "🚨 DEADLOCKED PROCESSES DETECTED:"
        echo "PID     Command                           CPU  Runtime"
        echo "----    --------                           ---  -------"

        for info in "${deadlock_info[@]}"; do
            local pid="${info%%:*}"
            local command="${info#*:}"
            local start_time=$(get_process_start "$pid")

            # Check if running too long
            if process_running_too_long "$pid"; then
                echo "$pid    $command    0.0%  $start_time"
                deadlock_pids+=("$pid")
                deadlock_detected="true"
            fi
        done
    else
        echo "✅ No deadlocked HADDOCK3 processes found"
    fi

    # Check for stale log files
    echo ""
    echo "📋 Checking log file activity..."
    local log_info=($(analyze_logs))

    if [[ ${#log_info[@]} -gt 0 ]]; then
        echo "⚠️  STALE LOG FILES DETECTED:"
        for info in "${log_info[@]}"; do
            local log_file="${info%%:*}"
            local remaining="${info#*:}"
            local age="${remaining%%:*}"
            local latest_entry="${remaining#*:}"

            echo "   $log_file (inactive for $age)"
            echo "   Latest: $latest_entry"
        done
        stale_log_detected="true"
    else
        echo "✅ Log files appear to be actively updated"
    fi

    # Kill deadlocked processes
    if [[ "$deadlock_detected" == "true" ]]; then
        echo ""
        safe_kill_processes "${deadlock_pids[@]}"
    fi

    # Provide recommendations
    provide_recommendations "$deadlock_detected" "$stale_log_detected"

    echo ""
    echo "🏁 Emergency recovery script completed"
}

# Check if running as intended
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi