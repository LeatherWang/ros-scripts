#!/usr/bin/env python
#coding=utf8

import rospy,itchat,threading
import json
import urllib2
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import hashlib
import requests
from std_msgs.msg import String

def md5(str):#生成md5
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()

#英译中
def en_to_zh(src):
    ApiKey = "20180117000116260"
    pwd = "HaukegDBvUHV2CYH2HgL"
    salt = "1435660288"
    all = ApiKey + src + salt + pwd
    sign = md5(all)
    src=src.replace(' ','+')#生成sign前不能替换
    url = "http://api.fanyi.baidu.com/api/trans/vip/translate?q="\
          + src + "&from=en&to=zh&appid=" + ApiKey + \
          "&salt=" + salt + "&sign=" + sign
    try:
        req = urllib2.Request(url)
        con = urllib2.urlopen(req)
        res = json.load(con)
        if 'error_code' in res:
            print 'error:', res['error_code']
            return res['error_msg']
        else:
            dst = res['trans_result'][0]['dst']
            return dst
    except:
        return "出错了"

#中译英     
def zh_to_en(src):
    ApiKey = "20180117000116260"
    pwd = "HaukegDBvUHV2CYH2HgL"
    salt = "1435660288"
    all = ApiKey + src + salt + pwd
    sign = md5(all)
    src=src.replace(' ','+')#生成sign前不能替换
    url = "http://api.fanyi.baidu.com/api/trans/vip/translate?q="\
          + src + "&from=zh&to=en&appid=" + ApiKey + \
          "&salt=" + salt + "&sign=" + sign
    try:
        req = urllib2.Request(url)
        con = urllib2.urlopen(req)
        res = json.load(con)
        return res['trans_result'][0]['dst']
    except:
        return "出错了"
             
# 图灵机器人
def get_response(msg, FromUserName):
    api_url = 'http://www.tuling123.com/openapi/api'#设定自己机器人的属性
    apikey = '638c2bd4124749338d8d08578053939c'
    
    data = {'key': apikey,
            'info': msg,
            'userid': 'leather'
            }
    try:
        req = requests.post(api_url, data=data).json()
        return req.get('text')
    except:
        return
                
def send_message(temp):
	itchat.send_msg(temp,toUserName='filehelper')

def send_image():
	itchat.send_image(r"/home/leather/oneshoot.jpg",toUserName='filehelper')
	
def callback(data):
    rospy.loginfo('I heard %s', data.data)#rospy.get_caller_id() 
    if data.data == 'alarm' :
        send_message('[Warn]:One stranger appears!!!')
    if data.data == 'photo' :
        send_image()

def send_takephoto_command():
    commmand_str = 'takephoto'
    pub.publish('commmand_str')

func_flag=10     
nick_name='x'
@itchat.msg_register(['Text', 'Map', 'Card', 'Note', 'Sharing'])
def text_reply(msg):
    global func_flag
    global nick_name
    rospy.loginfo('I received a WX message: ' + msg.text)
    users = itchat.search_friends(userName=msg['FromUserName'])

    if msg.text == '怎么用':
        nick_name = users['NickName']#注意跟users[0]['UserName']索引方式不同
        itchat.send('该机器人有以下三种功能：\n1、图灵机器人按：0\n2、英汉翻译按：1\n3、汉英翻译按：2\n\n退出机器人按：q\n\n注意：机器人不能发表情，如果有表情就表示是本人发的', msg['FromUserName'])
    
    if nick_name != users['NickName']:
        return
    if msg.text == '0':
        itchat.send('切换至图灵机器人聊天模式...', msg['FromUserName'])
        func_flag = 0
    if msg.text == '1':
        itchat.send('切换至‘英汉’翻译模式...', msg['FromUserName'])
        func_flag = 1
    if msg.text == '2':
        itchat.send('切换至‘汉英’翻译模式...', msg['FromUserName'])
        func_flag = 2
    if msg.text == '3':
        itchat.send('切换至获取美图模式...', msg['FromUserName'])
        func_flag = 3
    if msg.text == 'q':
        itchat.send('轻轻地我走了...\n\n回复：怎么用启用机器人', msg['FromUserName'])
        func_flag = 10
        #send_takephoto_command()
    
    if func_flag == 0:
        respones = get_response(msg['Content'], msg['FromUserName'])
        itchat.send(respones, msg['FromUserName'])
        print respones
    if func_flag == 1:
        print '翻译中...'
        target_1 = en_to_zh(msg.text)
        itchat.send(target_1, msg['FromUserName'])
    if func_flag == 2:
        print '翻译中...'
        target_2 = zh_to_en(msg.text)
        itchat.send(target_2, msg['FromUserName'])

    
    #users = itchat.search_friends(name=u'happy')#想给谁发信息，先根据备注查找到这个朋友
    #userName = users[0]['UserName']    #找到UserName
    #itchat.send_msg(msg.text,toUserName=userName)
    #itchat.send(msg.text, toUserName='filehelper')
    #return msg['Text']

class newThread(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.num = num
    def run(self):
    	print("--------------------------------------------------")
        print("-----------------初始化 itchat---------------------")#, self.num
        print("--------------------------------------------------")
        itchat.auto_login(True)
        itchat.send_msg(u"初始化完成！",toUserName='filehelper')
        print("--------------------------------------------------")
        print('---------------------初始化完成--------------------')
        print("--------------------------------------------------")
        itchat.run()

	
#rospy.init_node('talker', anonymous=True)
#rate=rospy.Rate(1)
rospy.init_node('listener', anonymous=True)
rospy.Subscriber('recogface_alarm', String, callback)
pub=rospy.Publisher('itchat_takephoto', String, queue_size=10)

if __name__ == '__main__':
    try:
        sys.setdefaultencoding('utf8')
        t1=newThread(1)
        t1.setDaemon(True)#守护线程，主线程退出时，子线程跟着退出
        t1.start()
        rospy.spin()
        
    except rospy.ROSInterruptException:
		pass
