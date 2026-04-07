
filepath = r'f:\censes\censesapp\views.py'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    # Found HTM...-1 head member fix
    if '# 1️⃣ ADD FAMILY HEAD AS MEMBER' in lines[idx-1] if idx > 0 else False:
        # Search for Member.objects.create in next few lines
        for i in range(idx, idx+15):
             if 'family=family,' in lines[i]:
                  # Ensure Member.objects.create is before it
                  if 'Member.objects.create(' not in lines[i-1]:
                       lines[i] = '        Member.objects.create(\n' + lines[i]
                  break

    # Fix other members and addmember view
    if 'family=family,' in line and 'Member.objects.create(' not in lines[idx-1]:
        # Check if it was part of a create call that lost its head
        if 'name=name,' in lines[idx+1] or 'name=' in lines[idx+1]:
            lines[idx] = '                Member.objects.create(\n' + lines[idx]

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Restored Member.objects.create headings")
