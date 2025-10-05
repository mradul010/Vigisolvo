from requests_html import HTMLSession
from time import sleep
import csv23 as csv, requests

session = HTMLSession()

def retrieve_data(href):
    c_url= session.get(href)
    try:
        cin = c_url.html.find('table thead tr td p')[1].text
    except:
        try:
            cin = c_url.html.find('table thead tr td p')[1].text
        except:
            cin = None
    try:
        name = c_url.html.find('table tbody tr td p')[1].text
    except:
        try:
            name = c_url.html.find('table tbody tr td p')[1].text
        except:
            name = None
            pass
    try:
        incorporation_date = c_url.html.find('table tbody tr')[7].find('td p')[1].text
    except:
        try:
            incorporation_date = c_url.html.find('table tbody tr')[7].find('td p')[1].text
        except:
            incorporation_date = None
            pass
    try:
        add = c_url.html.find('div.col-12')[0] 
        address = add.find('div div p')[3].text
        email = add.find('div div p')[0].text.split(':')[1].replace('"', '')
    except:
        try:
            add = c_url.html.find('div.col-12')[0] 
            address = add.find('div div p')[3].text
            email = add.find('div div p')[0].text.split(':')[1].replace('"', '')
        except:
            add = None
            address = None
            email = None
            pass
    try:
        roc = c_url.html.find('table tbody tr')[2].find('td p')[1].text
    except:
        try:
            roc = c_url.html.find('table tbody tr')[2].find('td p')[1].text
        except:
            roc = None
            pass
    try:
        reg = c_url.html.find('table tbody tr')[3].find('td p')[1].text
    except:
        try:
            reg = c_url.html.find('table tbody tr')[3].find('td p')[1].text
        except:
            reg = None
            pass
    try:
        activity = c_url.html.find('table tbody tr')[9].find('td p')[1].text
    except:
        try:
            activity = c_url.html.find('table tbody tr')[7].find('td p')[1].text
        except:
            activity = None
            pass
    try:
        if c_url.html.find('.col-lg-12 table tbody')[-1].find('tr td p')[1]:
            director_name = c_url.html.find('.col-lg-12 table tbody')[-1].find('tr td p')[1].text
            director_info = c_url.html.find('.col-lg-12 table tbody')[-1].find('tr td p')[1].find('a')[0].attrs['href']
            # print(director_name, director_info)
    except:
        director_name = None
        director_info = None
        pass
    df = {'cin':cin, 'link':href, 'company_name':name, 'incorporate':incorporation_date, 'email':email, 'roc':roc, 'reg_no':reg, 'director':director_name, 'director_info':director_info, 'activity':activity, 'address':address, 'category': ''}
    return df

def call_retrieve(link):
    url = 'https://techsolvo.com/companies/'
    href = link.attrs['href']
    data = retrieve_data(href)
    response = requests.post(url , data=data)
    # with open('data.csv', 'a+', newline='', encoding='utf-8') as csvfile:
    #     csv_writer = csv.DictWriter(csvfile, fieldnames=data.keys())
    #     if csvfile.tell() == 0:
    #         csv_writer.writeheader()
    #     ava_data = False
    #     csvfile.seek(0)
    #     csv_reader = csv.DictReader(csvfile)
    #     for row in csv_reader:
    #         if data['Name'] == row['Name']:
    #            ava_data = True
    #     if not ava_data:
    #         csv_writer.writerow(data)
    #     else:
    #         print("available")


# time = 12:36PM - 12:43PM 38, 12:46PM 39- https://www.zaubacorp.com/company-list/nic-722/city-BANGALORE-company.html