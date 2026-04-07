
filepath = r'f:\censes\censesapp\models.py'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_save_method = [
    '    def save(self,*args,**kwargs):\n',
    '        if not self.member_id:\n',
    '            # Generate ID based on current members in this specific family\n',
    '            # We try to find the last sequence number used for this family\n',
    '            last_member = Member.objects.filter(family=self.family, member_id__contains="-").order_by("-member_id").first()\n',
    '            if last_member and "-" in last_member.member_id:\n',
    '                try:\n',
    '                    last_num = int(last_member.member_id.split("-")[-1])\n',
    '                    num = last_num + 1\n',
    '                except (ValueError, IndexError):\n',
    '                    num = Member.objects.filter(family=self.family).count() + 1\n',
    '            else:\n',
    '                num = Member.objects.filter(family=self.family).count() + 1\n',
    '            \n',
    '            self.member_id = f"{self.family.family_id}-{num}"\n',
    '        super().save(*args,**kwargs)\n'
]

# Find where the save method starts and ends
# Based on previous view_file, indices 438:443 (since it was 5 lines)
# Wait, I just modified it to 5 lines.
# 439:     def save(self,*args,**kwargs):
# 440:         if not self.member_id:
# 441:             count = Member.objects.filter(family=self.family).count()
# 442:             self.member_id = f"{self.family.family_id}-{count + 1}"
# 443:         super().save(*args,**kwargs)

lines[438:443] = new_save_method

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Updated Member.save with more robust family-linked ID generation")
