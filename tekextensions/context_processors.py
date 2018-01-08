from django.conf import settings


# noinspection PyUnusedLocal
def static_url_prefix(request):
    return {'STATIC_URL': settings.STATIC_URL}


def current_site(request):
    """
    A context processor to add the "current_site" to the current Context

    """
    from django.contrib.sites.models import Site, RequestSite

    context_name = 'CURRENT_SITE'

    try:
        site = Site.objects.get_current()
        return {context_name: site}
    except Site.DoesNotExist:
        # always return a dict, no matter what!
        return {context_name: RequestSite(request)}

