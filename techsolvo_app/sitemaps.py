from django.contrib.sitemaps import Sitemap
from .models import Blog,Service,DeveloperType
from django.urls import reverse

class StaticSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return ['index', 'about', 'contact', 'newsletter', 'contact', 'team', 'faqs', 'privacy_policy']

    def location(self, item):
        return reverse(item)

class BlogSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8
    protocol = 'https'

    def items(self):
       return Blog.objects.all()

    def lastmod(self, obj):
        return obj.date_of_creation
        
    def location(self,obj):
        return f'/blog/{obj.slug}'

class ServiceSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8
    protocol = 'https'

    def items(self):
       return Service.objects.all()

    def lastmod(self, obj):
        return obj.created_at
        
    def location(self,obj):
        return f'/services/{obj.slug}'

class DeveloperTypeSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8
    protocol = 'https'

    def items(self):
       return DeveloperType.objects.all()

    def lastmod(self, obj):
        return obj.created_at
        
    def location(self,obj):
        return f'/hire-remote-developer/{obj.slug}'