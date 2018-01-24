# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
import time
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required

from app.models import Event,UserName,Email,PhoneNo,AdmissionNo,Branch,TeamName,Gender,Idea,Registration
from Email.form import SendEmailForm
import app.Constant as Constant
from django.contrib import messages as info
from django.core.mail import EmailMessage


admin = ['abhishektiwari981996@gmail.com']


Body = """<br>
			<br><b style = "color:#5a5a5a">Regards,<br>
				CES.</b><br><br>
				<i  style="color:#888888">This mail is generated by CES notification bot.<br>
				To unsubscribe contact at below no.</i><br>
				<b>9998705087</b><br>
				"""

@login_required
def SendMail(request):
	log = 0
	if request.method == 'POST':
		SendEmailform = SendEmailForm(request.POST)
		if SendEmailform.is_valid():
			subject = SendEmailform.cleaned_data['subject']
			body = SendEmailform.cleaned_data['body']
			value1 = SendEmailform.cleaned_data['Select_Event']
			event = Event.objects.get(id=value1)
			registraions = Registration.objects.filter(event=event)
			Email(registraions,subject,body)

			messages = "Email send succesfully"
			return render(request,'form.html',{'SendEmailform':SendEmailform,"messages":messages})
		
		message = "Error during validation of form, please fill correct email data"
		return render(request,'form.html',{'SendEmailform':SendEmailform,"message":message})
	else:
		SendEmailform = SendEmailForm()
		return render(request,'form.html',{'SendEmailform':SendEmailform})




def Email(userlist,subject,body):
	tag_open = """<pre style = "font-family:Arial">"""
	tag_close = """</pre>"""
	tag_open+= body
	tag_open+=tag_close 
	tag_open+=Body
	body = tag_open

	send_list = []
	errorlist = []
	for user in userlist:
		email1 = user.email.emailid
		email = EmailMessage(subject,body,to=[email1])
		email.content_subtype = "html"
		try:
			value = email.send()
			time.sleep(.3)
			send_list.append(email1)
		except:
			time.sleep(1)
			errorlist.append(email1)

	body+= " success mail  = "
	body +=str(send_list)
	body+= " error mail  = "
	body+= str(errorlist)

	email = EmailMessage(subject,body,to=admin)
	email.content_subtype = "html"
	email.send()
			
