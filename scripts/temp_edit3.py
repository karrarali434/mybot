import re

file_path = 'c:/Users/LOQ/Desktop/oad/bmqa/Plugins/set_ranks.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("مالك اساسي", "منشئ اساسي")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

file_path2 = 'c:/Users/LOQ/Desktop/oad/bmqa/Plugins/get_ranks.py'
with open(file_path2, 'r', encoding='utf-8') as f:
    content2 = f.read()

content2 = content2.replace("المالكين الاساسيين", "المنشئين الاساسيين")

with open(file_path2, 'w', encoding='utf-8') as f:
    f.write(content2)

print('Done!')
