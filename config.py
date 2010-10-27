import os

PRJ_PATH = os.path.abspath(os.path.dirname(__file__))

def createpath(root, *args):
    return root + os.path.sep + os.path.sep.join(args)

images = {
    'icon':os.path.join(PRJ_PATH, 'img', 'icon.png'),
    'logo':os.path.join(PRJ_PATH, 'img', 'logo_row.png'),
    'myfiles':os.path.join(PRJ_PATH, 'img', 'my_files.png'),
    'friends':os.path.join(PRJ_PATH, 'img', 'friend_files.png'),
    'upload':os.path.join(PRJ_PATH, 'img', 'upload_files.png'),
    'search':os.path.join(PRJ_PATH, 'img', 'search.png'),
    'download':os.path.join(PRJ_PATH, 'img', 'down.png'),
    'delete':os.path.join(PRJ_PATH, 'img', 'erase.png'),
    'facebook':os.path.join(PRJ_PATH, 'img', 'facebook.png'),
    'twitter':os.path.join(PRJ_PATH, 'img', 'twitter.png'),
    'preview':os.path.join(PRJ_PATH, 'img', 'preview.png'),
    'loading':os.path.join(PRJ_PATH, 'img', 'loading52.gif')}
type = {'image':os.path.join(PRJ_PATH, 'img', 'image.png'),
        'application/pdf':os.path.join(PRJ_PATH, 'img', 'pdf.png'),
        'application/zip':os.path.join(PRJ_PATH, 'img', 'zip.png'),
        'video':os.path.join(PRJ_PATH, 'img', 'video.png')}
typeBlank = os.path.join(PRJ_PATH, 'img', 'blank.png')
access = {'0':[144, 34, 37, 'Privado'], '1':[150, 153, 47, 'Amigos'], '2':[56, 110, 47, 'Publico']}
users = os.path.join(PRJ_PATH, 'users')
