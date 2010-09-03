import feedparser, pickle, os, sys, urllib , time, tweepy
import ConfigParser , codecs
import argparse, webbrowser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sohaib Afifi twitter bot.')
    parser.add_argument('--tag', nargs=1, help='retweet by tag .')
    parser.add_argument('--config', nargs=1, type=file, metavar='CONFIG.cfg', default=['defaults.cfg'], help='config file to load.')
    parser.add_argument('--interval', default=[10], nargs=1, metavar='TIME', type=int, help='interval between tweets (seconds).')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')
    parser.add_argument('--install', nargs=1, type=file, metavar='CONFIG.cfg', help='install the tool and generate the default setting file.')
    
    parser.print_help()
    args = parser.parse_args()
    #exit()

   
    if args.install != None:
        config = ConfigParser.RawConfigParser()
        config.read(args.install[0].name)
        USERNAME = config.get('user', 'username')
        PASSWORD = config.get('user', 'password')  
        CONSUMER_KEY = config.get('app', 'CONSUMER_KEY')
        CONSUMER_SECRET = config.get('app', 'CONSUMER_SECRET')
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth_url = auth.get_authorization_url()
        print 'Please authorize: \n' + auth_url
        webbrowser.open_new(auth_url)
        verifier = raw_input('PIN: ').strip()
        auth.get_access_token(verifier)
        config.set('app', 'ACCESS_KEY', auth.access_token.key)
        config.set('app', 'ACCESS_SECRET', auth.access_token.secret)
        # Writing our configuration file
        with open(args.install[0].name, 'wb') as configfile:
            config.write(configfile)
        
        exit()
    
    config = ConfigParser.RawConfigParser()
    config.read(args.config[0])
    USERNAME = config.get('user', 'username')
    PASSWORD = config.get('user', 'password')    
    CONSUMER_KEY = config.get('app', 'CONSUMER_KEY')
    CONSUMER_SECRET = config.get('app', 'CONSUMER_SECRET')
    ACCESS_KEY = config.get('app', 'ACCESS_KEY')
    ACCESS_SECRET = config.get('app', 'ACCESS_SECRET')       
        
    
       
        
    
    
class twitterbot:
    
    
    HISTORY = USERNAME + '.db'#'history.db'
    def __init__(self, url, username, passwd):
        self.filename = self.HISTORY
        self.url = url
        self.username = username
        self.passwd = passwd
        self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        self.api = tweepy.API(self.auth)
        print USERNAME, 'logged'

        if os.path.exists(self.filename):
            self.itemsDB = pickle.load(file(self.filename, 'r+b'))
        else:
            self.itemsDB = {}
                
    def getLatestFeedItems(self, items=3):
        feed = feedparser.parse(self.url);
        it = feed["items"]
        it_ret = it[0:items]
        return it_ret
    
    def twitIt(self, items, sleep=0):
        pItems = 0
        sys.stdout = codecs.getwriter('cp866')(sys.stdout)

        print "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        print "getting news from " + self.url
        print "----------------------------------------------------------------"
        for it in items:
            if self.itemPublished(it) == None :
                print "----------------------------------------------------------------"
                txt = "[#MyBot]: " + it["title"] + " " + self.tiny(it["link"])
                if len(txt) < 141 :
                    self.api.update_status(txt)
                    print pItems , " : " + txt
                    pItems = pItems + 1
                    time.sleep(sleep)
                else :
                    print 'tweet too long'
                
                    
        print "Total items :", len(items)
        print "published: ", pItems
        print "old stuff: ", len(items) - pItems
        return pItems
    
    def itemPublished (self, item):
        if self.itemsDB.has_key(item["link"]) == True:
            return True
        else:
            self.itemsDB[item["link"]] = item["title"]
            pickle.dump(self.itemsDB, file(self.filename, 'w+b'))
        return None
    
    def tiny(self, url):
        try:
            data = urllib.urlencode(dict(url=url, source="RSS2Twit"))
            encodedurl = "http://www.tinyurl.com/api-create.php?" + data
            #encodedurl="http://sohaibafifi.com/go/yourls-api.php?format=simple&action=shorturl&url="+data
            instream = urllib.urlopen(encodedurl)
            ret = instream.read()
            instream.close()
            if len(ret) == 0:
                return url
            return ret
        except IOError , e:
            raise "urllib error." 
            
            
if __name__ == "__main__":
    feedfile = open("feeds.txt", "r")
    url = feedfile.readline()
    while url:
        r2t = twitterbot(url, USERNAME, PASSWORD)
        its = r2t.getLatestFeedItems(3)
        count = r2t.twitIt(its, args.interval[0])
        if count > 0:
            time.sleep(args.interval[0])
        url = feedfile.readline()
