from django.core.mail import EmailMessage
from jobs.models import Job, Request_Payment
from expenses.models import Expenses
from crontab import CronTab
from django.conf import settings
from botocore.client import Config
import boto3
import botocore
import csv
import io
import os
import zipfile
# import getpass
# import datetime
# import sys

def send_data_email(user_email, title, queryset, request, form_vals={}):
    """sends data through email in a zip and csv file"""
    #create email
    email = EmailMessage(form_vals['subject'], form_vals['message'], user_email, [form_vals['send_to']])

    #generate csv and attach to email
    csv = generate_csv(title=title, queryset=queryset, request=request)
    email.attach('data.csv', csv, 'text/csv')


    #generate zip
    # zip_file = generate_zip(document_links=result[0])
    # email.attach('files.zip', zip_file, 'application/x-zip-compressed')

    #send email
    email.send(fail_silently=False)

def generate_file_url(document_link):
    """Generates file url"""
    Config.signature_version = botocore.UNSIGNED
    return boto3.client('s3', settings.AWS_S3_REGION_NAME, config=Config(s3={'addressing_style': 'path'})).generate_presigned_url('get_object', ExpiresIn=3600, Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': str(document_link)})


def get_attributes_and_headers(object, request):
    """
    Returns a tuple with the desired values from objects and headings for the csv file
    based on the instance type
    """
    if isinstance(object, Job):
        file_url = generate_file_url(document_link=object.document_link)
        headers    = ('House', 'Company', 'Start Amount', 'Balance', 'Submit Date', 'Total Paid', 'Contract Link')
        attributes = (object.house.address, object.company, object.start_amount, object.balance, object.start_date, object.total_paid, file_url)
    elif isinstance(object, Request_Payment):
        file_url = generate_file_url(document_link=object.job.document_link)
        headers    = ('House', 'Company', 'Amount', 'Submit Date', 'Approved Date', 'Contract Link')
        attributes = (object.house.address, object.job.company, object.amount, object.submit_date, object.approved_date, file_url)
    elif isinstance(object, Expenses):
        file_url = generate_file_url(document_link=object.job.document_link)
        headers = ('House', 'Expense Type', 'Amount',  'Date Added', 'Contract Link')
        attributes = (object.house, object.expense_type, object.amount, object.submit_date, file_url)
    else:
        headers = None
        attributes = None

    return (headers, attributes)

def generate_csv(title, queryset, request):
    if queryset:
        #create csv writer
        csv_file = io.StringIO()
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow((title))

        for count, item in enumerate(queryset):
            headers, attributes = get_attributes_and_headers(object=item, request=request)

            #write headers for spreadsheet on first loop
            if count == 0:
                writer.writerow(headers)

            writer.writerow(attributes)

        return csv_file.getvalue()
    else:
        raise ValueError('A queryset must be inserted to generate a spreadsheet')

def get_document_links(queryset):
    for item in queryset:
        #get document paths
        try: #for payment objects
            yield str(item.job.document_link)
        except AttributeError: #for job objects
            print('This is a Job object and thus has no attribute "job"')
            yield str(item.document_link)

def generate_zip(document_links=[]):
    """generates zip file"""
    if len(document_links) != 0:
        zip_file = io.BytesIO()
        zf = zipfile.ZipFile(zip_file, "w")
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        prev_arcnames = [] #previous arcnames
        for counter, file_path in enumerate(document_links):
            absname = os.path.abspath(os.path.join(base_dir, 'media', *file_path.split('/')))
            arcname = os.path.split(absname)[1]

            #do not overwrite files with the same name
            if arcname in prev_arcnames:
                fname, ext = os.path.splitext(arcname)
                arcname = '{fname}-{counter}{ext}'.format(fname=fname, counter=counter, ext=ext)

            prev_arcnames.append(arcname)

            zf.write(absname, arcname)

        zf.close()
        return zip_file.getvalue()

# def setup_cron_job(frequency, user, path, host, form_vals={}):
#     """sets up a cron job to send automated emails with data"""
#     user_id = user.id
#     system_user = getpass.getuser() #the user name of the user from the OS, not the web application
#
#     #check if user has any previous cron jobs
#     cron = CronTab(user=system_user)
#     user_id_string = 'User {user_id}'.format(user_id=user_id)
#     job_number = 1
#
#     for job in cron.crons:
#         if user_id_string in job.comment:
#             job_number = int(job.comment.split(' ').pop())
#             job_number += 1 #increase job number if it's another new job
#
#     base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     python_path = sys.executable
#     command = '{python_path} {base_dir}/manage.py runscript send_data_cron {url_path} {host} {user_id} {send_to}> /tmp/test.log 2>&1'.format(
#         python_path=python_path,
#         base_dir=base_dir,
#         url_path=path,
#         host=host,
#         user_id=user_id,
#         send_to=form_vals['send_to'],
#     )
#     comment = 'User {user_id}, Job {job_number}'.format(user_id=user_id, job_number=job_number)
#     job = cron.new(command=command, comment=comment)
#     today = datetime.datetime.now()
#     current_minute = today.minute + 1
#     current_hour = today.hour
#
#     if frequency == 2: #daily
#         job.minute.on(current_minute)
#         job.hour.on(current_hour)
#         job.dow.on('SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT')
#         print(job.frequency_per_year())
#     elif frequency == 3: #weekly
#         job.minute.on(current_minute)
#         job.hour.on(current_hour)
#         job.dow.on(today.weekday() + 1)
#         print(job.frequency_per_year())
#     elif frequency == 4: #monthly
#         job.minute.on(current_minute)
#         job.hour.on(current_hour)
#         job.day.on(today.day)
#         print(job.frequency_per_year())
#
#     cron.write()
#     return True
