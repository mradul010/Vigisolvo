from django.http.response import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.views.decorators.csrf import csrf_exempt
import json, csv23 as csv
from time import sleep
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.template.loader import render_to_string
from email.mime.application import MIMEApplication
import urllib.parse
import urllib.request
from django.contrib import messages
from .serializers import CompanySerializer
from rest_framework.generics import GenericAPIView
from rest_framework.response  import Response
from requests_html import HTMLSession
from .zauba_dynamic import call_retrieve
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
import os

def common_base():
    service_categories = ServiceCategory.objects.filter(on_menu = True)
    services = Service.objects.filter(service_category__in = service_categories)
    developer_category = DeveloperCategory.objects.filter(on_menu=True)
    developer_type = DeveloperType.objects.filter(developer_category__in = developer_category)
    insights = Blog.objects.filter(is_industry = False).order_by('-date_of_creation')[:3]
    clients=TechsolvoClient.objects.all()
    industry = Blog.objects.filter(is_industry=True)
    social_links = SocialLink.objects.all()
    context={
        "service_category":service_categories,
        "services":services,
        "developer_category":developer_category,
        "developer_type":developer_type,
        "insights":insights,
        "clients":clients,
        "industry":industry,
        "social_links":social_links
    }
    return context


def error_404_view(request, exception):
    page_title = "ERROR | Techsolvo"
    data = {"name": "techsolvo.com",'page_title':page_title}
    data.update(common_base())
    return render(request,'error_404.html', data)

def about(request):
    page_title = "About US | Techsolvo"
    context={"page_title":page_title}
    context.update(common_base())
    return render(request, 'about-us.html',context)

def dashboard(request):
    page_title = "Dashboard | Techsolvo"
    context={"page_title":page_title}
    context.update(common_base())
    return render(request, 'dashboard.html',context)

def erp_retail(request):
    page_title = "ERPNext for Retail | TechSolvo ERP Solutions"
    context={"page_title":page_title}
    context.update(common_base())
    return render(request, 'erp-retail.html',context)

def erp_services(request):
    page_title = "ERPNext for Service Industry | TechSolvo ERP Solutions"
    context={"page_title":page_title}
    context.update(common_base())
    return render(request, 'erp-services.html',context)

def erp_manufacturing(request):
    page_title = "ERPNext for Manufacturing | TechSolvo ERP Solutions"
    context={"page_title":page_title}
    context.update(common_base())
    return render(request, 'erp-manufacturing.html',context)

def frappe_hrms(request):
    page_title = "Frappe HRMS | Streamlined HR & Payroll Solutions for Businesses"
    context={"page_title":page_title}
    context.update(common_base())
    return render(request, 'frappe_hrms.html',context)

def erp_dist(request):
    page_title = "ERPNext for Distribution | TechSolvo ERP Solutions"
    context={"page_title":page_title}
    context.update(common_base())
    return render(request, 'erp-distribution.html',context)

def erp_healthcare(request):
    page_title = "ERPNext for Healthcare | TechSolvo ERP Solutions"
    context={"page_title":page_title}
    context.update(common_base())
    return render(request, 'erp-healthcare.html',context)

def erp_education(request):
    page_title = "ERPNext for Education | TechSolvo ERP Solutions"
    context={"page_title":page_title}
    context.update(common_base())
    return render(request, 'erp-education.html',context)

def privacy_policy(request):
    page_title = "Our Privacy Policy | Techsolvo"
    context={"page_title":page_title}
    context.update(common_base())
    return render(request, 'privacy-policy.html',context)

def index(request):
    page_content = PageContent.objects.filter(listing_page = "Home Page")
    homepage_blogs = Blog.objects.filter(
        Q(show_on_homepage=True) & Q(category__show_on_homepage=True)
    )
    categories = BlogCategories.objects.filter(show_on_homepage=True)
    context = common_base()
    if page_content:
        context.update(
            {
                "page_content":page_content[0],
                "page_meta_title":page_content[0].meta_title,
                "page_meta_description":page_content[0].meta_desc,
                "page_meta_keyword": page_content[0].meta_keyword
            }
        )
    if homepage_blogs:
        context['homepage_blogs'] = homepage_blogs
        context['categories'] = categories
    return render(request,'index.html', context)

def apply(request, slug):
    if request.method == "POST":
        try:
            name = request.POST.get('dzName')
            applier_email = request.POST.get('dzEmail')
            phone_no = request.POST.get('Phone')
            referral = request.POST.get('referred')
            experience = request.POST.get('dzex')
            position = request.POST.get('dzposition')
            file = request.FILES.get('file')

            if file:
                file_size = file.size / 1024 ** 2
                if file_size > 10:
                    return JsonResponse({'error': 'You can upload a maximum 10 MB file, please reduce file size and upload again.'})
            else:
                return JsonResponse({'error': 'No file uploaded.'})

            if all([name, applier_email, phone_no, experience, position]):
                ins = JobApply(fullname=name, email=applier_email, contact_no=phone_no, experience=experience, resume=file, position=position, referral=referral)
                ins.save()

                # Send mail to HR
                message = 'Below are the details of the candidate'
                subject = f'Job Application: {position} - {name}'
                from_email = str(settings.EMAIL_HOST_USER)
                hr_email = 'hr@techsolvo.com'
                hr_context = {
                    'name': name,
                    'email': applier_email,
                    'phone': phone_no,
                    'experience': experience,
                    'referral': referral
                }
                html_content = render_to_string("send_apply_details.html", hr_context)
                email = EmailMultiAlternatives(subject, message, from_email, [hr_email])
                email.attach_alternative(html_content, "text/html")

                # Attach the resume file
                file.seek(0)  # Ensure file pointer is at the start
                pdf_attachment = MIMEApplication(file.read(), _subtype='pdf')
                pdf_attachment.add_header('Content-Disposition', 'attachment', filename=file.name)
                email.attach(pdf_attachment)
                email.send()

                # Send mail to the applier
                applier_context = {'name': name}
                applier_content = render_to_string("send_mail_to_applier.html", applier_context)
                applier_email_message = EmailMultiAlternatives(subject, message, from_email, [applier_email])
                applier_email_message.attach_alternative(applier_content, "text/html")
                applier_email_message.send()

                return JsonResponse({'status': 1})
            else:
                return JsonResponse({'error': 'Please fill all the fields.'})
        except Exception as e:
            return JsonResponse({'status': 0, 'error': str(e)})
    else:
        job = JobOpenings.objects.filter(slug=slug).first()
        page_title = "Apply for | Techsolvo"
        context = {'slug': slug, 'job': job, 'page_title': page_title}
        context.update(common_base())
        return render(request, 'apply.html', context)
    
# def career(request):
#     job = JobOpenings.objects.all()
#     job_openings_data = JobOpenings.objects.filter(is_active=1)
#     page_title = "Career | Techsolvo"
#     context = {'job':job,'job_openings': job_openings_data,"page_title":page_title}
#     context.update(common_base())
#     return render(request,'career.html', context)

@csrf_exempt
def newsletter(request):
    if request.method == 'POST':
        email = request.POST.get("email", None)
        if email != '' :
            ins = Newsletter(email=email)
            ins.save()
            return JsonResponse({'status':1})
        else:
            return JsonResponse({'error':'Please Fill All the Fields'})

    return render(request, 'base.html')

def sitemap(request):
    return render(request,'sitemap.html')

@csrf_exempt
def contact(request):
    if request.method == "POST":
        first_name = request.POST.get('dzName')
        last_name = request.POST.get('dzLName')
        email = request.POST.get('dzEmail')
        skype_whatsappno = request.POST.get('dzSid')
        phone_no = request.POST.get('Phone')
        honeypot_field = request.POST.get('city', '')
        message = request.POST.get('dzMessage')
        verify = recaptcha(request)

        if honeypot_field:
            return JsonResponse({'error':'Spam detected!'}, status=400) 
                
        if verify == True:
            Contact.objects.create(first_name=first_name, last_name=last_name, email=email,
                                skype_whatsappno=skype_whatsappno, phone_no=phone_no, message=message)   
            
            #Email_format
            subject = f"Contact Form Submission from {first_name} {last_name}"
            body = f"""
            You have received a new message from the contact form on your website.
            First Name: {first_name}
            Last Name: {last_name}
            Email: {email}
            Message:
            {message}
            """
            
            from_email = settings.EMAIL_HOST_USER            
            recipient_list = ['mradul.mishra@vigisolvo.com'] 
            
            send_mail(subject, body, from_email, recipient_list)
            
            return JsonResponse({'status': 'success', 'message': "We have received your message."})
        else:
            return JsonResponse({'error': 'Please fill all the fields and complete reCAPTCHA'})

    page_title = "Contact Us | Techsolvo"
    context = {"page_title":page_title}
    context.update(common_base())
    return render(request, 'contact.html',context)

def faqs(request):
    page_title = "FAQ's | Techsolvo"
    frequently_asked_question = FrequentlyAskedQuestion.objects.filter(listing_page = "FAQ Page")
    page_content = PageContent.objects.filter(listing_page='FAQ Page')
    context = {"page_title":page_title, "frequently_asked_question":frequently_asked_question}
    if page_content:
        context.update(
            {
                "page_content":page_content[0],
                "page_meta_description":page_content[0].meta_desc,
                "page_meta_keyword": page_content[0].meta_keyword
            }
        )
    context.update(common_base())
    return render(request, 'faqs.html',context)

def iphone(request):
    page_title = "iPhone Development Company | Techsolvo"
    context = {"page_title":page_title}
    context.update(common_base())
    return render(request, 'iphone-app-development.html',context)

def our_vision(request):
    page_title = "Our Vision | Techsolvo"
    context = {"page_title":page_title}
    context.update(common_base())
    return render(request, 'our-vision-n-mission.html',context)

def travel(request):
    page_title = "Travel Development Company | Techsolvo"
    context = {"page_title":page_title}
    context.update(common_base())
    return render(request, 'travel.html',context)

def teams(request):
    page_title = "Teams | Techsolvo"
    context = {"page_title":page_title}
    context.update(common_base())
    return render(request, 'teams.html',context)

def blog(request):
    blog = Blog.objects.filter(is_industry = False).order_by('-date_of_creation')
    categories = BlogCategories.objects.all()
    page_title = "Blogs of the Day | Techsolvo"

    page = request.GET.get('page', 1)
    paginator = Paginator(blog,10)
    try:
        filters = paginator.page(page)
    except PageNotAnInteger:
        filters = paginator.page(1)
    except EmptyPage:
        filters = paginator.page(paginator.num_pages)

    context = {
        "blog":blog,
        "categories":categories,
        "page_title":page_title,
        'filters':filters
    }
    context.update(common_base())
    return render(request, 'blog.html', context)

def sort_blog(request, slug):
    blog = Blog.objects.filter(category__slug=slug).filter(is_industry=False).order_by('-date_of_creation')
    categories = BlogCategories.objects.all()
    page_title = "Blogs of the Day | Techsolvo"

    page = request.GET.get('page', 1)
    paginator = Paginator(blog,10)
    try:
        filters = paginator.page(page)
    except PageNotAnInteger:
        filters = paginator.page(1)
    except EmptyPage:
        filters = paginator.page(paginator.num_pages)

    context = {
        "blog":blog,
        "page_title":page_title,
        "categories":categories,
        'filters':filters
    }
    context.update(common_base())
    return render(request, 'blog.html', context)

def typesearch(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        search_blog = Blog.objects.filter(category__is_industry=False).filter(
            title__icontains=search_str) | Blog.objects.filter(
            author__istartswith=search_str) | Blog.objects.filter(
            short_desc__icontains=search_str) | Blog.objects.filter(
            content__icontains=search_str)| Blog.objects.filter(
            tags__icontains=search_str) | Blog.objects.filter(
            heading_image__icontains=search_str) |  Blog.objects.filter(
            date_of_creation__icontains=search_str) |  Blog.objects.filter(
            slug__icontains=search_str)
        data = search_blog.values()
        return JsonResponse(list(data),safe=False)

def singleblog(request, category_id, blog_slug):
    thisblog = Blog.objects.get(slug=blog_slug)
    if thisblog.view == 0 :
        thisblog.view = 1
        thisblog.save()
    else :
        thisblog.view += 1
        thisblog.save()
    context = {'thisblog':thisblog}
    context.update(common_base())
    return render(request, 'singleBlog.html',context)

@csrf_exempt
def request_quote(request):
    if request.method == "POST":
        full_name = request.POST.get('dzName')
        email = request.POST.get('dzEmail')
        phone_no = request.POST.get('dzPhone')
        message = request.POST.get('dzMessage', '')
        honeypot_field = request.POST.get('city', '')
        verify = recaptcha(request)
        page_path = request.META.get('HTTP_REFERER', '')  

        if honeypot_field:
            return JsonResponse({'error': 'Spam detected!'}, status=400)        

        if verify == True:
            RequestQuote.objects.create(
                full_name=full_name, 
                email=email, 
                phone_no=phone_no, 
                message=message,
                page_path=page_path
            )

            admin_subject = f"New Quote Request from: {full_name}"
            admin_message = f"""
            Name: {full_name}
            Email: {email}
            Phone: {phone_no}
            Message: {message}
            """

            from_email = settings.EMAIL_HOST_USER
            recipient_list = ['mradul.mishra@vigisolvo.com']

            html_message = render_to_string("quote_email.html", {
                'full_name': full_name,
                'email': email,
                'phone_no': phone_no,
                'message': message,
                'page_path': page_path
            })

            send_mail(
                subject=admin_subject,
                message=admin_message,
                from_email=from_email,
                recipient_list=recipient_list,
                html_message=html_message,
            )

            response_data = {'status': 'success', 'message': "We have received your message."}
            return JsonResponse(response_data)
        
    return JsonResponse({'error': 'Please Fill All the Fields and complete reCaptcha'})

#     if request.method == "POST":
#         full_name = request.POST.get('dzName')
#         email = request.POST.get('dzEmail')
#         phone_no = request.POST.get('dzPhone')
#         message = request.POST.get('dzMessage', '')
#         honeypot_field = request.POST.get('city', '')
#         verify = recaptcha(request)

       
#         if honeypot_field:
#             return JsonResponse({'error': 'Spam detected!'}, status=400)        

#         if verify == True or verify == False:
#             RequestQuote.objects.create(
#             full_name=full_name, 
#             email=email, 
#             phone_no=phone_no, 
#             message=message,
#             page_path=page_path
#         )

#             admin_subject = f"New Quote Request: {full_name}"
#             admin_message = f"""
#             Name: {full_name}
#             Email: {email}
#             Phone: {phone_no}
#             Message: {message}
#             """

#             from_email = settings.EMAIL_HOST_USER
#             recipient_list = ['kjoshi030603@gmail.com']

#             html_message = render_to_string("quote_email.html", {
#                 'full_name': full_name,
#                 'email': email,
#                 'phone_no': phone_no,
#                 'message': message,
#                 'page_path':page_path
#             })

#             send_mail(
#                 subject=admin_subject,
#                 message=admin_message,
#                 from_email=from_email,
#                 recipient_list=recipient_list,
#                 html_message=html_message,
#             )

#             response_data = {'status': 'success', 'message': "We have received your message."}
        
#         return JsonResponse(response_data)
#     else:
#         return JsonResponse({'error': 'Please Fill All the Fields and complete reCaptcha'})
    
def recaptcha(request):
    #Begin reCAPTCHA validation
    recaptcha_response = request.POST.get('g-recaptcha-response')
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
        'secret': settings.RECAPTCHA_PRIVATE_KEY,
        'response': recaptcha_response
    }
    data = urllib.parse.urlencode(values).encode('utf-8')
    req = urllib.request.Request(url, data)
    response = urllib.request.urlopen(req)
    result = json.load(response)

    if result['success']:
        return True
    else:
        return False

@csrf_exempt
def get_data(request):
    global stop
    stop = True
    if request.method == 'GET':
        response = HttpResponse()
        response['X-Frame-Options'] = 'DENY'
        stop = False
        return response
    if request.method == 'POST':
        session = HTMLSession()
        url = 'https://www.zaubacorp.com/company-list/'
        r = session.get(url)
        res = r.html

        # number of pages
        ele = res.find(':contains(">>")')[-1]
        nxt = ele.attrs['href'].split('-')[-2]
        try:
            if open('page.txt', 'r'):
                file = open('page.txt', 'r')
                p = int(file.read())
        except:
            p = int(1)

        while int(p) <= int(nxt) and stop:
            n=int(p)
            try:
                page = session.get(f'https://www.zaubacorp.com/company-list/p-{p}-company.html')
                # print(f"\ron page {p}", end="")
                links = page.html.find('td a')
                for link in links:
                    if stop:
                        call_retrieve(link)
                # print('\ndone')
            except Exception as e:
                sleep(5)
                p=int(n)
                page = session.get(f'https://www.zaubacorp.com/company-list/p-{p}-company.html')
                # print(f"\ron page {p}", end="")
                links = page.html.find('td a')
                for link in links:
                    if stop:
                        call_retrieve(link)
                # print('\ndone')
            p=int(p)+1
            with open('page.txt', 'w') as file:
                file.write(str(p))
                file.close()
            if int(p)==int(nxt)+1:
                file.write('')
                file.close()
        return render(request, 'index.html')

def ServiceView(request,service):
    try:
        each_service = Service.objects.get(slug = service)
    except:
        each_service = ServiceCategory.objects.get(slug=service)
    frequently_asked_questions = FrequentlyAskedQuestion.objects.filter(service_type__slug = service)
    context = {"each_service":each_service, "frequently_asked_questions":frequently_asked_questions}
    if each_service:
        try:
            get_platform = ServicePlatform.objects.filter(service_type = each_service)
            service_section = ServiceSection.objects.filter(service_type = each_service)
        except:
            get_platform = ServicePlatform.objects.filter(service_category = each_service)
            service_section = ServiceSection.objects.filter(service_category = each_service)
        section_topic = each_service.section_heading or ""
        buisness_areas = BusinessArea.objects.all()
        context.update({"platform":get_platform,"section_topic":section_topic,"service_section":service_section,"buisness_areas":buisness_areas})
    context.update(common_base())
    return render(request, 'service_page.html', context)

def HireDeveloperView(request,developer):
    each_developer = DeveloperType.objects.get(slug = developer)
    frequently_asked_questions = FrequentlyAskedQuestion.objects.filter(developer_type__slug = developer)
    context = {"each_developer":each_developer, "frequently_asked_questions":frequently_asked_questions}
    context.update(common_base())
    return render(request, 'hire_developer.html',context)

def developer_category(request):
    page_content = PageContent.objects.filter(listing_page = "Hire Developer Page")
    developer_cat = DeveloperCategory.objects.all()
    developer_dict = {}

    for develop in developer_cat:
        types = DeveloperType.objects.filter(developer_category=develop)
        developer_dict[develop] = [
            {'name': dev_type.name, 'slug': dev_type.slug, 'type_logo':dev_type.logo}
            for dev_type in types
        ]

    context = {"developer_dict": developer_dict} #,"page_content":page_content}
    if page_content:
        context.update(
            {
                "page_content":page_content[0],
                "page_meta_title":page_content[0].meta_title,
                "page_meta_description":page_content[0].meta_desc,
                "page_meta_keyword": page_content[0].meta_keyword
            }
        )
    context.update(common_base())

    return render(request, 'hire_developer_category.html', context)

def service_category(request):
    page_content = PageContent.objects.filter(listing_page = "Service Page")
    service_cat = ServiceCategory.objects.all()
    service_dict = {}

    for develop in service_cat:
        types = Service.objects.filter(service_category=develop)
        service_dict[develop] = [
            {'name': dev_type.name, 'slug': dev_type.slug, 'type_logo':dev_type.logo}
            for dev_type in types
        ]

    context = {"service_dict": service_dict} #,"page_content":page_content}
    if page_content:
        context.update(
            {
                "page_content":page_content[0],
                "page_meta_title":page_content[0].meta_title,
                "page_meta_description":page_content[0].meta_desc,
                "page_meta_keyword": page_content[0].meta_keyword
            }
        )
    context.update(common_base())

    return render(request, 'service_category.html', context)

class CompanyView(GenericAPIView):
    serializer_class = CompanySerializer
    queryset = CompanyData.objects.all()

    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="dataser.csv"'
        writer = csv.writer(response)

        company_data = CompanyData.objects.all()#self.get_queryset()
        serialized_data = self.get_serializer(company_data, many=True)#.data  # Extract data from serializer
        if serialized_data:
            headers = list(serialized_data.data[0].keys())
            writer.writerow(headers)

            # Write data rows to the CSV file
            for data_row in serialized_data:
                writer.writerow(data_row.values())

        return response

    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print(serializer.errors)
            return Response(serializer.errors)


def hire_remote_erpnext_developer(request):
    page_title = "Hire Remote ERPNext Developer | Techsolvo"
    context = {"page_title": page_title}
    context.update(common_base())
    return render(request, 'hire-remote-erpnext-developer.html', context)