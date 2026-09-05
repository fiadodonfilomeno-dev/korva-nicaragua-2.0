from django.http import HttpResponse, JsonResponse
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


@require_GET
def assetlinks(request):
    """Verificación de dominio para el TWA de Android (Play Store / instalación directa).
    El fingerprint corresponde al keystore generado por PWABuilder."""
    data = [
        {
            "relation": ["delegate_permission/common.handle_all_urls"],
            "target": {
                "namespace": "android_app",
                "package_name": "com.onrender.korva_nicaragua_2_0_1.twa",
                "sha256_cert_fingerprints": [
                    "B9:F1:52:ED:81:C9:96:A3:92:E5:2C:A9:5D:DA:D1:38:56:D5:C0:5F:6D:AB:FC:E9:89:24:A5:5F:E4:B4:97:A2"
                ],
            },
        }
    ]
    return JsonResponse(data, safe=False)