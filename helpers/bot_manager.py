import os
import sys
import shutil
import sqlite3
import subprocess
import psutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = os.path.join(BASE_DIR, 'factory.sqlite')

def _is_junction(path):
    """Check if a path is a Windows junction point."""
    try:
        if os.path.islink(path):
            return True
        if sys.platform == "win32":
            import ctypes
            FILE_ATTRIBUTE_REPARSE_POINT = 0x0400
            attrs = ctypes.windll.kernel32.GetFileAttributesW(str(path))
            return attrs != -1 and bool(attrs & FILE_ATTRIBUTE_REPARSE_POINT)
    except:
        pass
    return False

def _create_junction(src, dst):
    """Create a Windows junction (directory symlink, no admin needed)."""
    try:
        if sys.platform == "win32":
            subprocess.run(['cmd', '/c', 'mklink', '/J', dst, src],
                         capture_output=True, check=True)
        else:
            os.symlink(src, dst, target_is_directory=True)
    except Exception as e:
        print(f"Junction creation failed ({src} -> {dst}): {e}")
        # Fallback: copy the directory
        shutil.copytree(src, dst, dirs_exist_ok=True)


def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS bots (
            id TEXT PRIMARY KEY,
            username TEXT,
            token TEXT,
            owner_id INTEGER,
            status TEXT,
            pid INTEGER,
            folder_path TEXT
        )
    ''')
    try:
        c.execute("ALTER TABLE bots ADD COLUMN start_date TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE bots ADD COLUMN duration_months INTEGER")
    except sqlite3.OperationalError:
        pass
    conn.commit()
    conn.close()

def get_all_bots():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM bots")
    rows = c.fetchall()
    conn.close()
    bots = []
    for row in rows:
        bots.append({
            "id": row[0],
            "username": row[1],
            "token": row[2],
            "owner_id": row[3],
            "status": row[4],
            "pid": row[5],
            "folder_path": row[6],
            "start_date": row[7] if len(row) > 7 else None,
            "duration_months": row[8] if len(row) > 8 else None
        })
    return bots

def get_bot(bot_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM bots WHERE id=?", (str(bot_id),))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            "id": row[0],
            "username": row[1],
            "token": row[2],
            "owner_id": row[3],
            "status": row[4],
            "pid": row[5],
            "folder_path": row[6],
            "start_date": row[7] if len(row) > 7 else None,
            "duration_months": row[8] if len(row) > 8 else None
        }
    return None

def add_bot(bot_id, username, token, owner_id, folder_path, start_date=None, duration_months=None):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO bots (id, username, token, owner_id, status, pid, folder_path, start_date, duration_months) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (str(bot_id), username, token, owner_id, 'stopped', None, folder_path, start_date, duration_months))
    conn.commit()
    conn.close()

def update_bot_status(bot_id, status, pid=None):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE bots SET status=?, pid=? WHERE id=?", (status, pid, str(bot_id)))
    conn.commit()
    conn.close()

def delete_bot_db(bot_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM bots WHERE id=?", (str(bot_id),))
    conn.commit()
    conn.close()

def is_process_running(pid):
    if pid is None:
        return False
    try:
        p = psutil.Process(pid)
        return p.is_running() and p.status() != psutil.STATUS_ZOMBIE
    except psutil.NoSuchProcess:
        return False

def stop_bot(bot_id):
    bot = get_bot(bot_id)
    if bot and bot['pid']:
        try:
            parent = psutil.Process(bot['pid'])
            for child in parent.children(recursive=True):
                child.kill()
            parent.kill()
        except psutil.NoSuchProcess:
            pass
    update_bot_status(bot_id, 'stopped', None)

def start_bot(bot_id):
    bot = get_bot(bot_id)
    if not bot:
        return False
    
    if is_process_running(bot['pid']):
        update_bot_status(bot_id, 'running', bot['pid'])
        return True # Already running
        
    folder_path = bot['folder_path']
    main_file = os.path.join(folder_path, "main.py")
    
    if not os.path.exists(main_file):
        return False
        
    try:
        # For Windows, use creationflags to run in background without blocking
        creationflags = 0
        if sys.platform == "win32":
            creationflags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP | 0x08000000 # CREATE_NO_WINDOW
            
        log_file = open(os.path.join(folder_path, "bot.log"), "a", encoding="utf-8")
        
        clean_env = os.environ.copy()
        if "IS_FACTORY" in clean_env:
            del clean_env["IS_FACTORY"]
            
        # -- Auto Sync via Junctions (Symlinks) --
        # Instead of copying files, we create Windows junctions so sub-bots
        # always read directly from the main source code.
        import shutil
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Directories to symlink (sub-bot reads directly from main source)
        junction_dirs = ['Plugins', 'helpers', 'scripts']
        for dir_name in junction_dirs:
            src = os.path.join(base_dir, dir_name)
            dst = os.path.join(folder_path, dir_name)
            if not os.path.isdir(src):
                continue
            # Check if it's already a junction/symlink pointing to the right place
            if os.path.islink(dst) or _is_junction(dst):
                # Already a junction, skip
                continue
            # Remove existing directory (old copy) and create junction
            if os.path.isdir(dst):
                shutil.rmtree(dst)
            # Create Windows junction (no admin required)
            _create_junction(src, dst)
        
        # Sync root-level files (config, images, etc.) - these are small and rarely change
        skip_files = {'.env', 'bot.log', 'factory.sqlite', 'factory.py'}
        skip_extensions = {'.session', '.session-journal', '.sqlite', '.sqlite-shm', '.sqlite-wal'}
        for item in os.listdir(base_dir):
            src = os.path.join(base_dir, item)
            if os.path.isdir(src):
                continue
            if item in skip_files:
                continue
            if any(item.endswith(ext) for ext in skip_extensions):
                continue
            if item.startswith('factory.sqlite'):
                continue
            try:
                shutil.copy2(src, os.path.join(folder_path, item))
            except Exception:
                pass
        # -----------------------
            
        process = subprocess.Popen(
            [sys.executable, "-u", "main.py"],
            cwd=folder_path,
            creationflags=creationflags,
            stdout=log_file,
            stderr=subprocess.STDOUT,
            env=clean_env
        )
        update_bot_status(bot_id, 'running', process.pid)
        return True
    except Exception as e:
        print(f"Failed to start bot {bot_id}: {e}")
        return False

def clone_bot(token, bot_id, bot_username, owner_id, start_date=None, duration_months=None):
    base_dir = os.getcwd()
    bots_dir = os.path.join(base_dir, "bots")
    if not os.path.exists(bots_dir):
        os.makedirs(bots_dir)
        
    bot_folder = os.path.join(bots_dir, str(bot_username))
    if os.path.exists(bot_folder):
        try:
            shutil.rmtree(bot_folder)
        except Exception as e:
            print(f"Error removing old folder: {e}")
        
    os.makedirs(bot_folder)
    
    # Copy files
    ignore_patterns = shutil.ignore_patterns(
        'bots', '__pycache__', '.git', '*.session', '*.session-journal', 
        '*.sqlite', '*.sqlite-shm', '*.sqlite-wal', '.env', 'factory.sqlite*', 'bot.log', 'factory.py'
    )
    
    # Copy root files directly
    for item in os.listdir(base_dir):
        s = os.path.join(base_dir, item)
        d = os.path.join(bot_folder, item)
        if item in ['bots', '__pycache__', '.git', 'bot.log'] or item.endswith('.session') or item.endswith('.sqlite') or item.endswith('.sqlite-shm') or item.endswith('.sqlite-wal') or item == '.env' or item.startswith('factory.sqlite') or item.endswith('.session-journal') or item == 'factory.py':
            continue
        if os.path.isdir(s):
            shutil.copytree(s, d, ignore=ignore_patterns)
        else:
            shutil.copy2(s, d)
            
    # Create .env for the clone
    with open(os.path.join(bot_folder, '.env'), 'w') as f:
        f.write(f"BOT_TOKEN={token}\n")
        f.write(f"BOT_USERNAME={bot_username}\n")
        f.write(f"SUDO_ID={owner_id}\n")
        f.write(f"IS_FACTORY=False\n")
        f.write(f"REDIS_URL={os.getenv('REDIS_URL', 'redis://localhost:6379')}\n")
        
    add_bot(str(bot_id), bot_username, token, owner_id, bot_folder, start_date, duration_months)
    return bot_folder

def remove_bot(bot_id):
    bot = get_bot(bot_id)
    if not bot:
        return False
    stop_bot(bot_id)
    delete_bot_db(bot_id)
    try:
        shutil.rmtree(bot['folder_path'])
    except:
        pass
    return True

def add_months(sourcedate, months):
    import calendar
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return sourcedate.replace(year=year, month=month, day=day)

def calculate_remaining_time(start_date_str, duration_months):
    if not start_date_str or not duration_months:
        return "غير محدد", "غير محدد"
    from datetime import datetime
    try:
        start_date = datetime.fromisoformat(start_date_str)
        end_date = add_months(start_date, int(duration_months))
        now = datetime.now()
        
        if now >= end_date:
            return "منتهي 🔴", end_date.strftime("%Y-%m-%d")
            
        days_total = (end_date - now).days
        months_left = days_total // 30
        days_left = days_total % 30
        
        parts = []
        if months_left > 0:
            parts.append(f"{months_left} شهر")
        if days_left > 0:
            parts.append(f"{days_left} يوم")
            
        remaining_str = " و ".join(parts) if parts else "أقل من يوم"
        return remaining_str, end_date.strftime("%Y-%m-%d")
    except Exception as e:
        return "خطأ في الحساب", "غير محدد"
