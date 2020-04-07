from django.contrib.sitemaps import Sitemap
from .models import Poem
 
 
class PostSitemap(Sitemap):    
    changefreq = "monthly"
    priority = 0.9
 
    def items(self):
        return Poem.objects.all()
 
    def lastmod(self, obj):
        return obj.published_at