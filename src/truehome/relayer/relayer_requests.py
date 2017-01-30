from functools import wraps


def true_home_api(permission_needed):
    def api_decorator(func, **kwargs):
        @wraps(func)
        def wrapper(**kwargs):
            if permission_needed or not permission_needed:
                # Can the user perform the action?
                # Validation goes here.
                return func(**kwargs)

        return wrapper
    return api_decorator
