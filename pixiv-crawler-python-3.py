#-*- coding:utf-8 -*- #this line supports the input of the Chinese characters

# DOES NOT WORK!!!

# The code is based on the work of QuantMio
# https://github.com/QuantMio/PixivSpider

import urllib
from urllib.request import urlopen
#import cookielib
import re
import getpass

class Pixiv(object):
    def __init__(self, email, passwd):
        url="https://www.secure.pixiv.net/login.php"

        values={
            'op':'login',
            'pixiv_id':email,
            'pass':passwd,
            #'skip':'1'
        }

        data = urllib.parse.urlencode(values)
        binary_data = data.encode('UTF-8')
        req = urllib.request.Request(url, binary_data)
        response = urllib.request.urlopen(req)
        self.opener = response.read()

        try:
            with urllib.request.urlopen(url) as response:
                response = response.read()


        except:
            print ('Login Failed!')

        else:
            print ('Input confirmed, please stand by...')


    def login(self):
        print('Login......')
        with urllib.request.urlopen('http://www.pixiv.net/ranking.php?mode=daily&content=illust') as response:
            html = response.read()

        html = html.decode('utf-8')

        pattern = re.compile(r'(?<=\bdata-id=")\d+(?=")')
        start = 0
        i = 0
        m = pattern.search(html, start)

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
            #websiteCode = websiteCode.decode('utf-8')
            originalURL= 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=%s' % (id)


            imageWebsite = urllib.request.urlopen(originalURL)

            print ("URL", originalURL)
            websiteCode = imageWebsite.read()
            websiteCode = websiteCode.decode('utf-8')
            print (websiteCode)
            imageCode = image_compiled.search(websiteCode)
            print ("code", imageCode)

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

            # http://www.pixiv.net/member_illust.php?mode=manga&illust_id=51276014
            # http://i3.pixiv.net/c/1200x1200/img-master/img/2015/07/06/16/14/44/51276014_p1_master1200.jpg
            # http://i2.pixiv.net/img-original/img/2015/07/06/14/46/09/51275201_p0.jpg

            if (imageCode != None):
                imageGroup = imageCode.group()
                h_pre = re.compile('i\d*\.pixiv\.net(?=/img-original/img/\d*/\d*/\d*/\d*/\d*/\d*/%s\_p\d*\.(jpg|png))'%(id))
                host = re.search(h_pre,imageGroup).group()

                print("host: ", host)

                print ('Downloading Illust Pixiv ID %s' % (id))
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
                    f = open(filename,"w+")
                    f.write(response)
                    f.close()
                    print ('Incoming Transmission')
                else:
                    filename="%s.png"%(id)
                    f = open(filename,"wb")
                    f.write(response)
                    f.close()
                    print ('Incoming Transmission.')

            else:
                print ("Manga Found!")

                # http://i3.pixiv.net/c/1200x1200/img-master/img/2015/07/06/16/14/44/51276014_p1_master1200.jpg
                # http://i2.pixiv.net/img-original/img/2015/07/06/14/46/09/51275201_p0.jpg
                # h = re.compile('i\d*\.pixiv\.net(?=/img-original/img/\d*/\d*/\d*/\d*/\d*/\d*/%s\_p\d*\.(jpg|png))'%(id))

                manga_pattern = 'http://i\d*\.pixiv\.net/c/1200x1200/img-master/img/\d*/\d*/\d*/\d*/\d*/\d*/%s\_p\d*\_master1200\.(jpg|png)' % (id)

                manga_compiled = re.compile(manga_pattern)

                manga_URL = 'http://www.pixiv.net/member_illust.php?mode=manga&illust_id=%s' % (id)
                image_page = urllib.request.urlopen(manga_URL)
                image_page_code = image_page.read()

                image_catched = re.search(manga_compiled, image_page_code)
                if (image_catched != None):
                    image_group = image_catched.group()
                    h_pre = re.compile('i\d*\.pixiv\.net(?=/c/1200x1200/img-master/img/\d*/\d*/\d*/\d*/\d*/\d*/%s\_p\d*\_master1200\.(jpg|png))' % (id))
                    host = re.search(h_pre,image_group).group()

                    print ('Downloading Illust Pixiv ID %s' % (id))
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
                        f = open(filename,"w+")
                        f.write(response)
                        f.close()
                        print ('Incoming Transmission 2')

                    else:
                        filename="%s.png"%(id)
                        f = open(filename,"w+")
                        f.write(response)
                        f.close()
                        print ('Incoming Transmission 2')



print('#'*30)
print('## ' + "Welcome to Pixiv Crawler" + " ##")
print('#'*30)

print("\n")

email = input("Please input your Pixiv account: ")
passwd = getpass.getpass("Please input your Pixiv Password: ")

my = Pixiv(email, passwd)
my.login()
my.grab_image()


