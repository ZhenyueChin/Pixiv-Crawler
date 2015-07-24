# -*- coding:utf-8 -*- #this line supports the input of the Chinese characters

# The code is based on the work of QuantMio and for learning Python
# Fixed the errors when the images are mangas
# Reference: https://github.com/QuantMio/PixivSpider

import urllib
import urllib2
import cookielib
import re
import getpass
import requests
import cStringIO
import io
from urllib2 import Request, urlopen, URLError, HTTPError

class Pixiv(object):
    def __init__(self, email, passwd):
        url="https://www.secure.pixiv.net/login.php"

        values={
            'mode':'login',
            'pixiv_id':email,
            'pass':passwd,
            'skip':'1'
        }

        data = urllib.urlencode(values)
        req = urllib2.Request(url,data)
        cookie = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        try:
            response = self.opener.open(req, timeout=10)
        except URLError, e:
            if hasattr(e, 'code'):
                print 'Login Failed!'

            elif hasattr(e, 'reason'):
                print 'Login Failed!'

        else:
            print 'Input confirmed, please stand by...'

    def login(self):
        print('Login......')
        res = self.opener.open('http://www.pixiv.net/ranking.php?mode=daily&content=illust')
        html = res.read()

        pattern = re.compile(r'(?<=\bdata-id=")\d+(?=")')
        start = 0
        i = 0
        m = pattern.search(html,start)
        target=open("list.txt",'w')
        target.truncate()

        while (m != None):
            start = m.end()
            line = m.group()
            target.write(line)
            target.write('\n')
            m = pattern.search(html, start)
        target.close()

    def grab_image(self, painter = 0):
        target = open("list.txt", 'r')
        lines = len(target.readlines())

        i = 1
        for line in open("list.txt"):
            id = line.strip('\n')
            image_pattern = 'http://i\d*\.pixiv\.net/img-original/img/\d*/\d*/\d*/\d*/\d*/\d*/%s\_p\d*\.(jpg|png)' % (id)
            image_compiled = re.compile(image_pattern)
            originalURL='http://www.pixiv.net/member_illust.php?mode=medium&illust_id=%s' % (id)

            imageWebsite = self.opener.open(originalURL)
            websiteCode = imageWebsite.read()
            imageCode = re.search(image_compiled, websiteCode)

            print websiteCode

            # These codes are for getting the information of the authors. Still under construction.
            '''
            authorPattern = re.compile(r'[\u0800-\u9fa5_a-zA-Z0-9_]+(?=\s\[pixiv\])')

            #print(websiteCode)
            tempAuthor = re.search(authorPattern, websiteCode)

            print("temp: ", tempAuthor)

            testAuthor = tempAuthor.group()

            print("lol: ", testAuthor)
            '''

            jpgFirm = re.compile('\.jpg')
            pngFirm = re.compile('\.png')

            if (imageCode != None):
                imageGroup = imageCode.group()
                h_pre = re.compile('i\d*\.pixiv\.net(?=/img-original/img/\d*/\d*/\d*/\d*/\d*/\d*/%s\_p\d*\.(jpg|png))'%(id))
                host = re.search(h_pre,imageGroup).group()

                print("host: ", host)

                print 'Downloading Illust Pixiv ID %s' % (id)
                header={
                    'Host':host,
                    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
                    'Accept':'image/png,image/*;q=0.8,*/*;q=0.5',
                    'Accept-Language':'en-US,en;q=0.5',
                    'Accept-Encoding':'gzip, deflate',
                    'Referer':'http://www.pixiv.net/'
                }

                request = urllib2.Request(imageGroup, headers=header)
                response = urllib2.urlopen(url = request).read()

                if(re.search(jpgFirm,imageGroup)!=None):
                    filename="%s.jpg" % (id)
                    f = file(filename,"wb")
                    f.write(response)
                    f.close()
                    print 'Incoming Transmission'
                else:
                    filename="%s.png"%(id)
                    f = file(filename,"wb")
                    f.write(response)
                    f.close()
                    print 'Incoming Transmission.'

            else:
                print "Manga Found!"

                manga_pattern = 'http://i\d*\.pixiv\.net/c/1200x1200/img-master/img/\d*/\d*/\d*/\d*/\d*/\d*/%s\_p\d*\_master1200\.(jpg|png)' % (id)

                manga_compiled = re.compile(manga_pattern)

                manga_URL = 'http://www.pixiv.net/member_illust.php?mode=manga&illust_id=%s' % (id)
                image_page = self.opener.open(manga_URL)
                image_page_code = image_page.read()

                image_catched = re.search(manga_compiled, image_page_code)
                if (image_catched != None):
                    image_group = image_catched.group()
                    h_pre = re.compile('i\d*\.pixiv\.net(?=/c/1200x1200/img-master/img/\d*/\d*/\d*/\d*/\d*/\d*/%s\_p\d*\_master1200\.(jpg|png))' % (id))
                    host = re.search(h_pre,image_group).group()

                    print 'Downloading Illust Pixiv ID %s' % (id)
                    header={
                        'Host':host,
                        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
                        'Accept':'image/png,image/*;q=0.8,*/*;q=0.5',
                        'Accept-Language':'en-US,en;q=0.5',
                        'Accept-Encoding':'gzip, deflate',
                        'Referer':'http://www.pixiv.net/'
                    }

                    request = urllib2.Request(image_group, headers=header)
                    response = urllib2.urlopen(url = request).read()

                    if(re.search(jpgFirm,image_group)!=None):
                        filename="%s.jpg" % (id)
                        f = file(filename,"wb")
                        f.write(response)
                        f.close()
                        print 'Incoming Transmission 2'

                    else:
                        filename="%s.png"%(id)
                        f = file(filename,"wb")
                        f.write(response)
                        f.close()
                        print 'Incoming Transmission 2'



print('#'*30)
print('## ' + "Welcome to Pixiv Crawler" + " ##")
print('## ' + "2015 - 07 - 09           " + "##")
print('#'*30)

print("\n")

email = raw_input("Please input your Pixiv account: ")
passwd = getpass.getpass("Please input your Pixiv Password: ")

my = Pixiv(email, passwd)
my.login()
my.grab_image()


