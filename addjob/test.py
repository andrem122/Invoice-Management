import os

upload_path = os.path.dirname(os.path.abspath(__file__)) + '/Uploads'

print(os.path.join(upload_path, 'address', 'cool.txt'))
