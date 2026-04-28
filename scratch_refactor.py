import re

with open(r'f:\censes\censesapp\views.py', 'r', encoding='utf-8') as f:
    content = f.read()

helper_code = """
def _get_advanced_filtered_members(request):
    members = Member.objects.all().select_related(
        'family', 'blood_group', 'occupation', 'qualification',
        'income', 'overall_health', 'chronic_disease', 'relationship'
    )
    
    q = request.GET.get('q', '').strip()
    if q:
        members = members.filter(
            Q(name__icontains=q) | Q(member_id__icontains=q) |
            Q(family__family_id__icontains=q) | Q(alias__icontains=q) |
            Q(father_name__icontains=q) | Q(aadhaar_number__icontains=q) |
            Q(member_type__icontains=q) | Q(gender__icontains=q) |
            Q(marital_status__icontains=q) | Q(date_of_birth__icontains=q) |
            Q(relationship__name__icontains=q) | Q(mobile__icontains=q) |
            Q(whatsapp__icontains=q) | Q(email_id__icontains=q) |
            Q(blood_group__name__icontains=q) | Q(overall_health__name__icontains=q) |
            Q(chronic_disease__name__icontains=q) | Q(disability__icontains=q) |
            Q(activity_level__icontains=q) | Q(family__area__name__icontains=q) |
            Q(family__area__city__name__icontains=q) | Q(qualification__name__icontains=q) |
            Q(occupation__name__icontains=q) | Q(income__name__icontains=q) |
            Q(designation__icontains=q) | Q(department__icontains=q) |
            Q(company_name__icontains=q) | Q(skills__icontains=q) |
            Q(diploma_degree__icontains=q) | Q(sector__icontains=q) |
            Q(industry__icontains=q) | Q(membership_number__icontains=q) |
            Q(product_service_listing_in_yellow_pages__icontains=q) |
            Q(languages_speak__icontains=q) | Q(languages_read__icontains=q) |
            Q(languages_write__icontains=q) | Q(computer_proficiency__icontains=q) |
            Q(current_education_status__icontains=q) | Q(school_college_institute_name__icontains=q) |
            Q(grade_year__icontains=q) | Q(fees_payment__icontains=q) |
            Q(annual_academic_fees__icontains=q) | Q(sports__icontains=q) |
            Q(hobbies__icontains=q) | Q(career_goal__icontains=q) |
            Q(holy_koran_reading__icontains=q) | Q(deeniyath__icontains=q)
        ).distinct()

    get = request.GET.get
    family_id = get('family_id', '').strip()
    member_id = get('member_id', '').strip()
    name = get('name', '').strip()
    member_type = get('member_type', '').strip()
    gender = get('gender', '').strip()
    age = get('age', '').strip()
    city = get('city', '').strip()
    state = get('state', '').strip()
    pincode = get('pincode', '').strip()
    area = get('area', '').strip()
    blood_group = get('blood_group', '').strip()
    qualification = get('qualification', '').strip()
    income = get('income', '').strip()
    health = get('health', '').strip()
    disease = get('disease', '').strip()
    mobile = get('mobile', '').strip()
    whatsapp = get('whatsapp', '').strip()
    email_id = get('email_id', '').strip()
    aadhaar_number = get('aadhaar_number', '').strip()
    marital_status = get('marital_status', '').strip()
    occupation = get('occupation', '').strip()
    company_name = get('company_name', '').strip()
    designation = get('designation', '').strip()
    department = get('department', '').strip()
    skills = get('skills', '').strip()
    languages_speak = get('languages_speak', '').strip()
    computer_proficiency = get('computer_proficiency', '').strip()
    school_college = get('school_college', '').strip()
    grade_year = get('grade_year', '').strip()

    if family_id: members = members.filter(family__family_id__icontains=family_id)
    if member_id: members = members.filter(member_id__icontains=member_id)
    if name: members = members.filter(name__icontains=name)
    if member_type: members = members.filter(member_type__iexact=member_type)
    if gender: members = members.filter(gender__iexact=gender)
    
    if age and age.isdigit():
        import datetime
        today = datetime.date.today()
        birth_year = today.year - int(age)
        members = members.filter(date_of_birth__year=birth_year)

    if city: members = members.filter(family__area__city__name__icontains=city)
    if state: members = members.filter(family__area__city__state__name__icontains=state)
    if pincode: members = members.filter(family__pincode__icontains=pincode)
    
    if area: members = members.filter(family__area_id=area)
    if blood_group: members = members.filter(blood_group_id=blood_group)
    if qualification: members = members.filter(qualification_id=qualification)
    if income: members = members.filter(income_id=income)
    if health: members = members.filter(overall_health_id=health)
    if disease: members = members.filter(chronic_disease_id=disease)
    
    if mobile: members = members.filter(Q(mobile__icontains=mobile) | Q(family__mobile_no__icontains=mobile))
    if whatsapp: members = members.filter(whatsapp__icontains=whatsapp)
    if email_id: members = members.filter(email_id__icontains=email_id)
    if aadhaar_number: members = members.filter(Q(aadhaar_number__icontains=aadhaar_number) | Q(family__aadhar_no__icontains=aadhaar_number))
    
    if marital_status: members = members.filter(marital_status__icontains=marital_status)
    if occupation: members = members.filter(occupation__name__icontains=occupation)
    if company_name: members = members.filter(company_name__icontains=company_name)
    if designation: members = members.filter(designation__icontains=designation)
    if department: members = members.filter(department__icontains=department)
    if skills: members = members.filter(skills__icontains=skills)
    
    if languages_speak: members = members.filter(languages_speak__icontains=languages_speak)
    if computer_proficiency: members = members.filter(computer_proficiency__icontains=computer_proficiency)
    
    if school_college: members = members.filter(school_college_institute_name__icontains=school_college)
    if grade_year: members = members.filter(grade_year__icontains=grade_year)

    return members.distinct(), q

@login_required(login_url="/")
def advancereport(request):
    members, q = _get_advanced_filtered_members(request)

    context = {
        'members': members,
        'q': q,
        'total': members.count(),
        'areas': Area.objects.all(),
        'blood_groups': BloodGroup.objects.all(),
        'qualifications': Qualification.objects.all(),
        'incomes': Income.objects.all(),
        'health_statuses': OverallHealth.objects.all(),
        'diseases': ChronicDisease.objects.all(),
    }
    return render(request, 'advance-report.html', context)
"""

excel_code = """@login_required(login_url="/")
def export_advance_excel(request):
    members, q = _get_advanced_filtered_members(request)

    wb = openpyxl.Workbook()"""

pdf_code = """@login_required(login_url="/")
def export_advance_pdf(request):
    members, q = _get_advanced_filtered_members(request)

    import io"""

# Perform replacement for advancereport
patt1 = re.compile(r'@login_required\(login_url="/"\)\s*def advancereport\(request\):.*?return render\(request, \'advance-report\.html\', context\)', re.DOTALL)
if not patt1.search(content):
    print("Could not find advancereport")

content = patt1.sub(helper_code, content)

# Perform replacement for export_advance_excel
patt2 = re.compile(r'@login_required\(login_url="/"\)\s*def export_advance_excel\(request\):.*?wb = openpyxl\.Workbook\(\)', re.DOTALL)
if not patt2.search(content):
    print("Could not find export_advance_excel")

content = patt2.sub(excel_code, content)

# Perform replacement for export_advance_pdf
patt3 = re.compile(r'@login_required\(login_url="/"\)\s*def export_advance_pdf\(request\):.*?import io', re.DOTALL)
if not patt3.search(content):
    print("Could not find export_advance_pdf")

content = patt3.sub(pdf_code, content)

with open(r'f:\censes\censesapp\views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Refactored views.py successfully")
