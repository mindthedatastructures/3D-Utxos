import socket
import threading
import json
import traceback


from commands.commands import *

class CommandReceiver():
    def __init__(self, command_manager):
        self.cm = command_manager
        self.keep_running = True
        t = threading.Thread(target=self.start, args=[])
        t.start()

    def start(self):
        with open('config.json', 'r') as f:
            config = json.loads(f.read())
            address = config['commands']['address']
            port = config['commands']['port']

        self.serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serverSock.bind((address,port))
        print(f'starting {address} {port}')
        while self.keep_running:
            data, addr = self.serverSock.recvfrom(1024)
            msg = data.decode('utf-8')
            print(f'{msg}')
            self.process_command_request(msg)

    def close(self):
        print('closing command receiver server')
        self.serverSock.close()
        self.keep_running = False
        print('Done!')

    def process_command_request(self,msg):
        req = json.loads(msg)
        cmd_str = req['command']
        params = req['params']
        try:
            if cmd_str == 'AddToQueueTransactionCommand':
                self.cm.execute(AddToQueueTransactionCommand(params[0],params[1]))
            elif cmd_str == 'LoadNextTransactionToValidatorCommand':
                self.cm.execute(LoadNextTransactionToValidatorCommand())
            elif cmd_str == 'ValidateTransactionCommand':
                self.cm.execute(ValidateTransactionCommand())
            elif cmd_str == 'ValidatorDispatchTxCommand':
                self.cm.execute(ValidatorDispatchTxCommand())
            elif cmd_str == 'AddBlockToChainCommand':
                self.cm.execute(AddBlockToChainCommand())
            elif cmd_str == 'UpdateLivingViewCommand':
                self.cm.execute(UpdateLivingViewCommand())
            elif cmd_str == 'UpdateLimboCommand':
                self.cm.execute(UpdateLimboCommand())
            elif cmd_str == 'ChangeTxDisplayModeCommand':
                self.cm.execute(ChangeTxDisplayModeCommand())
            else:
                raise Exception('Invalid Command')
        except Exception as e:
            print(traceback.format_exc())
            print(e)
    


















