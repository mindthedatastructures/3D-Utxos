import random
import math
from functools import reduce
from enum import Enum

random.seed(111)

class Scene():
    def generate(configs):
        scene = Scene()
        scene.blockchain.populate()
        scene.cementery.init()
        LivingBoard.UTXOS_PER_LINE = configs['living_utxos_per_line']

        return scene

    def __init__(self):
        self.createBoards()
        self.listeners = []

    def createBoards(self):
        # TX Flow
        self.transaction_queue = TransactionQueue(self)
        self.validator = Validator(self)
        self.trash = Trash(self)

        # Block Flow
        self.preparing_block = PreparingBlock(self)
        self.blockchain = Blockchain(self)

        # UTXO Flow (nothing to do, included in TX)

        # RX Flow
        self.rx_validated_tx_board = RxValidatedTxBoard(self)
        self.rx_in_new_block_board = RxInNewBlockBoard(self)
        self.living_board = LivingBoard(self)
        self.limbo = Limbo(self)
        self.cementery = Cementery(self)


    def model_changed(self):
        for l in self.listeners:
            l.model_changed()

    def print(self, mode=0):
        print('####################################################################################')
        print('Scene')
        if mode == 1:
            self.transaction_queue.print()
            self.validator.print()
            self.preparing_block.print()
            self.trash.print()
        if mode == 2:
            self.blockchain.print(2)
            self.transaction_queue.print()
            self.validator.print()
            self.preparing_block.print()
            self.trash.print()
        else:
            self.transaction_queue.print()
            self.validator.print()
            self.trash.print()
            self.preparing_block.print()
            self.blockchain.print()
            self.rx_validated_tx_board.print()
            self.rx_in_new_block_board.print()
            self.living_board.print()
            self.limbo.print()
            self.cementery.print()

    def getAliveUtxos(self):
        return self.living_board.getAliveUtxos()

####################################################
# OBJECTS
####################################################

class Block():
    def __init__(self):
        self.txs = []
        self.prev = None
        self.index = -1
        self.listeners = []
    def model_changed(self):
        for l in self.listeners:
            l.model_changed()
    def print(self):
        print(f'\t\tTransactions : {len(self.txs)}')
        for tx in self.txs:
            tx.print()

class Transaction():
    def __init__(self):
        self.ins = []
        self.outs = []
        self.block = None
        self.index = -1
        self.listeners = []
    def model_changed(self):
        for l in self.listeners:
            l.model_changed()
    def print(self):
        res = f"Tx #{self.index}\tins:[{', '.join([str(u.index) for u in self.ins])}], outs:[{', '.join([str(u.index) for u in self.outs])}]"
        print(f'\t\t\t{res}')

class Utxo():
    class States(Enum):
        StateBeforeBorn = 1
        StateAlive = 2
        StateBeforeDie = 3
        StateDead = 4
    def __init__(self):
        self.index = -1
        self.state = Utxo.States.StateBeforeBorn
        self.rx = Reflection()
        self.rx.u = self
        self.tx_of_born = None
        self.tx_of_death = None
        self.listeners = []
    def model_changed(self):
        for l in self.listeners:
            l.model_changed()

class Reflection():
    def __init__(self):
        self.u = None
        self.listeners = []
    def model_changed(self):
        for l in self.listeners:
            l.model_changed()

####################################################
# BOARDS
####################################################

####################
# TX FLOW
class TransactionQueue():
    class States(Enum):
        Loading = 1
        Ready = 2
        SendingToValidator = 3
    def __init__(self, scene):
        self.scene = scene
        self.txs = []
        self.listeners = []
        self.state = TransactionQueue.States.Ready
    def model_changed(self):
        for l in self.listeners:
            l.model_changed()

    def print(self):
        print('----------------------------------------')
        print('TransactionQueue')
        for tx in self.txs:
            tx.print()

    def addTransaction(self,tx):
        self.txs.append(tx)

    def getNext(self):
        try:
            return self.txs.pop(0)
        except:
            return None
class Validator():
    class States(Enum):
        LoadedNonTestedState = 1
        LoadingTransactionState = 2
        LoadedValidTxState = 3
        Validating = 4
        LoadedInvalidTxNotValidUtxoState = 4
        LoadedInvalidTxUtxoAlreadyInBlockState = 5
        DispatchingState = 7
        EmptyState = 8
    ValidatedStates = [States.LoadedValidTxState,States.LoadedInvalidTxNotValidUtxoState,States.LoadedInvalidTxUtxoAlreadyInBlockState]

    class Events(Enum):
        DispatchEvent = 9

    def __init__(self, scene):
        self.scene = scene
        self.state = Validator.States.EmptyState
        self.tx=None
        self.listeners = []
    def model_changed(self, event):
        for l in self.listeners:
            l.model_changed(event)

    def print(self):
        print('----------------------------------------')
        print('Validator')
        print(f'\tState : {self.state}')
        if self.tx:
            self.tx.print()

    def finishLoadNextTransaction(self):
        self.tx = self.scene.transaction_queue.getNext()
        if self.tx:
            self.state = Validator.States.LoadedNonTestedState
            self.scene.rx_validated_tx_board.add(self.tx.outs)
        else:
            self.state = Validator.States.EmptyState


    def validateTransaction(self):
        if self.state != Validator.States.LoadedNonTestedState or self.tx == None:
            raise Exception(f'Already Validated or Not Loaded. tx:{str(self.tx)} , state:{self.state}')
        alives = self.scene.living_board.getAliveUtxos()
        print([u.index for u in self.tx.ins])
        print([u.index for u in alives])
        tx_used_in_prepared_block = reduce(lambda res, tx: res+tx.ins , self.scene.preparing_block.block.txs, [])
        check1 = all(u in alives for u in self.tx.ins)
        check2 = not any(u in tx_used_in_prepared_block for u in self.tx.ins)
        if not check1:
            self.state = Validator.States.LoadedInvalidTxNotValidUtxoState
        elif not check2:
            self.state = Validator.States.LoadedInvalidTxUtxoAlreadyInBlockState
        else:
            self.state = Validator.States.LoadedValidTxState

    def dispatch(self):
        if self.state not in Validator.ValidatedStates or self.tx == None:
            self.scene.print()
            raise Exception(f'Dispatching something on wrong state')
        tx = self.tx
        self.tx = None
        if self.state == Validator.States.LoadedValidTxState:
            self.scene.preparing_block.addTransaction(tx)
        else:
            self.scene.trash.txs.append(tx)
        self.state = Validator.States.EmptyState
        self.model_changed(Validator.Events.DispatchEvent)

class Trash():
    def __init__(self, scene):
        self.scene = scene
        self.txs=[]
        self.listeners = []
    def model_changed(self):
        for l in self.listeners:
            l.model_changed()
            
    def print(self):
        print('----------------------------------------')
        print('Trash')
        for tx in self.txs:
            tx.print()

####################
# BLOCK FLOW
class PreparingBlock():
    class States(Enum):
        ReadyToIncludeTransactions = 0
        LoadingBlockToChain = 1

    def __init__(self, scene):
        self.scene = scene
        self.block = Block()
        self.listeners = []
        self.state = PreparingBlock.States.ReadyToIncludeTransactions
    def model_changed(self):
        for l in self.listeners:
            l.model_changed()

    def print(self):
        print('----------------------------------------')
        print('PreparingBlock')
        self.block.print()

    def addTransaction(self, tx):
        self.block.txs.append(tx)

    def loadBlock(self):
        block = self.block
        self.scene.blockchain.addBlock(block)
        self.block = Block()
        self.state = PreparingBlock.States.ReadyToIncludeTransactions

class Blockchain():
    def __init__(self, scene):
        self.scene = scene
        # the block with lower index, is the latest block
        self.blocks = []
        self.last_block_id = -1
        self.last_tx_id = -1
        self.last_utxo_id = -1
        self.listeners = []
    def model_changed(self):
        for l in self.listeners:
            l.model_changed()


    def addBlock(self, block):
        # UPDATING IDS
        all_u_ins  = reduce(lambda res, tx: res+tx.ins, block.txs, [])
        all_u_outs = reduce(lambda res, tx: res+tx.outs, block.txs, [])
        
        self.last_block_id += 1
        block.index = self.last_block_id
        for tx in block.txs:
            self.last_tx_id += 1
            tx.index = self.last_tx_id
            for u in tx.outs:
                self.last_utxo_id += 1
                u.index = self.last_utxo_id
        
        # APPENDING BLOCKS
        if len(self.blocks) == 0:
            self.blocks = [block]
        else:
            block.prev = self.blocks[0]
            self.blocks = [block] + self.blocks
        self.scene.living_board.load_update(all_u_ins, all_u_outs)

    def getAliveUtxos(self):
        res = []
        for b in self.blocks:
            for t in b.txs:
                for u in t.outs:
                    if u.state == Utxo.States.StateAlive:
                        res.append(u)
        return res 
    def getDeadUtxos(self):
        res = []
        for b in self.blocks:
            for t in b.txs:
                for u in t.outs:
                    if u.state == Utxo.States.StateDead:
                        res.append(u)
        return res 

    def select_k_utxos_to_consume(self,k):
        selected = random.sample(self.getAliveUtxos(), k)
        return selected


    def populate(self):
        b = Block()
        for i in range(4):
            tx = Transaction()
            b.txs.append(tx)
            tx.block = b
            for j in range(2):
                utxo = Utxo()
                utxo.tx_of_born = tx
                utxo.state = Utxo.States.StateAlive
                tx.outs.append(utxo)
        self.addBlock(b)
        self.scene.living_board.update()

        #Block 1 : 4 tx with 2 utxos each
        for p in range(25):
            b = Block()
            utxos_to_consume = self.select_k_utxos_to_consume(4)
            for i in range(2):
                tx = Transaction()
                b.txs.append(tx)
                tx.block = b
                for j in range(2):
                    utxo = Utxo()
                    utxo.tx_of_born = tx
                    utxo.state = Utxo.States.StateAlive
                    tx.outs.append(utxo)
                for j in range(2):
                    u = utxos_to_consume.pop()
                    u.state = Utxo.States.StateDead
                    u.tx_of_death = tx
                    tx.ins.append(u)
            self.addBlock(b)
            self.scene.living_board.update()


    def populateOld(self):
        # 25 utxos
        # 20 tx
        #     16 tx with 1 utxo
        #     3 tx with 2 utxo
        #     1 tx with 3 utxo
        # 5 blocks
        # b1: 4 tx
        # b2: 3 tx
        # b3: 4 tx
        # b4: 5 tx
        # b5: 4 tx

        def addOneUtxoToTransaction(tx, utxos):
            utxo = utxos.pop()
            tx.outs.append(utxo)
            utxo.tx_of_born = tx

        utxos = []
        for i in range(25):
            utxo = Utxo()
            utxo.state = Utxo.States.StateAlive
            utxos.append(utxo)

        txs=[]
        for i in range(20):
            txs.append(Transaction())

        specials = random.choices(txs, k=4)
        for tx in txs:
            addOneUtxoToTransaction(tx, utxos)
            if tx in specials:
                addOneUtxoToTransaction(tx, utxos)
                if tx == specials[-1]:
                    addOneUtxoToTransaction(tx, utxos)
        for i in range(5):
            b = Block()
            # 4 3 4 5 4
            if i in [0,2,4]:
                tx_count = 4
            elif i == 1:
                tx_count = 3
            elif i == 3:
                tx_count = 5
            for q in range(tx_count):
                tx = txs.pop()
                b.txs.append(tx)
                tx.block = b
            self.addBlock(b)
            self.scene.living_board.update()

    def print(self, mode=0):
        print('----------------------------------------')
        print('Blockchain')
        for i in range(len(self.blocks)):
            ii = len(self.blocks) -1 -i
            print(f'\t Block #{i}')
            if mode != 2:
                self.blocks[ii].print()

####################
# RX FLOW
class RxInNewBlockBoard():
    def __init__(self, scene):
        self.scene = scene
        self.us = []
        self.listeners = []
    def model_changed(self):
        for l in self.listeners:
            l.model_changed()
    def print(self):
        print('----------------------------------------')
        print('Utxos In New Block')

class RxValidatedTxBoard():
    def __init__(self, scene):
        self.scene = scene
        self.rxs = []
        self.listeners = []
    def add(self, rxs):
        self.rxs = rxs
    def model_changed(self):
        for l in self.listeners:
            l.model_changed()
    def print(self):
        print('----------------------------------------')
        print('Utxos In Validated Tx')

class LivingBoard():
    class States(Enum):
        UpdatedState   = 0
        ToUpdateState =1
    UTXOS_PER_LINE = -1
    def __init__(self, scene):
        self.scene = scene

        self.reflexes = []
        self.pendingRexToAdd = []
        self.pendingRexToRemove = []
        self.state = LivingBoard.States.UpdatedState

        self.view = None
        self.listeners = []
    def model_changed(self):
        for l in self.listeners:
            l.model_changed()

    def getAliveUtxos(self):
        return [r.u for r in self.reflexes]

    def print(self):
        print('----------------------------------------')
        print('LivingBoard')
        print(f'\tstate: {self.state}')
        ids = [str(r.u.index) for r in self.reflexes]
        lines = math.ceil( (1.0*len(ids)) / LivingBoard.UTXOS_PER_LINE)
        for l in range(lines):
            k1 = l*LivingBoard.UTXOS_PER_LINE
            k2 = (l+1)*LivingBoard.UTXOS_PER_LINE
            print('[' + ',\t'.join(ids[k1:k2]) + ']')

    def load_update(self, all_u_ins, all_u_outs):
        self.state = LivingBoard.States.ToUpdateState
        self.pendingRexToAdd += [u.rx for u in all_u_outs]
        self.pendingRexToRemove += [u.rx for u in all_u_ins]

    def update(self):
        self.scene.limbo.add(self.pendingRexToRemove)
        for r in self.pendingRexToRemove:
            self.reflexes.remove(r)
        self.reflexes += self.pendingRexToAdd
        self.pendingRexToAdd = []
        self.pendingRexToRemove = []
        self.state = LivingBoard.States.UpdatedState


class Limbo():
    def __init__(self, scene):
        self.scene = scene
        self.rxs=[]
        self.listeners = []
    def model_changed(self):
        for l in self.listeners:
            l.model_changed()
    def add(self,rxs):
        self.rxs = rxs
    def update(self):
        self.scene.cementery.send_to_cementery(self.rxs)
        self.rxs = []
    def print(self):
        print('----------------------------------------')
        print('Limbo')
        print('\t[' + ', '.join([str(r.u.index) for r in self.rxs]) + ']')

class Cementery():
    def __init__(self, scene):
        self.scene = scene
        self.rxs = []
        self.listeners = []
    def model_changed(self):
        for l in self.listeners:
            l.model_changed()

    def send_to_cementery(self, rxs):
        self.rxs += rxs

    def init(self):
        self.send_to_cementery(self.scene.blockchain.getDeadUtxos())

    def print(self):
        print('----------------------------------------')
        print('Cementery')
        print('\t[' + ', '.join([str(r.u.index) for r in self.rxs]) + ']')


