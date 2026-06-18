import asyncio
import os
import sys
import logging
import traceback

# Force UTF-8 output for Arabic text in terminal
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Setup comprehensive logging - ALL errors will show in terminal
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
    datefmt='%H:%M:%S',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("BOT")

# Catch ALL unhandled exceptions and show them in terminal
def global_exception_handler(exc_type, exc_value, exc_tb):
    logger.error(f"❌ UNHANDLED EXCEPTION: {exc_type.__name__}: {exc_value}")
    logger.error(''.join(traceback.format_exception(exc_type, exc_value, exc_tb)))
sys.excepthook = global_exception_handler

# Catch unhandled exceptions in threads too
import threading
_original_thread_run = threading.Thread.run
def _patched_thread_run(self):
    try:
        _original_thread_run(self)
    except Exception as e:
        logger.error(f"❌ THREAD CRASH [{self.name}]: {type(e).__name__}: {e}")
        logger.error(traceback.format_exc())
threading.Thread.run = _patched_thread_run

# Ensure the working directory is always the script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import redis
from pyrogram import Client, idle
from config import token, Dev_Zaid, owner_id, r, botUsername, IS_FACTORY

plugins_config = {"root": "Plugins"}
if not IS_FACTORY:
    plugins_config["exclude"] = ["factory"]

app = Client(f'{Dev_Zaid}r3d', 33763526, 'e2644b351ca9ebbe628dc6cd1a6d4b16',
    bot_token=token,
    plugins=plugins_config
)

if not r.get(f'{Dev_Zaid}:botkey'):
    r.set(f'{Dev_Zaid}:botkey', '⇜')

if not r.get(f'{Dev_Zaid}botname'):
    r.set(f'{Dev_Zaid}botname', 'رعد')

if not r.get(f'{Dev_Zaid}botchannel'):
    r.set(f'{Dev_Zaid}botchannel', 'W_WT1')

async def main():
    print('''
[===========================]

█████╗░██████╗░██████╗░
██╔══██╗╚════██╗██╔══██╗
██████╔╝░█████╔╝██║░░██║
██╔══██╗░╚═══██╗██║░░██║
██║░░██║██████╔╝██████╔╝
╚═╝░░╚═╝╚═════╝░╚═════╝░

[===========================]

* Your bot started successfully on R 3 D * Source *

••••••••  -  •••••••••
''')
    
    if IS_FACTORY:
        try:
            from helpers.bot_manager import init_db, get_all_bots, start_bot
            init_db()
            bots = get_all_bots()
            for bot in bots:
                if bot['status'] == 'running':
                    print(f"Auto-starting bot {bot['username']}...")
                    start_bot(bot['id'])
        except Exception as e:
            print(f"Error starting factory bots: {e}")

    # Start auto-reload watcher (monitors Plugins/ and helpers/ for changes)
    from helpers.auto_reload import start_watcher
    start_watcher()
    
    await app.start()
    
    # Send startup message
    dev_group = r.get(f'DevGroup:{Dev_Zaid}')
    if dev_group:
        try:
            await app.send_message(int(dev_group), "تم تشغيل البوت بنجاح ✔️")
        except Exception as e:
            pass

    from Plugins.clean import auto_clean_function
    from Plugins.fifa import fifa_league_task
    asyncio.create_task(auto_clean_function(app))
    asyncio.create_task(fifa_league_task(app))
    
    await idle()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
