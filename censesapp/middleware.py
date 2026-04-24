from datetime import datetime, date
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from .models import AddUser, VolunteerAllocation


class VolunteerSessionCheckMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated:

            try:
                profile = AddUser.objects.get(user=request.user)

                if profile.role == "volunteer":

                    allocations = VolunteerAllocation.objects.filter(
                        volunteer=profile,
                        start_date__lte=date.today(),
                        end_date__gte=date.today()
                    )

                    now = datetime.now().time()

                    active = False

                    for a in allocations:
                        if a.start_time and a.end_time:
                            if a.start_time <= now <= a.end_time:
                                active = True
                                break
                        else:
                            # If no times are set, assume 24-hour access for that day
                            active = True
                            break

                    if not active:
                        logout(request)
                        messages.error(request, "Your allocated time is over.")
                        return redirect("login")

            except AddUser.DoesNotExist:
                pass

        return self.get_response(request)



class VolunteerAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                # Use filter().first() to avoid DoesNotExist if possible
                profile = AddUser.objects.filter(user=request.user).first()

                if profile and profile.role == "volunteer":
                    # Added /update-member/ and ensured /memberlist/ is strictly checked
                    allowed_urls = [
                        "/addfamily",
                        "/memberlist",
                        "/update-member", # This covers /update-member/9/
                        "/get-location",
                        "/incompletemember",
                        "/logout",
                        "/static",
                        "/media",
                        "/edit-member",
                        "/viewmember",
                        "/viewfamily",
                        "/volunteer-familylist",
                        "/volunteer-viewfamily",
                    ]

                    # Normalize path: remove trailing slash for comparison
                    path = request.path.rstrip('/')
                    
                    # Special check: If path is empty (root), redirect to addfamily
                    if path == "":
                        return redirect("/addfamily/")

                    # If the current path doesn't start with any allowed URL, block it
                    is_allowed = any(request.path.startswith(url) for url in allowed_urls)
                    
                    if not is_allowed:
                        messages.error(request, "Access denied.")
                        return redirect("/addfamily/")

            except Exception as e:
                print(f"Middleware Error: {e}")

        response = self.get_response(request)
        return response



 