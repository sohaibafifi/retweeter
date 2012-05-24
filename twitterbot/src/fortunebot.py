import pickle, os, sys, time, tweepy
import ConfigParser , codecs,datetime
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
        
    
       
        
    
    
class fortunebot:
    
    
    HISTORY = USERNAME + '.db'#'history.db'
    def __init__(self,  username, passwd):
        self.filename = self.HISTORY
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
                
     
    def tweet(self, quote, sleep=0):
        sys.stdout = codecs.getwriter('cp866')(sys.stdout)
        print "----------------------------------------------------------------"
        txt = "#quote: " + quote
        if self.itemPublished(txt) == None :
            if len(txt) < 141 :
                self.api.update_status(txt)
                print txt
            else :
                print 'tweet too long'
                
    def retweet(self, tag, count = 1,lang='fr'):
        retweets = self.api.retweeted_by_me()
        if retweets:
            created_after = retweets[0].retweeted_status.created_at
        else:     
            created_after = datetime.datetime(year=2000, month=1, day=1)
        
        tweets = self.api.search(tag,lang)
        tweets.reverse()
        cpt = 0
        for tweet in tweets:
            if cpt == count:
                break;
             
            if tweet.created_at > created_after and tweet.from_user != self.username and self.itemPublished(tweet.text) == None :
                try : 
                    self.api.retweet(tweet.id)
                    print tweet.text
                    cpt = cpt + 1
                except tweepy.error.TweepError:
                    print 'error'
                
                
                
    def itemPublished (self, quote):
        if self.itemsDB.has_key(quote) == True:
            return True
        else:
            self.itemsDB[quote] = quote
            pickle.dump(self.itemsDB, file(self.filename, 'w+b'))
        return None
    
        
            
if __name__ == "__main__":
    r2t = fortunebot(USERNAME, PASSWORD)
    if args.tag != None:
        r2t.retweet(args.tag[0],5)
    else :
        feedfile = open("fortune.txt", "r")
        quote = feedfile.readline()
        while quote:
            r2t.tweet(quote, args.interval[0])
            time.sleep(args.interval[0])
            quote = feedfile.readline()
    