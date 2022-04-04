##################################################################
#
# INSPIRATION FROM https://github.com/GranielGran/Ricart-Agrawala
#
##################################################################

import sys
import socket
import random
import time
import threading
import json

DEBUG = False
class Process(threading.Thread):
    # STATES
    # 0 - DO-NOT-WANT
    # 1 - WANTED
    # 2 - HOLD

    def __init__(self, id):
        super().__init__()
        self.id = id
        self.state = 0
        self.timestamp = None
        self.cstime = [3, 5]
        self.ptime = [15, 25]
        # Keep IDs of processes we are waiting an answer from and waiting to answer
        self.request_queue = []
        self.reply_queue = []
        # Make it run on localhost
        self.localAddr = '127.0.0.1'
        self.proc_amount = None
        self.request_access = True
        # Thread for listening for receiving messages
        self.listener = threading.Thread(target=self.message_listener)

    def run(self):
        self.listener.setDaemon(True)
        self.listener.start()
        while True:
            if self.state == 0:
                sleep_time = random.randint(self.ptime[0], self.ptime[1])
                time.sleep(sleep_time)
                self.state = 1

            elif self.state == 1:
                # Ask for access from every process
                if self.request_access:
                    self.timestamp = time.time()
                    temp = []
                    # If there are other processes to send a message to
                    if self.proc_amount is not None and self.proc_amount > 1:
                        for i in range(1, self.proc_amount + 1):
                            if i != self.id:
                                # Add the processes we are waiting a reply from
                                self.request_queue.append(i)
                                temp.append(i)
                        # Make sure every process gets a request message
                        # Sometimes for-cycle is not enough and messages get lost
                        while temp:
                            for i in temp:
                                message = {'type': 'request', 'timestamp': self.timestamp, 'id': self.id}
                                self.send_message(message, i)
                                temp.remove(i)
                    if DEBUG:
                        print(f'DEBUG: {self.id} requested acces from: {self.request_queue}')
                    self.request_access = False

                # If there are requests in the queue which haven't gotten a reply (list not empty)
                if self.request_queue:
                    continue

                self.state = 2
                self.request_access = True

            else:
                if DEBUG:
                    print(f'DEBUG: {self.id} ENTERING CS')
                sleep_time = random.randint(self.cstime[0], self.cstime[1])
                time.sleep(sleep_time)
                self.state = 0
                while self.reply_queue:
                    for i in self.reply_queue:
                        if DEBUG:
                            print(f'DEBUG: CS TIME END. {self.id} sending OK to {i}')
                        self.send_message({'type': 'reply', 'msg': 'OK', 'id': self.id}, i)
                        self.reply_queue.remove(i)
                if DEBUG:
                    print(f'DEBUG: CS TIME END FOR {self.id}')
                self.timestamp = None

    # A separate thread is going to listen for messages
    def message_listener(self):
        listen = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        listen.bind((self.localAddr, 5550+self.id))

        while True:
            # When we get a message, handle it
            message = listen.recv(4096)
            self.message_handler(message)

    def send_message(self, message, address):
        sending = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sending.connect((self.localAddr, 5550+address))
        encode_data = json.dumps(message, indent=2).encode('utf-8')
        sending.send(encode_data)
        sending.close()

    def message_handler(self, message):
        # Decode from bytes
        message = eval(message.decode("utf-8"))
        if message['type'] == 'request':
            # This process has an advantage, do not reply to request until the CS is used
            if (self.timestamp is not None and message['timestamp'] > self.timestamp and self.state == 1) or self.state == 2:
                # Queue processes that we have to notify after using the CS
                self.reply_queue.append(message['id'])
            else:
                # The other process has an advantage
                if DEBUG:
                    print(f'DEBUG: {self.id} with state {self.state} sending OK to {message["id"]}')
                return_message = {'type': 'reply', 'msg': 'OK', 'id': self.id}
                self.send_message(return_message, message['id'])

        # Got a reply to the process' request
        if message['type'] == 'reply':
            if DEBUG:
                print(f'DEBUG: {self.id} deleting from request queue: {message["id"]}')
            try:
                self.request_queue.remove(message['id'])
            except Exception as e:
                print(e)
                exit()


def list(threads):
    # utility method to list threads
    for t in threads:
        if t.state == 1:
            state = "WANTED"
        elif t.state == 2:
            state = "HOLD"
        else:
            state = "DO-NOT-WANT"
        print(f'P{t.id}, {state}')


def cstime(input):
    if input < 10:
        print("Input must be greater or equal to 10")
        return
    for t in threads:
        t.cstime = [10, input]


def ptime(input):
    if input < 5:
        print("Input must be greater or equal to 5")
        return
    for t in threads:
        t.ptime = [5, input]


# main program function
if __name__=='__main__':

    pid = 1
    threads = []

    if len(sys.argv) > 1:
        try:
            if (int(sys.argv[1]) < 1):
                print("Input is smaller than 1")
                exit()
            for i in range(int(sys.argv[1])):
                t = Process(pid)
                threads.append(t)
                t.setDaemon(True)
                pid += 1
                t.start()

            for t in threads:
                t.proc_amount = len(threads)

        except Exception as e:
            print(e)
            exit()
    else:
        print("No input provided")
        exit()

    print("Commands: list, time-cs t, time-p t, exit ")

    # start the main loop
    running = True

    while running:
        inp = input().lower()
        cmd = inp.split(" ")

        command = cmd[0]

        if len(cmd) > 2:
            print("Too many arguments")

        elif command == "exit":
            running = False

        elif command == "list":
            try:
                list(threads)
            except Exception as e:
                print(e)

        elif command == "time-cs":
            try:
                cstime(int(cmd[1]))
            except:
                print("Error")

        elif command == "time-p":
            try:
                ptime(int(cmd[1]))
            except:
                print("Error")

        else:
            print("Unsupported command:", inp)

    print("Program exited")
