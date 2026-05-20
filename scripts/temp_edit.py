import re

file_path = 'c:/Users/LOQ/Desktop/oad/bmqa/helpers/Ranks.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("return 'المالك الاساسي'", "return 'منشئ اساسي'")

creator_block = '''   if r.get(f'{cid}:rankCREATOR:{id}{Dev_Zaid}'):
      if r.get(f'{cid}:RankCreator:{Dev_Zaid}'):
         return r.get(f'{cid}:RankCreator:{Dev_Zaid}')
      return 'منشئ'
'''
if 'rankCREATOR' not in content:
    content = content.replace("   if r.get(f'{cid}:rankOWNER:{id}{Dev_Zaid}'):\n      if r.get(f'{cid}:RankOwner:{Dev_Zaid}'):", creator_block + "   if r.get(f'{cid}:rankOWNER:{id}{Dev_Zaid}'):\n      if r.get(f'{cid}:RankOwner:{Dev_Zaid}'):")

creator_pls_func = '''
def creator_pls(id, cid) -> bool:
   if id == 6646631745 or id == 6646631745:
      return True
   if id == 6646631745 or id == 6646631745:
      return True
   if id == int(Dev_Zaid):
      return True
   if id == int(r.get(f'{Dev_Zaid}botowner')):
      return True
   if r.get(f'{id}:rankDEV2:{Dev_Zaid}'):
      return True
   if r.get(f'{id}:rankDEV:{Dev_Zaid}'):
      return True
   if r.get(f'{cid}:rankGOWNER:{id}{Dev_Zaid}'):
      return True
   if r.get(f'{cid}:rankCREATOR:{id}{Dev_Zaid}'):
      return True
   else:
      return False
'''

if 'def creator_pls' not in content:
    content = content.replace("def gowner_pls(id, cid) -> bool:", creator_pls_func + "\ndef gowner_pls(id, cid) -> bool:")

for func in ['owner_pls', 'mod_pls', 'admin_pls', 'pre_pls']:
    repl = "   if r.get(f'{cid}:rankGOWNER:{id}{Dev_Zaid}'):\n      return True\n   if r.get(f'{cid}:rankCREATOR:{id}{Dev_Zaid}'):\n      return True"
    content = re.sub(r"   if r.get\(f'\{cid\}:rankGOWNER:\{id\}\{Dev_Zaid\}'\):\s+return True", repl, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
