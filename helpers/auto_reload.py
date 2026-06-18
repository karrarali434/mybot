"""
Auto-Reload Module
==================
Watches Plugins/ and helpers/ directories for .py file changes.
When a change is detected, the bot process restarts automatically
so the new code is loaded without any manual intervention.

Usage in main.py:
    from helpers.auto_reload import start_watcher
    start_watcher()  # Call BEFORE app.run()
"""

import os
import sys
import time
import threading
import logging

logger = logging.getLogger("AUTO_RELOAD")

def _get_file_timestamps(directories):
    """Get modification timestamps for all .py files in given directories."""
    timestamps = {}
    for directory in directories:
        if not os.path.isdir(directory):
            continue
        for root, dirs, files in os.walk(directory):
            # Skip __pycache__ directories
            dirs[:] = [d for d in dirs if d != '__pycache__']
            for f in files:
                if f.endswith('.py'):
                    filepath = os.path.join(root, f)
                    try:
                        timestamps[filepath] = os.path.getmtime(filepath)
                    except OSError:
                        pass
    return timestamps


def _watcher_loop(directories, check_interval=3):
    """Background loop that checks for file changes and restarts if needed."""
    logger.info(f"🔄 Auto-reload watcher started (checking every {check_interval}s)")
    logger.info(f"   Watching: {', '.join(directories)}")
    
    # Get initial state
    last_timestamps = _get_file_timestamps(directories)
    
    while True:
        time.sleep(check_interval)
        try:
            current_timestamps = _get_file_timestamps(directories)
            
            # Check for new or modified files
            changed_files = []
            for filepath, mtime in current_timestamps.items():
                if filepath not in last_timestamps:
                    changed_files.append(("NEW", filepath))
                elif mtime != last_timestamps[filepath]:
                    changed_files.append(("MODIFIED", filepath))
            
            # Check for deleted files
            for filepath in last_timestamps:
                if filepath not in current_timestamps:
                    changed_files.append(("DELETED", filepath))
            
            if changed_files:
                for change_type, filepath in changed_files:
                    basename = os.path.basename(filepath)
                    logger.info(f"🔄 [{change_type}] {basename}")
                
                logger.info("🔄 Changes detected! Restarting bot in 2 seconds...")
                time.sleep(2)  # Small delay to ensure file write is complete
                
                # Restart the process
                _restart_process()
            
            last_timestamps = current_timestamps
            
        except Exception as e:
            logger.error(f"🔄 Watcher error: {e}")
            time.sleep(5)


def _restart_process():
    """Restart the current Python process."""
    logger.info("🔄 Restarting now...")
    
    python = sys.executable
    args = sys.argv[:]
    
    try:
        # On Windows, os.execv doesn't truly replace the process,
        # so we use subprocess + sys.exit for a clean restart
        import subprocess
        
        creationflags = 0
        if sys.platform == "win32":
            creationflags = subprocess.CREATE_NEW_PROCESS_GROUP
        
        # Start new process
        subprocess.Popen(
            [python] + args,
            cwd=os.getcwd(),
            creationflags=creationflags,
        )
        
        # Kill current process
        logger.info("🔄 New process started. Shutting down old process...")
        os._exit(0)
        
    except Exception as e:
        logger.error(f"🔄 Failed to restart: {e}")


def start_watcher(extra_dirs=None, check_interval=3):
    """
    Start the file watcher in a background daemon thread.
    
    Args:
        extra_dirs: Additional directories to watch (list of paths)
        check_interval: Seconds between checks (default: 3)
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    directories = [
        os.path.join(base_dir, "Plugins"),
        os.path.join(base_dir, "helpers"),
    ]
    
    if extra_dirs:
        directories.extend(extra_dirs)
    
    # Filter to only existing directories
    directories = [d for d in directories if os.path.isdir(d)]
    
    if not directories:
        logger.warning("🔄 No directories to watch!")
        return
    
    watcher_thread = threading.Thread(
        target=_watcher_loop,
        args=(directories, check_interval),
        daemon=True,  # Dies when main process dies
        name="AutoReloadWatcher"
    )
    watcher_thread.start()
