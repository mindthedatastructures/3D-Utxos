
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
import socket

import json

import requests
import signal

# import tkthread; tkthread.patch()

class CommandUI(Tk):
    def __init__(self):
        super(CommandUI, self).__init__()

        self.title("Commands")
        self.minsize(800,100)
        with open('config.json', 'r') as f:
            config = json.loads(f.read())
            self.commands_address = config['commands']['address']
            self.commands_port = config['commands']['port']
            self.get_info_address = config['get_info']['address']
            self.get_info_port = config['get_info']['port']

        self.commands_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.get_info_session = requests.Session()

        self.initUi()

    def initUi(self):

        self.initAddTxFrame()

        loadNextTx_button = Button(self, text="Load Next Transaction to Validator", command=lambda:self.sendCommand('LoadNextTransactionToValidatorCommand'))
        loadNextTx_button.grid(row=1,column=0)
        validateTx_button = Button(self, text="Validate Transaction", command=lambda:self.sendCommand('ValidateTransactionCommand'))
        validateTx_button.grid(row=2,column=0)
        dispatchValidator_button = Button(self, text="Dispatch Validator", command=lambda:self.sendCommand('ValidatorDispatchTxCommand'))
        dispatchValidator_button.grid(row=3,column=0)
        addBlockToChain_button = Button(self, text="Add Block To Chain", command=lambda:self.sendCommand('AddBlockToChainCommand'))
        addBlockToChain_button.grid(row=4,column=0)
        updateLivingView_button = Button(self, text="Update Living UTXO View", command=lambda:self.sendCommand('UpdateLivingViewCommand'))
        updateLivingView_button.grid(row=5,column=0)
        updateLimbo_button = Button(self, text="Update Limbo", command=lambda:self.sendCommand('UpdateLimboCommand'))
        updateLimbo_button.grid(row=6,column=0)
        changeTxDisplayMode_button = Button(self, text="Change display TX Mode", command=lambda:self.sendCommand('ChangeTxDisplayModeCommand'))
        changeTxDisplayMode_button.grid(row=1,column=1)


    def initAddTxFrame(self):
        add_tx_frame = Frame(self)
        add_tx_frame.grid(row=0,column=0)
        add_tx_title_label = Label(add_tx_frame, text="Add Transaction To Queue")
        add_tx_title_label.grid(row=0,column=0, columnspan=4)

        alive_utxos_title_label = Label(add_tx_frame, text="Alive Utxos")
        alive_utxos_title_label.grid(row=1,column=0, rowspan=2)

        self.alive_tx_var = StringVar()
        alive_utxo_label = Label(add_tx_frame, textvariable=self.alive_tx_var)
        alive_utxo_label.grid(row=1,column=1, columnspan=3)
        
        update_alive_utxo_button = Button(add_tx_frame, text="Update Alive Utxo List", command=self.update_alive_utxo_list, width = 60)
        update_alive_utxo_button.grid(row=2,column=1, columnspan=3)

        inputs_frame = Frame(add_tx_frame)
        inputs_frame.grid(row=3,column=0, columnspan=4)

        intput_utxo_label = Label(inputs_frame, text="Input Utxo (example: '1,43')")
        intput_utxo_label.grid(row=0,column=0)
        self.input_utxo_var = StringVar()
        input_utxo_entry = Entry(inputs_frame, textvariable=self.input_utxo_var, width=10)
        input_utxo_entry.grid(row=0,column=1)
        
        output_utxo_count_label = Label(inputs_frame, text="Output Utxo Count")
        output_utxo_count_label.grid(row=0,column=2)
        self.output_utxo_count_var = StringVar()
        output_utxo_count_entry = Entry(inputs_frame, textvariable=self.output_utxo_count_var, width=10)
        output_utxo_count_entry.grid(row=0,column=3)

        send_add_tx_button = Button(add_tx_frame, text="Send Transaction", command=self.sendTransaction)
        send_add_tx_button.grid(row=4,column=0, columnspan=3)
        self.error_send_tx_var = StringVar()
        error_send_tx_entry = Label(add_tx_frame, textvariable=self.error_send_tx_var)
        error_send_tx_entry.grid(row=4,column=3)



    def sendTransaction(self):
        self.error_send_tx_var.set('')
        is_error=True
        try:
            ns = self.input_utxo_var.get().split(',')
            intputs = [int(i) for i in ns]
            output_count = int(self.output_utxo_count_var.get())
            is_error=False
        except Exception as e:
            is_error=True
            print(e)
            self.error_send_tx_var.set(f'error {str(e)}')
        if not is_error:
            self.sendCommand('AddToQueueTransactionCommand', [intputs, output_count])

    def buttonPressed(self, button_no):
        if button_no %2 == 0:
            self.sendCommand(f"button{str(button_no)} pressed")
        else:
            msg='{"Hello":"World"}'
            headers = {'Content-type': 'application/json'}
            print(f"sending {msg}")
            res = self.get_info_session.get(f'http://{self.get_info_address}:{self.get_info_port}', msg, headers = headers).text
            

    def update_alive_utxo_list(self):
        msg='{"request":"get_alive_utxos"}'
        headers = {'Content-type': 'application/json'}
        res = self.get_info_session.post(f'http://{self.get_info_address}:{self.get_info_port}', msg, headers = headers).text
        self.alive_tx_var.set(res)

    def sendCommand(self, cmd, params=[]):
        msg = json.dumps({'command':cmd, 'params':params})
        print(f'Sending: {msg}')
        self.commands_sock.sendto(bytes(msg, 'utf-8'), (self.commands_address,self.commands_port))



def handler_exit(signum, frame):
    root.get_info_session.close()
    exit(0)

signal.signal(signal.SIGINT, handler_exit)

root = CommandUI()
root.mainloop()
