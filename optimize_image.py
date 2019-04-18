from PIL import Image
import os

def optimize_image(img_paths=()):
    """
    optimizes images to take up smaller space
    in the system
    """
    for img_path in img_paths:
        try:
            img = Image.open(img_path)
            img.save(img_path, optimize=True, quality=60)
            print('Image optimized!')
        except IOError as e:
            print(e)

def is_image(img_names=()):
    """
    checks if uploaded files are images
    """
    img_exts = ('.jpg', '.jpeg', '.gif', '.png')
    for img_name in img_names:
        filename, ext = os.path.splitext(img_name)

        if ext.lower() in img_exts:
            return True
        else:
            return False

MISSING = object()
def generate_file_path(house, user=MISSING, img_names=(), upload_folder=''):
    """
    generates file path for uploaded files
    """
    BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'project_management')
    for img_name in img_names:
        try:
            img_path = os.path.join(BASE_DIR, 'media', upload_folder, str(user.id) + '-expenses', str(img_name))
        except AttributeError:
            print('User object is missing and therefore a worker is uploading an image.')
            img_path = os.path.join(BASE_DIR, 'media', upload_folder, str(house.address), str(img_name))
        yield img_path
