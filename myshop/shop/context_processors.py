from .models import SiteSettings

def site_settings(request):
    settings = SiteSettings.objects.first()
    return {
        'shop_name': settings.shop_name if settings else 'My Shop'
    }
