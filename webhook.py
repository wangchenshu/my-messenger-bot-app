#!/usr/bin/env python
#-*- coding: utf-8 -*-

import json
import tornado.web
import urllib
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.options import define, options
from tornado import gen
import message

define("verify_token", default="", help="", type=str)
define("access_token", default="", help="", type=str)

class WebhookHandler(tornado.web.RequestHandler):    
    def get(self):
        print(self.get_query_argument("hub.verify_token"))

        if self.get_query_argument("hub.verify_token") == options.verify_token:
            print("rec: " + self.get_query_argument("hub.challenge"))
            self.write(self.get_query_argument("hub.challenge"))
        else:
            self.write('Error, wrong validation token');
        
    @gen.coroutine
    def post(self):
        request_dict = json.loads(self.request.body)

        print(request_dict["entry"][0]["messaging"])

        messaging_events = request_dict["entry"][0]["messaging"]
        http_client = AsyncHTTPClient()
        
        for event in messaging_events:
            print(event["sender"]["id"])
            if event["message"] and event["message"]["text"]:
                content_text = event["message"]["text"]
                print content_text

                #print(options.access_token)
                headers = { 
                    'Content-Type': 'application/json'
                   }        

                send_text = message.send_text["default"]

                if "h4" in content_text and                                                       \
                   ("where" in content_text or "go" in content_text or "going" in content_text or \
                    u"如何去" in content_text or u"怎麼去" in content_text or                     \
                    u"如何走" in content_text or u"怎麼走" in content_text):
                    send_text = message.send_text["where_is_h4"]

                elif "h4" in content_text and ("doing" in content_text or u"做什麼" in content_text):
                    send_text = message.send_text["what_are_h4_people_do"]

                elif "h4" in content_text and u"由來" in content_text:
                    send_text = message.send_text["h4_beginning"]

                elif "contact" in content_text or u"聯絡" in content_text:
                    send_text = message.send_text["contact_us"]

                send_data = {
                    'access_token': options.access_token,
                    "recipient": {
                        "id": event["sender"]["id"]
                    },
                    "message": {
                        "text": send_text
                    }
                   }
                
                print(send_data)
                #data = urllib.urlencode(send_data)

                try:
                    send_message_response = yield http_client.fetch(HTTPRequest(
                        "https://graph.facebook.com/v2.6/me/messages?access_token=" + options.access_token,
                        'POST',
                        headers,
                        body=json.dumps(send_data)
                    ))

                    if send_message_response.error:
                        print "Error:", send_message_response.error

                    else:
                        print 'send_message_response: ' + send_message_response.body

                except tornado.httpclient.HTTPError as e:
                    print("ex: " + str(e))

                except Exception as e:
                    print("Error: " + str(e))

            self.write("200")
