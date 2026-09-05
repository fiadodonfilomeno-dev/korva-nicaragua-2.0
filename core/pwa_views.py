from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.template import loader


@require_GET
def service_worker(request):
    """Sirve el Service Worker desde la raíz para que tenga alcance global /"""
    template = loader.get_template('pwa/sw.js')
    manifest = "/static/pwa/manifest.json"
    return HttpResponse(
        template.render({'manifest_url': manifest}, request),
        content_type='application/javascript; charset=utf-8',
        headers={'Service-Worker-Allowed': '/'},
    )