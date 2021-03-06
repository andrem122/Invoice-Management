from jobs.models import Job, Request_Payment
from expenses.models import Expenses
from django.conf import settings
from botocore.client import Config
from django.db.models.query import QuerySet
from sms_alerts.sms_budget_alerts import as_currency
from requests import get
import boto3
import botocore
import csv
import io
import zipfile
import os

def generate_aws_file_url(document_link):
    """Generates file url"""
    Config.signature_version = botocore.UNSIGNED
    return boto3.client(
        's3',
        settings.AWS_S3_REGION_NAME,
        config=Config(s3={'addressing_style': 'path'}),
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    ).generate_presigned_url('get_object', ExpiresIn=86400, Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': str(document_link)})


def get_attributes_and_headers(object, request):
    """
    Returns a tuple with the desired values from objects and headings for the csv file
    based on the instance type
    """
    try:
        if object.approved:
            is_approved = 'Approved'
        else:
            is_approved = 'Not Approved'
    except AttributeError as e:
        print(e)

    if isinstance(object, Job):
        file_url = generate_aws_file_url(document_link=object.document_link)
        headers    = ('House', 'Company', 'Start Amount', 'Balance', 'Total Paid', 'Submit Date', 'Status', 'Contract Link')
        attributes = (object.house.address, object.company, as_currency(object.start_amount), as_currency(object.balance1), as_currency(object.total_paid1), object.start_date.strftime('%m/%d/%Y %I:%M %p'), is_approved, file_url)
    elif isinstance(object, Request_Payment):
        file_url = generate_aws_file_url(document_link=object.job.document_link)
        headers    = ('House', 'Company', 'Amount', 'Submit Date', 'Approved Date', 'Status', 'Contract Link')
        attributes = (object.house.address, object.job.company, as_currency(object.amount), object.submit_date.strftime('%m/%d/%Y %I:%M %p'), object.approved_date.strftime('%m/%d/%Y %I:%M %p'), is_approved, file_url)
    elif isinstance(object, Expenses):
        file_url = generate_aws_file_url(document_link=object.document_link)
        headers = ('House', 'Expense Type', 'Amount',  'Date Added', 'Contract Link')
        attributes = (object.house, object.expense_type, as_currency(object.amount), object.submit_date.strftime('%m/%d/%Y %I:%M %p'), file_url)
    else:
        headers = None
        attributes = None

    return (headers, attributes)

def generate_csv(title, queryset, request):
    if queryset:
        if isinstance(queryset, QuerySet) or isinstance(queryset, list):
                    #create csv writer
                    with io.StringIO() as csv_file:
                        writer = csv.writer(csv_file, delimiter=',')
                        writer.writerow([title])

                        for count, item in enumerate(queryset):
                            headers, attributes = get_attributes_and_headers(object=item, request=request)

                            #write headers for spreadsheet on first loop
                            if count == 0:
                                writer.writerow(headers)

                            writer.writerow(attributes)

                        return csv_file.getvalue()
        else:
            raise TypeError('Queryset argument must be of type Queryset or list')
    else:
        raise ValueError('A queryset must be inserted to generate a spreadsheet')

def get_document_links(queryset):
    """Gets document paths"""
    if queryset:
        if isinstance(queryset, QuerySet) or isinstance(queryset, list):
            for item in queryset:
                if isinstance(item, Job) or isinstance(item, Expenses):
                    yield str(item.document_link)
                elif isinstance(item, Request_Payment):
                    yield str(item.job.document_link)
        else:
            raise TypeError('Queryset argument must be of type Queryset or list')
    else:
        raise ValueError('A queryset must be inserted to get document links')


def download_file_from_url(url):
    """Downloads file from specifed url"""
    if url:
        with io.BytesIO() as file:
            # get request
            response = get(url)
            # write to file
            file.write(response.content)
            return file.getvalue()
    else:
        raise ValueError('A url must be provided to extract url contents')

def generate_zip(queryset):
    """generates zip file"""
    if queryset:
        if isinstance(queryset, QuerySet) or isinstance(queryset, list):
            with io.BytesIO() as zip_file:
                with zipfile.ZipFile(zip_file, "w") as zf: #open the zip file created in memory and open in 'write' mode
                    #get document links from queryset
                    document_links = get_document_links(queryset)

                    #get urls from aws
                    previous_arcnames = []
                    for count, document_link in enumerate(document_links):
                        file_url = generate_aws_file_url(document_link)
                        file = download_file_from_url(url=file_url)

                        #add to zip file
                        arcname = document_link.split('/')[-1] #name we will call the file in the zip file

                        if arcname in previous_arcnames: #change arcname to prevent overwriting of file
                            file_name, file_extension = os.path.splitext(document_link.split('/')[-1])
                            arcname = '{file_name}-{count}{file_extension}'.format(file_name=file_name, count=count, file_extension=file_extension)

                        zf.writestr(zinfo_or_arcname=arcname, data=file)
                        previous_arcnames.append(arcname) #append arcname we used to list so we know if we used the name before (prevents overwriting of files with the same name)

                return zip_file.getvalue()
        else:
            raise TypeError('Queryset argument must be of type Queryset or list')
    else:
        raise ValueError('A queryset must be inserted to generate a zip file')
