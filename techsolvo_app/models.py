from unicodedata import category
from django.db import models
from django.db.models.aggregates import Max
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

from django.template.defaultfilters import slugify # new
from django.urls import reverse
import uuid


class RequestQuote(models.Model):
    full_name = models.CharField(max_length=50 ,blank=True, null=True)
    email = models.EmailField(max_length=50)
    phone_no = models.CharField(max_length=15)
    message = models.TextField()
    page_path = models.CharField(max_length=255, blank=True, null=True)
    honeypot = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.email} - {self.phone_no}"


class Contact(models.Model):
    first_name = models.CharField(max_length=50 ,blank=True, null=True)
    last_name = models.CharField(max_length=50 ,blank=True, null=True)
    email = models.EmailField(max_length=50)
    skype_whatsappno = models.CharField(max_length=50, null=True)
    phone_no = models.CharField(max_length=15)
    honeypot = models.CharField(max_length=100, blank=True, null=True)
    # budget = models.CharField(max_length=100)
    # file = models.FileField(upload_to='files/', null=True)
    message = models.TextField()

    def __str__(self):
        return self.email


class Student(models.Model):
    name = models.CharField(max_length=40 ,blank=True, null=True)
    email = models.EmailField(max_length=254)
    phone_no = models.CharField(max_length=10)
    skype_id = models.CharField(max_length=100)
    experience = models.CharField(max_length=500)
    position = models.CharField(max_length=500)
    file = models.FileField(upload_to='upload/',blank=True, null=True)

    def __str__(self):
        return self.email

class Newsletter(models.Model):
    email = models.CharField(max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    is_subscribe = models.BooleanField(default=True)

    def __str__(self) :
        return self.email

class JobOpenings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique= True)
    position_type = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    qualification = models.CharField(max_length=200)
    experience = models.CharField(max_length=100)
    skills = models.TextField()
    number_of_position = models.IntegerField()
    is_active = models.BooleanField(default=False)
    slug = models.SlugField(null=True, unique=True, blank=True)
    job_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{str(self.id)}-{self.position}'

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.position)
        super().save(*args, **kwargs)

class JobApply(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    contact_no = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    resume = models.FileField(upload_to='resume/')
    referral = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.email+' -- '+self.position

class Bloginsight(models.Model):
    blog_image = models.ImageField(upload_to='Blog/', blank=True, null=True)
    category = models.CharField(max_length=200)
    title = models.CharField(max_length=1000)
    description = models.TextField()

    def __str__(self):
        return f'{str(self.id)}-{self.category}'

class BlogCategories(models.Model):
    category = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True, unique=True)
    random_color = models.CharField(max_length=7, default='', blank=True)
    logo = models.ImageField(upload_to='img/', null=True, blank=True)
    show_on_homepage = models.BooleanField(default=False)

    # is_industry = models.BooleanField(default=False)

    def generate_random_color(self):
        unique_id = str(uuid.uuid4().hex)[:6]
        color = f"#{unique_id}"
        return color

    def __str__(self):
        return self.category

    def save(self, *args, **kwargs): # new
        if not self.random_color:
            self.random_color = self.generate_random_color()
        super(BlogCategories, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.category)
        return super().save(*args, **kwargs)

class Author(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='img/', null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    book_consultant_url = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

class Blog(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    short_desc = models.CharField(max_length=300)
    category = models.ForeignKey(BlogCategories, on_delete=models.CASCADE, null=True, blank=True)
    content = RichTextUploadingField()
    tags = models.CharField(max_length=200)
    heading_image = models.ImageField(upload_to='img/', blank=True, null=True)
    date_of_modification = models.DateField(auto_now=True)
    date_of_creation = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=True, unique=True, blank=True,max_length=500)
    view = models.IntegerField(default=0, null = True)
    is_industry = models.BooleanField(default=False)
    show_on_homepage = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_of_modification']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

class BlogComment(models.Model):
    full_name = models.CharField(max_length=100, null=False, blank=False)
    email = models.CharField(max_length=100, null=False, blank=False)
    phone = models.CharField(max_length=15, null=False, blank=False)
    query = models.TextField(null=False, blank=False)
    blog_name = models.ForeignKey(Blog, on_delete=models.CASCADE, null=False, blank=False)
    date_of_creation = models.DateField(auto_now=True, blank=False)

    def __str__(self):
        return self.full_name

class TeamImageCategory(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class TeamImage(models.Model):
    category = models.ForeignKey(TeamImageCategory, null=False, blank= False, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='team_photos/')
    description = models.TextField(blank=True)
    doc = models.DateField(auto_now=True)

class CompanyData(models.Model):
    company_name = models.CharField(max_length=100, blank=True, null=True, default=None)
    cin = models.CharField(primary_key=True ,max_length=100)
    email = models.CharField(max_length=100, blank=True, null=True, default=None)
    roc = models.CharField(max_length=50, blank=True, null=True, default=None)
    reg_no = models.CharField(max_length=100, blank=True, null=True, default=None)
    director = models.CharField(max_length=200, blank=True, null=True, default=None)
    address = models.TextField(blank=True, null=True, default=None)
    status = models.CharField(max_length=100, blank=True, null=True, default=None)
    activity = models.TextField(blank=True, null=True, default=None)
    director_info = models.URLField(blank=True, null=True, default=None)
    link = models.URLField(blank=True, null=True, default=None)
    category = models.CharField(max_length=100,blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    incorporate = models.DateField(default='1900-01-01')#CharField(max_length=50, blank=True, null=True, default=None)

    class Meta:
        ordering = ['-incorporate']

    def __str__(self):
        return self.company_name

    def save(self, **kwargs):
        cin = self.cin
        if cin and 'U01' == cin[0:3]:
            self.category = 'Agriculture, Hunting and Forestry'
        elif cin and 'U05' == cin[0:3]:
            self.category = 'Fishing'
        elif cin and 'U1' == cin[0:2] and int(cin[2])<=5:
            self.category = 'Mining and Quarrying'
        elif cin and 'U' == cin[0] or 'L' == cin[0] and int(cin[1])<=3:
            self.category = 'Manufacturing'
        elif cin and 'U4' == cin[0:2] and int(cin[2])<=1:
            self.category = 'Electricity, Gas, Water supply'
        elif cin and 'U45' == cin[0:3]:
            self.category = 'Construction'
        elif cin and 'U5' == cin[0:2] and int(cin[2])<5:
            self.category = 'Wholesale and Retail Trade'
        elif cin and 'U55' == cin[0:3]:
            self.category = 'Hotels and Restaurants'
        elif cin and 'U6' == cin[0:2] and int(cin[2])<5:
            self.category = 'Transport, Storage and Communications'
        elif cin and 'U6' == cin[0:2] and int(cin[2])>=5:
            self.category = 'Financial Intermediation'
        elif cin and 'U7' == cin[0:2] and int(cin[2])<5:
            self.category = 'Real Estate, Renting and Business Activities'
        elif cin and 'U75' == cin[0:3]:
            self.category = 'Public Administration and Defence'
        elif cin and 'U80' == cin[0:3]:
            self.category = 'Education'
        elif cin and 'U85' == cin[0:3]:
            self.category = 'Health and Social Work'
        elif cin and 'U9' == cin[0:2] and int(cin[2])<5:
            self.category = 'Other community and social service activity'
        elif cin and 'U99' == cin[0:3]:
            self.category = 'Extra Territorial Organizations'
        elif cin and 'U9' == cin[0:2] and int(cin[2])>=5:
            self.category = 'Household Activities'
        else:
            self.category = 'company'
        return super().save(**kwargs)

class ServiceCategory(models.Model):
    on_menu = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    description= RichTextField(null=True,blank=True)
    logo = models.ImageField(upload_to='service_category/', null=True, blank=True)
    service_title = models.CharField(max_length=100, null=True, blank=True)
    detail= RichTextField(null=True,blank=True)
    slug = models.SlugField(max_length=100, null=True, blank=True, unique=True)
    section_heading = models.CharField(max_length=100, null=True, blank=True)
    meta_desc = models.TextField(null=True, blank=True)
    meta_title = models.CharField(max_length=100, null=True, blank=True)
    meta_keyword = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('service-cat',kwargs={'slug':self.slug})

class Service(models.Model):
    name= models.CharField(max_length=200)
    description= RichTextField(blank=False)
    logo = models.ImageField(upload_to='service_types/', null=True, blank=True)
    service_title = models.CharField(max_length=100, null=True, blank=True)
    detail= RichTextField(blank=False)
    slug = models.SlugField(max_length=100, null=True, blank=True, unique=True)
    section_heading = models.CharField(max_length=100, null=True, blank=True)
    service_category = models.ManyToManyField(ServiceCategory, blank=True)
    meta_desc = models.TextField(null=True, blank=True)
    meta_title = models.CharField(max_length=100, null=True, blank=True)
    meta_keyword = models.CharField(max_length=150, null=True, blank=True)
    created_at= models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('service',kwargs={'slug':self.slug})

class ServiceSection(models.Model):
    # title = models.CharField(max_length=100, null=True, blank=True)
    service_type = models.ManyToManyField(Service, blank=True)
    service_category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, null=True, blank=True)
    logo = models.ImageField(upload_to='service_section/', null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = RichTextField(blank=False)

    def __str__(self):
        return self.name

class DeveloperCategory(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='developer_category/', null=True, blank=True)
    on_menu = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class DeveloperType(models.Model):
    name= models.CharField(max_length=200)
    description= RichTextField(blank=False)
    logo = models.ImageField(upload_to='developer_types/', null=True, blank=True)
    detail= RichTextField(blank=False)
    slug = models.SlugField(max_length=100, null=True, blank=True, unique=True)
    developer_category = models.ManyToManyField(DeveloperCategory, blank=True)
    meta_desc = models.TextField(null=True, blank=True)
    meta_title = models.CharField(max_length=100, null=True, blank=True)
    meta_keyword = models.CharField(max_length=150, null=True, blank=True)
    created_at= models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('courses',kwargs={'slug':self.slug})

class ServicePlatform(models.Model):
    service_type = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    service_category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, null=True, blank=True)
    logo = models.ImageField(upload_to='platform_logo/', null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    page_link = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True)
    developer = models.ForeignKey(DeveloperType, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class FrequentlyAskedQuestion(models.Model):
    LISTING_PAGE_CHOICES = (
        ('FAQ Page', 'FAQ Page'),
        ('Home Page', 'Home Page')
    )
    question = models.CharField(max_length=200, null=True, blank=True)
    answers = RichTextField(blank=False)
    listing_page =  models.CharField(max_length=200, choices=LISTING_PAGE_CHOICES,null=True,blank=True)
    developer_type = models.ForeignKey(DeveloperType, on_delete=models.CASCADE, null=True, blank=True)
    service_type = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.question

class BusinessArea(models.Model):
    logo = models.ImageField(upload_to='buisness_area/', null=True, blank=True)
    short_desc = models.CharField(max_length=300)

    def __str__(self):
        return self.short_desc

class TechsolvoClient(models.Model):
    name=models.CharField(max_length=200, null=True, blank=True)
    client_image = models.ImageField(upload_to='clients/', null=True, blank=True)

    def __str__(self):
        return self.name

class PageContent(models.Model):
    PAGE_CHOICES = (
        ('Home Page', 'Home Page'),
        ('Hire Developer Page', 'Hire Developer Page'),
        ('Service Page', 'Service Page'),
        ('FAQ Page', 'FAQ Page'),
    )
    name= models.CharField(max_length=200)
    description= RichTextField(blank=False)
    listing_page =  models.CharField(max_length=200, choices=PAGE_CHOICES,null=True,blank=True)
    page_title = models.CharField(max_length=500,null=True,blank=True)
    meta_desc = models.TextField(null=True, blank=True)
    meta_title = models.CharField(max_length=500, null=True, blank=True)
    meta_keyword = models.TextField(null=True, blank=True)
    created_at= models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('courses',kwargs={'slug':self.slug})

class SocialLink(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='social_links/', null=True, blank=True)
    link = models.CharField(max_length=500)

    def __str__(self):
        return self.name
