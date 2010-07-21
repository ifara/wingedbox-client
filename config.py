import os

images = {'logo':os.getcwd() + '/img/logo_row.png',
                    'myfiles':os.getcwd() + '/img/my_files.png',
                    'friends':os.getcwd() + '/img/friend_files.png',
                    'download':os.getcwd() + '/img/down.png',
                    'delete':os.getcwd() + '/img/erase.png',
                    'facebook':os.getcwd() + '/img/facebook.png',
                    'twitter':os.getcwd() + '/img/twitter.png',
                    'preview':os.getcwd() + '/img/preview.png'}
type = {'image':os.getcwd()+'/img/image.png',
        'application/pdf':os.getcwd()+'/img/pdf.png',
        'application/zip':os.getcwd()+'/img/zip.png',
        'video':os.getcwd()+'/img/video.png'}
access = {'0':[144, 34, 37, 'Privado'], '1':[150, 153, 47, 'Amigos'], '2':[56, 110, 47, 'Publico']}
users = os.getcwd() + '/.config/wingedbox/'
