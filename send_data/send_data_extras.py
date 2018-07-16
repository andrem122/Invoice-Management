from django.core.mail import EmailMessage
from crontab import CronTab
import csv
import io
import os
import zipfile
import getpass
import datetime
import sys

def send_data_email(user_email, title, headers, queryset, attributes, host, form_vals={}):
    """sends data through email in a zip and csv file"""
    #create email
    email = EmailMessage(form_vals['subject'], form_vals['message'], user_email, [form_vals['send_to']])

    #generate csv
    result = generate_csv(title, headers, queryset, attributes, host)
    email.attach('data.csv', result[1], 'text/csv')

    #generate zip
    zip_file = generate_zip(document_links=result[0])
    email.attach('files.zip', zip_file, 'application/x-zip-compressed')

    #send email
    email.send(fail_silently=False)

def generate_csv(title, headers, queryset, attributes, host):
    if queryset:

        #generate csv file
        csv_file = io.StringIO()
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow([title])
        writer.writerow(headers)
        document_links = []

        for q in queryset.iterator():
            try:
                document_links.append(str(q.job.document_link))
            except AttributeError:
                print('This is a Job object and thus has no attribute "job"')
                document_links.append(str(q.document_link))
            atts = []

            #loop through attributes
            for attribute in attributes:
                #if the attribute is a list
                if isinstance(attribute, list):
                    if attribute[1] == 'document_link':
                        try:
                            a = 'http://{host}/media/{document_path}'.format(
                                host=host,
                                document_path=str(getattr(getattr(q, attribute[0]), attribute[1]))
                            )
                        except NameError:
                            print('Request object is missing in tests')
                    else:
                        a = str(getattr(getattr(q, attribute[0]), attribute[1]))
                #if the attribute is NOT a list
                else:
                    if attribute == 'document_link':
                        try:
                            a = 'http://{host}/media/{document_path}'.format(
                                    host=host,
                                    document_path=str(getattr(q, attribute)),
                                )
                        except NameError:
                            print('Request object is missing in tests')
                    else:
                        a = str(getattr(q, attribute))
                atts.append(a)
            writer.writerow(atts)

        return (document_links, csv_file.getvalue())

def generate_zip(document_links=[]):
    """generates zip file"""
    if len(document_links) != 0:
        zip_file = io.BytesIO()
        zf = zipfile.ZipFile(zip_file, "w")
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        prev_arcnames = [] #previous arcnames
        for counter, fpath in enumerate(document_links):
            absname = os.path.abspath(os.path.join(base_dir, 'media', *fpath.split('/')))
            arcname = os.path.split(absname)[1]

            #do not overwrite files with the same name
            if arcname in prev_arcnames:
                fname, ext = os.path.splitext(arcname)
                arcname = '{fname}-{counter}{ext}'.format(fname=fname, counter=counter, ext=ext)

            prev_arcnames.append(arcname)

            zf.write(absname, arcname)

        zf.close()
        return zip_file.getvalue()

def setup_cron_job(frequency, user, path, host, form_vals={}):
    """sets up a cron job to send automated emails with data"""
    user_id = user.id
    system_user = getpass.getuser() #the user name of the user from the OS, not the web application

    #check if user has any previous cron jobs
    cron = CronTab(user=system_user)
    user_id_string = 'User {user_id}'.format(user_id=user_id)
    job_number = 1

    for job in cron.crons:
        if user_id_string in job.comment:
            job_number = int(job.comment.split(' ').pop())
            job_number += 1 #increase job number if it's another new job

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    python_path = sys.executable
    command = '{python_path} {base_dir}/manage.py runscript send_data_cron {url_path} {host} {user_id} {send_to}> /tmp/test.log 2>&1'.format(
        python_path=python_path,
        base_dir=base_dir,
        url_path=path,
        host=host,
        user_id=user_id,
        send_to=form_vals['send_to'],
    )
    comment = 'User {user_id}, Job {job_number}'.format(user_id=user_id, job_number=job_number)
    job = cron.new(command=command, comment=comment)
    today = datetime.datetime.now()
    current_minute = today.minute + 1
    current_hour = today.hour

    if frequency == 2: #daily
        job.minute.on(current_minute)
        job.hour.on(current_hour)
        job.dow.on('SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT')
        print(job.frequency_per_year())
    elif frequency == 3: #weekly
        job.minute.on(current_minute)
        job.hour.on(current_hour)
        job.dow.on(today.weekday() + 1)
        print(job.frequency_per_year())
    elif frequency == 4: #monthly
        job.minute.on(current_minute)
        job.hour.on(current_hour)
        job.day.on(today.day)
        print(job.frequency_per_year())

    cron.write()
    return True
