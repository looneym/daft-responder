import feedparser
import urlparse
from time import sleep
import dateutil.parser
import datetime
import pytz
import random
import logging
import time
import requests

logging.basicConfig(filename='responder.log',level=logging.DEBUG)


def quickTime():
    return time.strftime("%Y-%m-%d %H:%M")

def email_to(ident):

    message = """
        Hey there,

        Got in pretty quick on this one :)

        I'm Micheal and I work as an Engineer at a tech company called Intercom.

        I'm at work every day from 9 till 7 or so. On the weekends I enjoy
        cycling/going to gigs/meeting friends for lunch or a few beers.
        I'm not someone who would be looking to have loads of parties or anything like that but I'm pretty laid back
        and easy to get along with at the same time. I don't smoke.

        I have letters of reference from various landlords and a letter of reference from work if you need it.
        Let me know if you think I'd be a good fit!

        LinkedIn: https://ie.linkedin.com/in/looneym
    """

    req = requests.post("http://www.daft.ie/ajax_endpoint.php", data={
        'action': 'daft_contact_advertiser',
        'from': 'Micheal Looney',
        'email': 'looneymicheal@gmail.com',
        'message': message,
        'contact_number': '0851426134',
        'type': 'sharing',
        'id': ident,
        'self_copy': '1',
        'agent_id': ''
    })



    if req.text == u'"Email successfully sent to advertiser"':
        logging.info(quickTime() + " Email successfully sent to {0}".format(ident))
    else:
        logging.error(req.text)

def start():

    observedIds = set([])
    startUpTime = pytz.UTC.localize(datetime.datetime.now())
    logging.info(quickTime() + " Program started")

    while True:

        logging.info(quickTime() + " Requesting feed")

        f = feedparser.parse("http://www.daft.ie/rss.daft?uid=1492175&id=751701&xk=544686")

        logging.info(quickTime() + " {0} entries recieved".format(len(f['entries'])))
        for entry in f['entries']:
            url = urlparse.urlparse(entry['link'])
            ident = urlparse.parse_qs(url.query)['id'][0]
            pub_date = dateutil.parser.parse(entry['published'])

            if pub_date < startUpTime:
                continue

            if ident in observedIds:
                continue

            observedIds.add(ident)
            email_to(ident)

        if datetime.datetime.now().hour < 8:
            sleep(15*60)
        else:
            sleep(random.randint(5*60,10*60))

start()

