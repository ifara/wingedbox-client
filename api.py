import os
import urllib
import webbrowser

from BeautifulSoup import BeautifulSoup

class Api(object):

    def __init__(self, user, password):
        self.user = user
        self.password = password
        self._browser = Browser()

    def get_files(self):
        myfiles = 'http://wingedbox.com/api/archives.xml?login=' \
                + self.user + '&password=' + self.password + '&type=my_files'
        soup = self.obtain_data(myfiles)
        if soup.find('html') != None:
            raise Exception("Login Error")
        archives = soup.findAll('archive')
        self.files = []
        for archive in archives:
            file = {}
            file['id'] = archive.find('id').text
            file['accesibility'] = archive.find('accesibility').text
            type = archive.find('attachment-content-type').text
            if type.startswith('video') or type.startswith('image'):
                file['type'] = type.split('/')[0]
            else:
                file['type'] = type
            file['file-name'] = archive.find('attachment-file-name').text
            file['file-size'] = int(archive.find('attachment-file-size').text)
            file['name'] = archive.find('name').text
            self.files.append(file)
        
        friendFiles = 'http://wingedbox.com/api/archives.xml?login='\
                + self.user + '&password=' + self.password + '&type=friend_files'
        soup = self.obtain_data(friendFiles)
        archives = soup.findAll('archive')
        self.filesFriends = []
        for archive in archives:
            file = {}
            file['id'] = archive.find('id').text
            file['accesibility'] = archive.find('accesibility').text
            type = archive.find('attachment-content-type').text
            if type.startswith('video') or type.startswith('image'):
                file['type'] = type.split('/')[0]
            else:
                file['type'] = type
            file['file-name'] = archive.find('attachment-file-name').text
            file['file-size'] = int(archive.find('attachment-file-size').text)
            file['name'] = archive.find('name').text
            self.filesFriends.append(file)

    def login(self):
        myfiles = 'http://wingedbox.com/api/sessions.xml?login=' \
                + self.user + '&password=' + self.password
        soup = self.obtain_data(myfiles)
        auth = soup.find('auth')
        if auth.text == 'OK':
            return 0
        elif auth.text == 'NOK':
            return 1
        elif auth.text == 'NF':
            return 2

    def obtain_data(self, link):
        page = self._browser.open(link)
        soup = BeautifulSoup(page.read())
        return soup

    def download_file(self, data, folder):
        down = 'http://wingedbox.com/downloads/' + data['id'] + '-' + data['file-name']
        content = self._browser.open(down)
        fileName = os.path.join(folder, data['file-name'])
        f = open(fileName, 'w')
        f.write(content.read())
        f.flush()
        f.close()
        content.close()

    def delete_file(self, data):
        delete = 'http://wingedbox.com/api/archives/' + data['id'] \
                + '/delete?login=' + self.user + '&password=' + self.password
        self._browser.open(delete)

    def invite(self, friendEmail):
        url = "http://wingedbox.com/api/invitations.xml?login=" + self.user + \
                "&password=" + self.password + "&friend=" + friendEmail + "&locale=es"
        self._browser.open(url)

    def facebook(self, data):
        name = data['name'].replace(' ', '%20')
        link = data['id'] + '-' + data['file-name']
        link = 'http://www.facebook.com/sharer.php?u=http://wingedbox.com/downloads/'\
                + link + '&title=' + name
        webbrowser.open(link)

    def twitter(self, data):
        name = data['name'].replace(' ', '%20')
        link = data['id'] + '-' + data['file-name']
        link = 'http://twitter.com/home?status=Check%20this%20' \
                + name + '%20http://wingedbox.com/downloads/' + link + '%20uploaded%20to%20@winged_box'
        webbrowser.open(link)

class Browser(urllib.FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
