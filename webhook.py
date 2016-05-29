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
    def send_text_message(sender, text):
        pass
        messageData = {
            "text": text
        }
                
    def get(self):
        print('hello: ' + self.get_query_argument("hub.verify_token"))

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

            '''
            send_data = {
              "object":"page",
              "entry":[
                {
                  "id": PAGE_ID,
                  "time":1458692752478,
                  "messaging":[
                    {
                      "sender":{
                        "id":"USER_ID"
                      },
                      "recipient":{
                        "id":"PAGE_ID"
                      },
                      "timestamp":1458692752478,
                      "postback":{
                        "payload":"USER_DEFINED_PAYLOAD"
                      }
                    }
                  ]
                }
              ]
            }
            '''
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
            
            send_message_response = yield http_client.fetch(
                HTTPRequest("https://graph.facebook.com/v2.6/me/messages", 'POST', headers, body=json.dumps(send_data))
            )

            if send_message_response.error:
                print "Error:", send_message_response.error
            else:
                print 'send_message_response: ' + send_message_response.body
                        
            self.write("200")
            break
