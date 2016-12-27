def requires_authentication(requires_token=False):
    def wrapper(func, *args, **kwargs):
        if requires_token:
            if args or kwargs:
                token = kwargs.get('auth_key', args[0] if args else None)
                if not token:
                    raise Exception()
            else:
                raise Exception()
        # TODO: Token check
        return func
    return wrapper
