from django.contrib import admin
from .models import *

class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

class Adminblogcomment(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'blog_name']

@admin.register(CompanyData)
class CompanyData(admin.ModelAdmin):
    list_display = ('cin', 'company_name', 'email', 'incorporate')
    search_fields = ('company_name', 'cin', 'status', 'director','activity', 'roc', 'category', 'incorporate', 'created_on')
    list_filter = ('category', 'roc')

@admin.register(RequestQuote)
class AdminRequestQuote(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_no', 'message', 'page_path')

admin.site.register(Contact)
admin.site.register(Newsletter)
admin.site.register(Student)
admin.site.register(JobOpenings)
admin.site.register(Bloginsight)
admin.site.register(JobApply)
admin.site.register(Author)
admin.site.register(Blog,BlogAdmin)
admin.site.register(BlogCategories)
admin.site.register(BlogComment, Adminblogcomment)
admin.site.register(TeamImage)
admin.site.register(TeamImageCategory)
admin.site.register(ServiceCategory)
admin.site.register(Service)
admin.site.register(ServicePlatform)
admin.site.register(ServiceSection)
admin.site.register(DeveloperCategory)
admin.site.register(DeveloperType)
admin.site.register(FrequentlyAskedQuestion)
admin.site.register(BusinessArea)
admin.site.register(TechsolvoClient)
admin.site.register(PageContent)
admin.site.register(SocialLink)