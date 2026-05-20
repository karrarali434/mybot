import re

file_path = 'c:/Users/LOQ/Desktop/oad/bmqa/Plugins/all.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Edit commands1
content = content.replace('⌯ رفع ↣ ↢ تنزيل مالك\n', '⌯ رفع ↣ ↢ تنزيل منشئ\n⌯ رفع ↣ ↢ تنزيل مالك\n')
content = content.replace('⌯ مسح الرتب\n', '⌯ مسح الرتب\n⌯ مسح الرتب الوهميه\n')

# Edit commands3
content = content.replace('⌯ تفعيل ↣ ↢ تعطيل الرابط\n', '⌯ تفعيل ↣ ↢ تعطيل الرابط\n⌯ تفعيل ↣ ↢ تعطيل الرابط العادي\n')
content = content.replace('⌯ قفل ↣ ↢ فتح  التكرار\n', '⌯ قفل ↣ ↢ فتح  التكرار بالكتم\n⌯ وضع التكرار + العدد\n')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Help menus in all.py updated")
