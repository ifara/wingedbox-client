import threading
import urllib
import webbrowser

from BeautifulSoup import BeautifulSoup

class Api(threading.Thread):

    def __init__(self, winged):
        threading.Thread.__init__(self)
        self._winged = winged
        self._browser = Browser()

    def run(self):
        user = self._winged._box.user
        password = self._winged._box.password
        myfiles = 'http://wingedbox.com/api/archives.xml?login=' \
                + user + '&password=' + password + '&type=my_files'
        soup = self.obtain_data(myfiles)
        archives = soup.findAll('archive')
        files = []
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
            files.append(file)
        
        friendFiles = 'http://wingedbox.com/api/archives.xml?login='\
                + user + '&password=' + password + '&type=friend_files'
        soup = self.obtain_data(friendFiles)

        self._winged.load_tables(files, [])

    def obtain_data(self, link):
        page = self._browser.open(link)
        soup = BeautifulSoup(page.read())
        return soup

    def download_file(self, id):
        down = 'http://wingedbox.com/downloads/' + id
        webbrowser.open(down)

    def facebook(self, id, name):
        name = name.replace(' ', '%20')
        link = 'http://www.facebook.com/sharer.php?u=http://wingedbox.com/downloads/'\
                + id + '&title=' + name
        webbrowser.open(link)

    def twitter(self, id, name):
        name = name.replace(' ', '%20')
        link = 'http://twitter.com/home?status=Check%20this%20' \
                + name + '%20http://wingedbox.com/downloads/' + id + '%20uploaded%20to%20@winged_box'
        webbrowser.open(link)

class Browser(urllib.FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
