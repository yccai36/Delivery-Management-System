from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
import json
from .models import User
from django.utils import timezone
import time as Time
import subprocess
import socket
import sys
import pickle
from django.http import JsonResponse

def index(request):
    return render(request, 'deliveree/index.html')

@csrf_exempt
def form(request):
    if request.method=='POST':
            received_json_data=json.loads(request.body.decode("utf-8"))
    # print(received_json_data)
    firstname = received_json_data['firstname']
    lastname = received_json_data['lastname']
    contact = received_json_data['contact']
    address = received_json_data['address']
    date = received_json_data['date']
    time = received_json_data['time']
    lat = received_json_data['lat']
    lng = received_json_data['lng']
    distance = calculateDistance(float(lat), float(lng))
    print(distance)
    user_info = User(firstname = firstname, lastname = lastname, contact = contact, address = address, date = date, time = time, pub_time = timezone.now(), status = False, lat = lat, lng = lng, distance = distance)
    name = firstname + " " + lastname
    title = ""
    message = {"!New Order!": title, "Name" : name,"Address" : address,"Date":date,"Time":time,"Contact":contact}
    accept = tcpConn(message)
    if(accept):
        user_info.save()
        print("Suceess fully saved "+ firstname + " "+ lastname)
    else:
        print("Order rejected")
    # return HttpResponse(received_json_data['firstname'])
    return JsonResponse({'status':'ok'}) if accept else JsonResponse({'status':'reject'})

def tcpConn(message):
    # Create a TCP/IP socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_address = ('localhost', 10000)
        print('starting up on {} port {}'.format(*server_address))
        sock.bind(server_address)
        sock.listen(1024)
    except socket.error as msg:
        print(msg)
        return False
    # Listen for incoming connections
    data = ''
    while (len(data) == 0):
        # Wait for a connection
        print('waiting for a connection')
        connection, client_address = sock.accept()
        print('connection from', client_address)
        message = pickle.dumps(message)
        connection.sendall(message)
        try:
            data = connection.recv(256)
            print('received {!r}'.format(data))
            if(data == b"Success"):
                print("Accept order")
                return True
            else:
                print("Decline order")
                return False
        finally:
            # Clean up the connection
            connection.close()

def calculateDistance(lat, lng):
    from math import sin, cos, sqrt, atan2, radians
    # approximate radius of earth in km
    R = 6373.0
    lat = radians(lat)
    lng = radians(lng)
    lat2 = radians(42.4406)
    lng2 = radians(-76.4966)

    dlon = lng2 - lng
    dlat = lat2 - lat

    a = sin(dlat / 2)**2 + cos(lat) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance
