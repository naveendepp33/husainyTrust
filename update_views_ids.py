
filepath = r'f:\censes\censesapp\views.py'
try:
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
except UnicodeDecodeError:
    with open(filepath, 'r', encoding='latin-1') as f:
        lines = f.readlines()

# indices are 0-indexed, so line 1396 is index 1395

# 1. Family head
lines[1405] = '' # Remove line 1406 (member_id)
# Indices 1395 to 1403 (Lines 1396-1403)
for i in range(1395, 1404):
    lines[i] = '# Removed\n'

# 2. Other members in addfamily
lines[1433] = '' # Remove line 1434 (member_id)
# Indices 1423 to 1431 (Lines 1424-1431)
for i in range(1423, 1432):
    lines[i] = '# Removed\n'

# 3. addmember view
# Line 1584 index 1583. Let's find it.
for idx, line in enumerate(lines):
    if 'def addmember(request,id):' in line:
        print(f"Found addmember at {idx}")
        # Search for the block starting 1584 
        # which is indices from 1583 
        lines[1583:1593] = ['# Removed\n'] * 10
        # Search forward for the create call
        for i in range(idx, idx+50):
            if 'member_id=member_id,' in lines[i]:
                lines[i] = ''
        break

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Cleaned up IDs in views successfully")
