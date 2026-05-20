import os
import re
import glob

files = glob.glob('Plugins/*.py')

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Any mention of url="https://t.me/{channel}" or url=f"t.me/{channel}" that corresponds to an update channel.
    # Actually, let's just make `channel = 'eeeCASH'` if it's not explicitly inquiry.
    # We can replace:
    # `channel = r.get(f'{Dev_Zaid}:BotChannel') if r.get(f'{Dev_Zaid}:BotChannel') else 'GGGGG1S'`
    # with
    # `channel = r.get(f'{Dev_Zaid}:BotChannel') if r.get(f'{Dev_Zaid}:BotChannel') else 'eeeCASH'`
    # Wait! If I do this, it will make "للاستفسار" point to `eeeCASH` again. 
    # But wait, we can just find 'للاستفسار - @{channel}' and change it to 'للاستفسار - @GGGGG1S'
    # And 'للاستفسار - {channel}' to 'للاستفسار - @GGGGG1S'

    # Fix inquiries first
    content = re.sub(r'للاستفسار - @?\{channel\}', 'للاستفسار - @GGGGG1S', content)
    content = re.sub(r'للاستفسار \- @?GGGGG1S', 'للاستفسار - @GGGGG1S', content)
    
    # Fix the fallback for BotChannel to be 'eeeCASH'
    content = content.replace("else 'GGGGG1S'", "else 'eeeCASH'")
    content = content.replace('else "GGGGG1S"', 'else "eeeCASH"')
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Channel fix applied.")
