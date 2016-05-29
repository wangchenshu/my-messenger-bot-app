#!/usr/bin/env python
#-*- coding: utf-8 -*-

import json
import tornado.web
import urllib
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.options import define, options
from tornado import gen

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
                text = event["message"]["text"]
                print text

            #print(options.access_token)
            headers = { 
                'Content-Type': 'application/json',
                'access_token': options.access_token        
            }        

            send_data = {
                "recipient": {
                    "id": event["sender"]["id"]
                },
                "message": {
                    "text": text
                }
            }
            
            print(send_data)
            #data = urllib.urlencode(send_data)

            try:
                send_message_response = yield http_client.fetch(
                    HTTPRequest("https://graph.facebook.com/v2.6/me/messages", 'POST', headers, body=json.dumps(send_data))
                )

                if send_message_response.error:
                    print "Error:", send_message_response.error

                else:
                    print 'send_message_response: ' + send_message_response.body

            except tornado.httpclient.HTTPError as e:
                print("ex: " + str(e))

            except Exception as e:
                print("Error: " + str(e))

            self.write("200")
