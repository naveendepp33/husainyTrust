
import os

filepath = r'f:\censes\censesapp\models.py'
with open(filepath, 'r') as f:
    lines = f.readlines()

new_lines = []
in_member_save = False
skip_next = False

for line in lines:
    if 'def save(self,*args,**kwargs):' in line and 'Member' in lines[max(0, lines.index(line)-15):lines.index(line)]: 
        # This is simple and messy, but let's just replace the specific block
        pass
    
    # Let's find the Member class and then its save method
    
content = "".join(lines)
old_block = """    def save(self,*args,**kwargs):

        if not self.member_id:

            last = Member.objects.order_by('-id').first()

            if last:
                num = int(last.member_id[3:]) + 1
            else:
                num = 1

            self.member_id = f"HTM{num:04d}"

        super().save(*args,**kwargs)"""

new_block = """    def save(self,*args,**kwargs):
        if not self.member_id:
            count = Member.objects.filter(family=self.family).count()
            self.member_id = f"{self.family.family_id}-{count + 1}"
        super().save(*args,**kwargs)"""

# Instead of exact match, just look for the known self.member_id line
if 'self.member_id = f"HTM{num:04d}"' in content:
    print("Found old content")
    # Actually let's use the line-number based approach from view_file
    # line 439 to 452
    
import sys
content_lines = open(filepath).readlines()
# Lines 439 to 452 inclusive (1-indexed) are content_lines[438:452]
new_save_method = [
    '    def save(self,*args,**kwargs):\n',
    '        if not self.member_id:\n',
    '            count = Member.objects.filter(family=self.family).count()\n',
    '            self.member_id = f"{self.family.family_id}-{count + 1}"\n',
    '        super().save(*args,**kwargs)\n'
]
content_lines[438:452] = new_save_method
with open(filepath, 'w') as f:
    f.writelines(content_lines)
print("Updated successfully")
