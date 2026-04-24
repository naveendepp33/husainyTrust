from django.db import models
from django.contrib.auth.models import User

class AddUser(models.Model):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('volunteer', 'Volunteer'),
    )

    ROLE_PREFIX = {
        'admin': 'ADM',
        'manager': 'SVR',
        'volunteer': 'VOL',
    }

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"   
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    employee_id = models.CharField(max_length=10, unique=True, blank=True)  # renamed

    # fullname = models.CharField(max_length=100)
    email = models.CharField(max_length=50, null=True, blank=True)
    mobile = models.CharField(max_length=15)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    supervisor = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="volunteers"
    )

    def save(self, *args, **kwargs):
        if not self.employee_id:
            prefix = self.ROLE_PREFIX.get(self.role)

            last_user = AddUser.objects.filter(role=self.role).order_by('-id').first()

            if last_user and last_user.employee_id:
                last_number = int(last_user.employee_id[-3:])
                new_number = last_number + 1
            else:
                new_number = 1

            self.employee_id = f"{prefix}{new_number:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class LoginReport(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField()
    logout_time = models.DateTimeField(null=True, blank=True)

    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="states")
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('country', 'name')

    def __str__(self):
        return f"{self.name} - {self.country.name}"
    

class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="cities")
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('state', 'name')

    def __str__(self):
        return f"{self.name} - {self.state.name}"
    

class Area(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="areas")
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('city', 'name')

    def __str__(self):
        return f"{self.name} - {self.city.name}"
    
class Pincode(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name="pincodes")
    code = models.CharField(max_length=10)

    class Meta:
        unique_together = ('area', 'code')

    def __str__(self):
        return f"{self.code} - {self.area.name}"


class Relationship(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class ChronicDisease(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Qualification(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Occupation(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Income(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class BloodGroup(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class OverallHealth(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Grade(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Sports(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Sectors(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class SiteSetting(models.Model):
    logo = models.ImageField(upload_to="site_logo/", blank=True, null=True)
    site_name = models.CharField(max_length=200)
    address = models.TextField()
    contact_no = models.CharField(max_length=20)
    contact_email = models.EmailField()

    def __str__(self):
        return self.site_name

class News(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]

class VolunteerAllocation(models.Model):

    volunteer = models.ForeignKey(
        AddUser,
        on_delete=models.CASCADE,
        related_name="volunteer_allocations"
    )

    start_date = models.DateField()
    end_date = models.DateField()

    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    allocated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.volunteer.username} - ({self.start_date} to {self.end_date})"

class Family(models.Model):

    family_id = models.CharField(max_length=10, unique=True, blank=True)

    head_name = models.CharField(max_length=100)
    aadhar_no = models.CharField(max_length=12)
    mobile_no = models.CharField(max_length=15)

    door_no = models.CharField(max_length=50)
    apartment_name = models.CharField(max_length=100, blank=True)
    flat_no = models.CharField(max_length=50, blank=True)

    floor_no = models.CharField(max_length=50)
    street_name = models.CharField(max_length=100)
    road_name = models.CharField(max_length=100)

    area = models.ForeignKey(Area, on_delete=models.CASCADE)

    pincode = models.CharField(max_length=10)

    landline = models.CharField(max_length=15, blank=True)

    residential_status = models.CharField(
        max_length=20,
        choices=[("Owner","Owner"),("Renter","Renter")]
    )

    ration_card = models.FileField(upload_to="ration_cards/", blank=True)

    no_of_members = models.IntegerField()

    created_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

    created_at = models.DateTimeField(auto_now_add=True)


    def save(self,*args,**kwargs):

        if not self.family_id:

            last = Family.objects.order_by('-id').first()

            if last:
                num = int(last.family_id[3:]) + 1
            else:
                num = 1

            self.family_id = f"HTF{num:04d}"

        super().save(*args,**kwargs)


    def __str__(self):
        return self.family_id
    
    
class Member(models.Model):

    member_id = models.CharField(max_length=20, unique=True, blank=True)

    family = models.ForeignKey(
        Family,
        on_delete=models.SET_NULL,
        related_name="members",
        null=True,
        blank=True
    )

    name = models.CharField(max_length=100)

    member_type = models.CharField(
        max_length=20,
        choices=[
            ("Adult","Adult"),
            ("Student","Student"),
            ("Baby","Baby")
        ]
    )

    is_updated = models.BooleanField(default=False)

    # -----------------------------
    # COMMON FIELDS
    # -----------------------------

    relationship = models.ForeignKey(Relationship,on_delete=models.SET_NULL,null=True,blank=True)

    alias = models.CharField(max_length=100, blank=True, null=True)

    father_name = models.CharField(max_length=100, blank=True, null=True)

    gender = models.CharField(
        max_length=10,
        choices=[("Male","Male"),("Female","Female"),("Other","Other")],
        blank=True,null=True
    )

    date_of_birth = models.DateField(blank=True, null=True)

    blood_group = models.ForeignKey(BloodGroup,on_delete=models.SET_NULL,null=True,blank=True)

    overall_health = models.ForeignKey(OverallHealth,on_delete=models.SET_NULL,null=True,blank=True)

    govt_health_insurance = models.BooleanField(default=False)

    private_health_insurance = models.BooleanField(default=False)

    photo = models.ImageField(upload_to="member_photos/",blank=True,null=True)

    # shared fields
    languages_speak = models.CharField(max_length=200, blank=True, null=True)
    languages_read = models.CharField(max_length=200, blank=True, null=True)
    languages_write = models.CharField(max_length=200, blank=True, null=True)
    computer_proficiency = models.CharField(max_length=100, blank=True, null=True)

    chronic_disease = models.ForeignKey(
        ChronicDisease,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    disability = models.CharField(max_length=200, blank=True, null=True)

    aadhaar_number = models.CharField(max_length=20, blank=True, null=True)

    # -----------------------------
    # ADULT FIELDS
    # -----------------------------

    marital_status = models.CharField(max_length=50, blank=True, null=True)

    qualification = models.ForeignKey(
        Qualification,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    diploma_degree = models.CharField(max_length=200, blank=True, null=True)

    skills = models.CharField(max_length=200, blank=True, null=True)

    occupation = models.ForeignKey(
        Occupation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    company_name = models.CharField(max_length=200, blank=True, null=True)

    sector = models.CharField(max_length=100, blank=True, null=True)

    industry = models.CharField(max_length=100, blank=True, null=True)

    designation = models.CharField(max_length=100, blank=True, null=True)

    department = models.CharField(max_length=100, blank=True, null=True)

    income = models.ForeignKey(
        Income,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    activity_level = models.CharField(max_length=100, blank=True, null=True)

    husainy_trust_member = models.BooleanField(default=False)

    membership_number = models.CharField(max_length=100, blank=True, null=True)

    interested_in_digital_directory = models.BooleanField(default=False)

    listing_in_community_digital_pages = models.BooleanField(default=False)

    product_service_listing_in_yellow_pages = models.CharField(max_length=100,null=True,blank=True)

    email_id = models.EmailField(blank=True, null=True)

    mobile = models.CharField(max_length=15, blank=True, null=True)

    whatsapp = models.CharField(max_length=15, blank=True, null=True)

    # -----------------------------
    # STUDENT FIELDS
    # -----------------------------

    current_education_status = models.CharField(max_length=100, blank=True, null=True)

    school_college_institute_name = models.CharField(max_length=200, blank=True, null=True)

    grade_year = models.CharField(max_length=50, blank=True, null=True)

    annual_academic_fees = models.CharField(max_length=50, blank=True, null=True)

    fees_payment = models.CharField(max_length=100, blank=True, null=True)

    sports = models.CharField(max_length=200, blank=True, null=True)

    hobbies = models.CharField(max_length=200, blank=True, null=True)

    career_goal = models.CharField(max_length=200, blank=True, null=True)

    holy_koran_reading = models.CharField(max_length=100, blank=True, null=True)

    deeniyath = models.CharField(max_length=100, blank=True, null=True)

    # -----------------------------
    # TRANSFER/REMOVAL INFO
    # -----------------------------
    removal_reason = models.CharField(max_length=100, blank=True, null=True)
    transfer_date = models.DateField(blank=True, null=True)
    transferred_to_family = models.ForeignKey(
        Family, on_delete=models.SET_NULL, null=True, blank=True, related_name="transferred_in_members"
    )
    
    # -----------------------------
    # ID GENERATION
    # -----------------------------


    def save(self,*args,**kwargs):
        if not self.member_id and self.family:
            # Generate ID safely by finding the max numeric suffix
            members = Member.objects.filter(family=self.family, member_id__contains="-")
            max_num = 0
            for m in members:
                try:
                    num = int(m.member_id.split("-")[-1])
                    if num > max_num:
                        max_num = num
                except (ValueError, IndexError):
                    pass
            
            new_num = max_num + 1
            self.member_id = f"{self.family.family_id}-{new_num}"
            
            # Ensure unique constraint is strictly followed
            while Member.objects.filter(member_id=self.member_id).exists():
                new_num += 1
                self.member_id = f"{self.family.family_id}-{new_num}"
                
        super().save(*args,**kwargs)


    def __str__(self):
        return self.member_id