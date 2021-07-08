def create_token(*args):
    from django.conf import settings
    components = tuple([settings.SECRET_KEY, *args])
    return str(hash(components))
