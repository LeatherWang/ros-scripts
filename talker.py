#!/usr/bin/env python
#coding=utf8

import rospy,itchat,threading,sys
from std_msgs.msg import String

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
      
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    rospy.loginfo('I received a WX message: ' + msg.text)
    if msg.text == 'look':
        send_takephoto_command()
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
        reload(sys)
        sys.setdefaultencoding('utf8')
        t1=newThread(1)
        t1.setDaemon(True)#守护线程，主线程退出时，子线程跟着退出
        t1.start()
        rospy.spin()
        
    except rospy.ROSInterruptException:
		pass
