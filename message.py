#!/usr/bin/env python
#-*- coding: utf-8 -*-

image_link = {
    "h4": "https://s3-ap-northeast-1.amazonaws.com/walter-s3/line-bot/image/h4-logo",
    "emacs": "https://s3-ap-northeast-1.amazonaws.com/walter-s3/line-bot/image/emacs-logo"
}

send_text = {
    "default": "Welcome to h4!",
    "h4": "Welcome to h4!",
    "emacs": "Welcome to Emacs Taiwan!",
    "how_are_you_today": "How are you today?",
    "where_is_h4": u"""
        餐廳：田中園光華店
        地址：台北市中正區臨沂街 1 號
        (捷運忠孝新生站一號出口直走第一個路口右轉)
        時間：7:30pm ~ 10:00pm

        Restaurant : 田中園 (Tian Jung Yuan)
        Venue : No. 1, Linyi St, Zhongzheng District, Taipei City
        (MRT JungXiao Xingshen Station Exit 1)
        Time : 7:30pm ~ 10:00pm
    """,
    "what_are_h4_people_do": u"""
        1. 討論 web, network, programming, system, blablah….
        2. 交流系統工具 & 使用技巧
        3. 八卦
    """,
    "h4_beginning": u"""
        Hacking Thursday 是由幾位居住於台北地區的自由軟體/開放原碼開發者所發起，
        每週四晚上會於特定咖啡店聚會。以非會議形式、交換並實做各自提出的想法，
        輕鬆的會議過程以禮貌、謙遜與尊重的互信態度接納並鼓勵概念發想、發起新計畫、
        並從開發者的協同開發與經驗分享中互相學習。
    """,
    "contact_us": u"""
        除了實體聚會外，我們使用 Google group / Facebook group 做為大家的溝通聯絡管道。
        聊天，討論，及聚會通告都會在這裡發佈。如果您對我們的聚會有興趣，隨時都歡迎您加入/訂閱我們的討論區，和我們交流！！

        http://groups.google.com/group/hackingthursday ( Google group )
        http://www.facebook.com/groups/hackingday/ ( Facebook group )
        https://www.meetup.com/hackingthursday/ ( Meetup )
    """
}

def create_text_message(sender, text):
    return {
        "recipient": {
            "id": sender
        },
        "message": {
            "text": text
        }
    }

def create_generic_message(sender):
    message_data = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [{
                    "title": "First card",
                    "subtitle": "Element #1 of an hscroll",
                    "image_url": "https://s3-ap-northeast-1.amazonaws.com/walter-s3/line-bot/image/11813376_842684179173214_3987034703356373870_n.jpg",
                    "buttons": [{
                        "type": "web_url",
                        "url": "https://hackingthursday.org",
                        "title": "H4 Web url"
                    }, {
                        "type": "postback",
                        "title": "Postback",
                        "payload": "Payload for first element in a generic bubble",
                    }],
                  },{
                        "title": "Second card",
                        "subtitle": "Element #2 of an hscroll",
                        "image_url": "https://s3-ap-northeast-1.amazonaws.com/walter-s3/line-bot/image/11813376_842684179173214_3987034703356373870_n.jpg",
                        "buttons": [{
                            "type": "postback",
                            "title": "EmacsPostback",
                            "payload": "Payload for second element in a generic bubble",
                        }],
                    }
                ]
            }
        }
    }

    return {
        "recipient": {
            "id": sender
        },
        "message": {
            "text": message_data
        }
    }

def create_butten_template_message(sender):
    return {
        "recipient":{
            "id": sender
        },
        "message":{
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text":"What do you want to do next?",
                    "buttons":[
                        {
                            "type":"web_url",
                            "url":"http://www.hackingthursday.org/",
                            "title":"H4 Website"
                        },
                        {
                            "type":"postback",
                            "title":"Start Chatting",
                            "payload":"USER_DEFINED_PAYLOAD"
                        }
                    ]
                }
            }
        }
    }
