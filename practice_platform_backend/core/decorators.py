def cors_exempt(func):
    """
    This decorator currently has bad compatibility with the REST framework.
    """

    def wrap(request, *arg, **args):
        res = func(request, *arg, **args)
        res["Access-Control-Allow-Credentials"] = "true"

        # Allow all methods
        res["Access-Control-Allow-Methods"] = "*"

        # Allow all origins
        res["Access-Control-Allow-Origin"] = request.headers.get("Origin")
        return res

    wrap.__name__ = func.__name__
    return wrap
