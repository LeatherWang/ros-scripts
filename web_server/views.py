#!/usr/bin/env python
#coding=utf8
'''
#=============================================================================
#     FileName: views.py
#         Desc: 
#       Author: wangheng
#        Email: wujiwh@gmail.com
#     HomePage: http://wangheng.org
#      Version: 0.0.1
#   LastChange: 2015-01-14 13:46:29
#      History:
#=============================================================================
'''
import rospy,threading
from std_msgs.msg import String
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
#from pi_car import app
import re

app = Flask(__name__)
#app.config.from_object('pi_car.config.Development')

@app.route('/')
def show_index():
    return render_template('home.html')

@app.route("/login", methods=["GET", "POST"])                                   
def login():                                                                    
	if request.method=="GET":                                                   
		return "get"+request.form["user"]
	elif request.method=="POST":                                                
		return "post"

@app.route('/ctl',methods=['GET','POST'])
def ctrl_id():
	if request.method == 'POST':
		id=request.form['id']

		if id == 't_left':
			t_left()
			print 'left'
			return "left"
		elif id == 't_right':
			t_right()
			print 'right'
			return "right"
		elif id == 't_up':
			t_up()
			print 'up'
			return "up"
		elif id == 't_down':
			t_down()
			print 'down'
			return "down"
		elif id == 't_stop':
			t_stop()
			print 'stop'
			return "stop"

	return redirect(url_for('show_index'))

def t_stop():
	pass

def t_up():
	pass

def t_down():
	pass

def t_left():
	pass

def t_right():
	pass

class newThread(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.num = num
    def run(self):
        print("\n-----------------子线程：flask---------------------\n")#, self.num
        app.run(host='0.0.0.0',port=2000)
    
rospy.init_node('flask_server', anonymous=True)
#rospy.Subscriber('recogface_alarm', String, callback)
pub=rospy.Publisher('web_server_cmd', String, queue_size=10)

if __name__=='__main__':
    try:
        t1=newThread(1)
        t1.setDaemon(True)#守护线程，主线程退出时，子线程跟着退出
        t1.start()
        print("-----------------主线程：rospy---------------------\n")
        rospy.spin()
        print("\n-----------------安全退出---------------------")
    except rospy.ROSInterruptException:
        pass
  
