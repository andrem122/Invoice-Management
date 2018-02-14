#handles uploaded files through the AddJob form
import os
from jobs.models import Job

def upload_file(f, address, job):

    #path to upload files folder
    upload_path = os.path.dirname(os.path.abspath(__file__)) + '/Uploads'
    #file name
    file_name = f.name
    #make directory for the house if it doesn't exist

    try:
        os.makedirs(os.path.join(upload_path, address))
    except OSError:
        pass

    #write to file
    file_path = os.path.join(upload_path, address, file_name)

    #update 'document_link' column in the job object
    Job.objects.filter(id=job.id).update(document_link=file_path)

    # Iterate through the chunks.
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
