from jobs.models import Job, Request_Payment
from expenses.models import Expenses
from django.conf import settings
from botocore.client import Config
from requests import get
import boto3
import botocore
import csv
import io
import zipfile

def generate_aws_file_url(document_link):
    """Generates file url"""
    Config.signature_version = botocore.UNSIGNED
    return boto3.client('s3', settings.AWS_S3_REGION_NAME, config=Config(s3={'addressing_style': 'path'})).generate_presigned_url('get_object', ExpiresIn=86400, Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': str(document_link)})


def get_attributes_and_headers(object, request):
    """
    Returns a tuple with the desired values from objects and headings for the csv file
    based on the instance type
    """
    if isinstance(object, Job):
        file_url = generate_aws_file_url(document_link=object.document_link)
        headers    = ('House', 'Company', 'Start Amount', 'Balance', 'Submit Date', 'Total Paid', 'Contract Link')
        attributes = (object.house.address, object.company, object.start_amount, object.balance, object.start_date, object.total_paid, file_url)
    elif isinstance(object, Request_Payment):
        file_url = generate_aws_file_url(document_link=object.job.document_link)
        headers    = ('House', 'Company', 'Amount', 'Submit Date', 'Approved Date', 'Contract Link')
        attributes = (object.house.address, object.job.company, object.amount, object.submit_date, object.approved_date, file_url)
    elif isinstance(object, Expenses):
        file_url = generate_aws_file_url(document_link=object.job.document_link)
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
        writer.writerow([title])

        for count, item in enumerate(queryset):
            headers, attributes = get_attributes_and_headers(object=item, request=request)

            #write headers for spreadsheet on first loop
            if count == 0:
                writer.writerow(headers)

            writer.writerow(attributes)

        value = csv_file.getvalue()
        csv_file.close()
        return value
    else:
        raise ValueError('A queryset must be inserted to generate a spreadsheet')

def get_document_links(queryset):
    """Gets document paths"""
    if queryset:
        for item in queryset:
            if isinstance(item, Job) or isinstance(item, Expenses):
                yield str(item.document_link)
            elif isinstance(item, Request_Payment):
                yield str(item.job.document_link)
    else:
        raise ValueError('A queryset must be inserted to get document links')


def download_file_from_url(url):
    """Downloads file from specifed url"""
    if url:
        file = io.BytesIO()
        # get request
        response = get(url)
        # write to file
        file.write(response.content)

        value = file.getvalue()
        file.close()
        return value
    else:
        raise ValueError('A url must be provided to extract url contents')

def generate_zip(queryset):
    """generates zip file"""
    if queryset:
        zip_file = io.BytesIO() #create a zip file in memory
        zf = zipfile.ZipFile(zip_file, "w") #open the zip file created in memory and open in 'write' mode

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
                arcname = document_link.split('/')[-1] + '-' + str(count)

            zf.writestr(zinfo_or_arcname=arcname, data=file)
            previous_arcnames.append(arcname) #append arcname we used to list so we know if we used the name before (prevents overwriting of files with the same name)

        zf.close()
        value = zip_file.getvalue()
        zip_file.close()
        return value
    else:
        raise ValueError('A queryset must be inserted to generate a zip file')
