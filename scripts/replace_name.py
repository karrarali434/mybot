import os
import re

directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Plugins')
for filename in os.listdir(directory):
    if filename.endswith('.py'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace occurrences
        new_content = content.replace("else 'رعد'", "else 'اتاك'")
        new_content = new_content.replace("else \"رعد\"", "else \"اتاك\"")
        new_content = new_content.replace("else 'ليو'", "else 'اتاك'")
        new_content = new_content.replace("else \"ليو\"", "else \"اتاك\"")

        if content != new_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Updated {filename}')
