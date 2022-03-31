def validate_account_info(request):
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")

    if not (username and email and password):
        raise Exception("Please complete the form.")
    # Need more validation
