from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email, validate_slug

from .models import user as User


def validate_account_info(request):
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")

    try:
        validate_slug(username)
    except:
        raise Exception(
            "An username can only contains letters, numbers, underscores or hyphens."
        )
    validate_email(email)
    validate_password(password)

    if not (username and email and password):
        raise Exception("Please complete the form.")
    elif len(User.objects.filter(username=username)) > 0:
        raise Exception("Duplicated username.")
    elif len(User.objects.filter(email=email)) > 0:
        raise Exception("Duplicated email.")
