from wsmeext.pecan import wsexpose


def expose(*args, **kwargs):
    if 'rest_content_types' not in kwargs:
        kwargs['rest_content_types'] = ('json',)

    return wsexpose(*args, **kwargs)