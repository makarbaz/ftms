from django.shortcuts import render
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login
from django.db.models import Count
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message,MessageUpdate
import json
from django.http import HttpResponse
import uuid


def loginpage(request):
    if request.method =='POST':
        username=request.POST.get('userName')
        pass1=request.POST.get('password')
        user = auth.authenticate(request,username=username, password=pass1)
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            return redirect('login')  
    return render(request, 'login.html',)


@login_required(login_url='login')

def send_message(request):  #recipient_id
    send=User.objects.all()
    if request.method == 'POST':
        reciver = request.POST['recipient']
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        sender = User.objects.get(id=request.user.id)
        rec = User.objects.get(id=reciver)
        message = Message(sender=sender, recipient=rec, subject=subject, body=body)
        message.save()
        pop = Message.objects.filter().last()
        return render(request, 'send_message.html', {'users' : send ,"popup" : pop})
        
    return render(request, 'send_message.html', {'users' : send })



@login_required(login_url='login')
def read_message(request):
    received_messages = Message.objects.filter(recipient=request.user)
    if request.method == 'POST':
        forward_to_user_id = request.POST.get('forward_to_user')
        selected_messages_ids = request.POST.getlist('selected_messages')
        forward_to_user = User.objects.get(id=forward_to_user_id)
        selected_messages = Message.objects.filter(id__in=selected_messages_ids)
        aa=MessageUpdate(order_id=int(Message.objects.filter(recipient=request.user)[0].id +1),update_desc=request.user,delivered=True)     
        aa.save()
        for message in selected_messages:
            Message.objects.create(
                sender=request.user,
                recipient=forward_to_user,
                subject=message.subject,
                body=message.body,
            )
            message.delete()
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'read_message.html', {'received_messages': received_messages, 'users': users})


#------tracker----#

@login_required(login_url='login')
def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId')
        try:
            order = Message.objects.filter(id=int(orderId))
            if len(order)>0:
                update = MessageUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps(updates, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse(f'{len(order)}')
        except Exception as e:
            return HttpResponse(f'exception {e}')

    return render(request,'tracker.html' )

    


#############inbox###########
    
@login_required(login_url='login')
def inbox(request):
    if 'q' in request.GET:
        q =request.GET['q']
        messages = Message.objects.filter(sender__icontains=q)
    else:
          messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
          
    return render(request,'inbox.html',{'count':messages})



@login_required(login_url='login')
def home(request):
    return render(request,'base.html')

def track(request):
    return render(request,'tracker.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


