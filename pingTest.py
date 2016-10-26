#!/usr/bin/python
import platform
import subprocess
from time import sleep
from tkinter import *
from tkinter import messagebox


addresses = {
             '10.252.50.150': (185, 300, 'plc'),
             '10.252.50.151': (185, 218, 'hmi'),
             '10.252.50.152': (320, 300, 'icam'),
             '10.252.50.153': (190, 125, 'serv'),
             '10.252.50.154': (320, 125, 'serv'),
             '10.252.50.155': (388, 125, 'bcam'),
             '10.252.50.156': (545, 125, 'bcam'),
             '10.252.50.157': (455, 125, 'hmi'),
             '10.252.50.158': (185, 555, 'nj'),
             '10.252.50.190': (695, 555, 'pc'),
             '10.252.50.191': (805, 455, 'scam'),
             '10.252.50.192': (635, 455, 'scam'),
             '10.252.50.193': (800, 555, 'lprnt'),
             '10.252.50.194': (630, 555, 'lprnt'),
             '10.252.50.1': (675, 165, 'gway'),
             '10.252.1.34': (785, 130, 'db')
             }
hosts = []
stopped = False


class Host:
    def __init__(self, ip, data):
        self.ip = ip
        self.status = 'down'
        self.image_x = data[0]
        self.image_y = data[1]
        self.type = data[2]
        self.image = 'images/' + str(self.type) + str(self.status) + ".gif"
        self.filename = ''

    def update_image(self):
        self.image = 'images/' + str(self.type) + str(self.status) + ".gif"

    def update_filename(self, filename):
        self.filename = filename


def ping(host):

    response = ping_it(host.ip)
    if response:
        host.status = 'up'
        host.update_image()
    else:
        host.status = 'down'
        host.update_image()


def ping_it(host):
    # Ping parameters as function of OS
    ping_str = "-n 1" if platform.system().lower() == "windows" else "-c 1"
    # Ping
    try:
        if subprocess.check_call("ping " + ping_str + " " + host, stdout=subprocess.PIPE) == 0:
            return True
    except:
        return False


def on_closing():
    global stopped
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        stopped = True
        top.destroy()


top = Tk()
top.wm_title("Ethernet Device Status")
top.protocol("WM_DELETE_WINDOW", on_closing)
C = Canvas(top, bg="white", height=600, width=900)
C.pack()
b_ground = PhotoImage(file='images/background.gif')
C.create_image(0, 0, anchor=NW, image=b_ground)
monitor = PhotoImage(file='images/terminal.gif')
C.create_image(252, 125, anchor=SW, image=monitor)
switch = PhotoImage(file='images/switchup.gif')
C.create_image(435, 215, anchor=SW, image=switch)
C.create_image(690, 360, anchor=SW, image=switch)
C.create_image(435, 425, anchor=SW, image=switch)
for address in addresses:
    address = Host(address, addresses[address])
    hosts.append(address)
for host in hosts:
    host.update_filename(PhotoImage(file=host.image))
    C.create_image(host.image_x, host.image_y, anchor=SW, image=host.filename)
index = 0
while not stopped:
    sleep(0.5)
    host = hosts[index]
    ping(host)
    host.update_filename(PhotoImage(file=host.image))
    if not stopped:
        C.create_image(host.image_x, host.image_y, anchor=SW, image=host.filename)
    index += 1
    index %= len(hosts)
    top.update_idletasks()
    top.update()
