from django.shortcuts import render, redirect
from chat.models import Room, Message
from django.http import HttpResponse, JsonResponse
from .producer import publish
from .consumer import consumer
import pika
import sys
global message
message =""
# Create your views here.
"""import threading

import pika
from django.conf import settings


class AMQPConsuming(threading.Thread):
    def callback(self, ch, method, properties, body):
        # do something
        print(" [x] Received %r" % body)

    @staticmethod
    def _get_connection():
        parameters = pika.URLParameters(settings.RABBIT_URL)
        return pika.BlockingConnection(parameters)

    def run(self):
        connection = self._get_connection()
        channel = connection.channel()

        channel.queue_declare(queue='task_queue6')
        print('Hello world! :)')

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(self.callback, queue='queue')

        channel.start_consuming()

def ready(self):
    if not settings.IS_ACCEPTANCE_TESTING and not settings.IS_UNITTESTING:
        consumer = AMQPConsuming()
        consumer.daemon = True
        consumer.start()"""
def home(request):
    return render(request, 'home.html')

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/room/'+room)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/room/'+room)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']
    publish(message)
    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})

def consumeMessage(request):
    #global username
    #global room
    print("\n\n\n\nhello\n\n\n")
    s= consumer()
    print("\n\n\n\nS is")
    print(s)
    d={'message': s}
    #print (str)
    #return render(request, 'room.html')
    #return HttpResponse("consumer successfully")
    return render(request,'cons.html', d)
 

#def publishMessage(request):
    #publish()
    #return HttpResponse('Message sent successfully')
