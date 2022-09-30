from model.models import *
from views.views import *
import time

class EditPart():
    def __init__(self):
        self.model = None
        self.view = None
    def model_changed(self):
        None

class SceneEditPart():
    def generate(scene_model, view_manager, animator, configs):
        scene_edit_part = SceneEditPart(scene_model, view_manager, animator, configs)

        return scene_edit_part
    # Scene
    def __init__(self, scene_model, view_manager, animator, configs):
        self.model = scene_model
        self.view = None
        self.animator = animator
        self.model.listeners.append(self)
        self.view_manager = view_manager
        self.configs = configs

        self.txDisplayMode = 0

        # TX Flow
        self.transaction_queue_edit_part = TransactionQueueEditPart(self, scene_model.transaction_queue, view_manager)
        self.validator_edit_part = ValidatorEditPart(self, scene_model.validator, view_manager)
        self.trash_edit_part = TrashEditPart(self, scene_model.trash, view_manager)

        # Block Flow
        self.preparing_block_edit_part = PreparingBlockEditPart(self, scene_model.preparing_block, view_manager)
        self.blockchain_edit_part = BlockchainEditPart(self, scene_model.blockchain, view_manager)

        # UTXO Flow (nothing to do, included in TX)

        # RX Flow

        self.rx_validated_tx_board_edit_part = RxValidatedTxBoardEditPart(self, scene_model.rx_validated_tx_board, view_manager)
        self.rx_in_new_block_board_edit_part = RxInNewBlockBoardEditPart(self, scene_model.rx_in_new_block_board, view_manager)
        self.living_board_edit_part = LivingBoardEditPart(self, scene_model.living_board, view_manager)
        self.limbo_edit_part = LimboEditPart(self, scene_model.limbo, view_manager)
        self.cementery_edit_part = CementeryEditPart(self, scene_model.cementery, view_manager)


        self.blocks_edit_parts = []
        self.txs_edit_parts = []
        self.us_edit_parts = []
        self.rxs_edit_parts = []


        self.initObjectEditParts()

    def create_utxos_edit_parts(self, txs_model, tx_edit_part,  where_to_add_rxs_edit_parts=None):
        for u in txs_model:
            u_edit_part = UtxoEditPart(self,u)
            u_edit_part.tx_of_born_edit_part = tx_edit_part
            tx_edit_part.outs_edit_parts.append(u_edit_part)
            self.us_edit_parts.append(u_edit_part)

            rx_edit_part = ReflectionEditPart(self,u.rx)
            self.rxs_edit_parts.append(rx_edit_part)
            u_edit_part.rx_edit_part = rx_edit_part
            rx_edit_part.u_edit_part = u_edit_part
            if where_to_add_rxs_edit_parts != None:
                where_to_add_rxs_edit_parts.rxs_edit_parts.append(rx_edit_part)

    def create_transactions_edit_parts(self, txs_model, tx_holder_edit_part, where_to_add_rxs_edit_parts=None):
        for tx in txs_model:
            if tx == None:
                continue
            tx_edit_part = TransactionEditPart(self,tx)
            self.txs_edit_parts.append(tx_edit_part)
            tx_holder_edit_part.txs_edit_parts.append(tx_edit_part)
            tx_edit_part.tx_holder_edit_part = tx_holder_edit_part
            self.create_utxos_edit_parts(tx.outs, tx_edit_part, where_to_add_rxs_edit_parts)

    def create_blocks_edit_parts(self, blocks_model, block_holder_edit_part, isInBlockchain=False, where_to_add_rxs_edit_parts=None):
        for block in blocks_model:
            block_edit_part = BlockEditPart(self, block)
            self.blocks_edit_parts.append(block_edit_part)
            if isInBlockchain and len(self.blockchain_edit_part.blocks_edit_parts)>0 and block != self.blockchain_edit_part.blocks_edit_parts[-1]:
                self.blockchain_edit_part.blocks_edit_parts[-1].prev_edit_part = block_edit_part
            if isInBlockchain:
                self.blockchain_edit_part.blocks_edit_parts.append(block_edit_part)
            else:
                block_holder_edit_part.block_edit_part = block_edit_part
            self.create_transactions_edit_parts(block.txs, block_edit_part, where_to_add_rxs_edit_parts)
    def initObjectEditParts(self):
        # Block Flow
        # Init Blockchain Objects
        self.create_blocks_edit_parts(self.blockchain_edit_part.model.blocks, block_holder_edit_part=None, isInBlockchain=True)
        # updatetx_of_death_edit_part, and create ins_edit_parts
        for block_edit_part in self.blockchain_edit_part.blocks_edit_parts:
            for tx_edit_part in block_edit_part.txs_edit_parts:
                for u_edit_part in tx_edit_part.outs_edit_parts:
                    if u_edit_part.model.tx_of_death == None:
                        self.living_board_edit_part.rxs_edit_parts.append(u_edit_part.rx_edit_part)
                        continue
                    breakAll = False
                    for block_edit_part2 in self.blockchain_edit_part.blocks_edit_parts:
                        if breakAll: break
                        for tx_edit_part2 in block_edit_part2.txs_edit_parts:
                            if breakAll: break
                            if u_edit_part.model.tx_of_death == tx_edit_part2.model:
                                u_edit_part.tx_of_death_edit_part = tx_edit_part2
                                if u_edit_part.rx_edit_part.model in self.limbo_edit_part.model.rxs:
                                    self.limbo_edit_part.rxs_edit_parts.append(u_edit_part.rx_edit_part)
                                else:
                                    self.cementery_edit_part.rxs_edit_parts.append(u_edit_part.rx_edit_part)
                                breakAll = True
                for u in tx_edit_part.model.ins:
                    breakAll = False
                    for block_edit_part2 in self.blockchain_edit_part.blocks_edit_parts:
                        if breakAll: break
                        for tx_edit_part2 in block_edit_part2.txs_edit_parts:
                            if breakAll: break
                            for u_edit_part2 in tx_edit_part2.outs_edit_parts:
                                if breakAll: break
                                if u == u_edit_part2.model:
                                    tx_edit_part.ins_edit_part.append(u_edit_part2)

        self.create_blocks_edit_parts([self.preparing_block_edit_part.model.block], self.preparing_block_edit_part, isInBlockchain=False, where_to_add_rxs_edit_parts=self.rx_in_new_block_board_edit_part)
    # TX Flow
    # RX Flow
        self.create_transactions_edit_parts(self.transaction_queue_edit_part.model.txs, self.transaction_queue_edit_part)
        self.create_transactions_edit_parts([self.validator_edit_part.model.tx], self.validator_edit_part, self.rx_validated_tx_board_edit_part)
        self.create_transactions_edit_parts(self.trash_edit_part.model.txs, self.trash_edit_part, None)

    def initObjectViews(self):
        # Blockchain Views
        for block_edit_part in self.blockchain_edit_part.blocks_edit_parts:
            block_view = self.create_block_view(block_edit_part)
            if len(self.view_manager.blockchain_view.blocks_views) != 0:
                self.view_manager.blockchain_view.blocks_views[-1].prev_block_view = block_view
            self.view_manager.blockchain_view.blocks_views.append(block_view)
        self.blockchain_edit_part.updateChildrenPositions()
        # Preparing Block Views
        if self.preparing_block_edit_part.block_edit_part != None:
            block_view = self.create_block_view(self.preparing_block_edit_part.block_edit_part)
            self.view_manager.preparing_block_view.block_view = block_view
            self.preparing_block_edit_part.updateChildrenPositions()
        # Living Board Views
        for rx_edit_part in self.living_board_edit_part.rxs_edit_parts:
            rx_view = ReflectionView(rx_edit_part)
            rx_edit_part.view = rx_view
            self.view_manager.living_board_view.rxs_views.append(rx_view)
            self.view_manager.rxs_views.append(rx_view)
        self.living_board_edit_part.updateChildrenPositions()
        # Cementery Views
        for i, rx_edit_part in enumerate(self.cementery_edit_part.rxs_edit_parts):
            rx_view = ReflectionView(rx_edit_part)
            rx_edit_part.view = rx_view
            # self.view_manager.cementery_view.rxs_views.append(rx_view)
            pos = self.cementery_edit_part.view.getPosForIndex(i)
            rx_view.setPos(pos[0], pos[1], pos[2])
            rx_view.visible = True
            rx_view.setAlive(False)
            self.view_manager.rxs_views.append(rx_view)

        for block_edit_part in self.blockchain_edit_part.blocks_edit_parts:
            for tx_edit_part in block_edit_part.txs_edit_parts:
                tx_edit_part.initInterTxLinks()


    def create_block_view(self, block_edit_part):
        block_view = BlockView()
        block_edit_part.view = block_view
        self.view_manager.blocks_views.append(block_view)
        for tx_edit_part in block_edit_part.txs_edit_parts:
            tx_view = TransactionView()
            self.view_manager.txs_views.append(tx_view)
            block_view.txs_views.append(tx_view)
            tx_edit_part.view = tx_view
            for u_edit_part in tx_edit_part.outs_edit_parts:
                u_view = UtxoView()
                self.view_manager.us_views.append(u_view)
                u_view.tx_view = tx_view
                u_edit_part.view = u_view
                tx_view.outs_views.append(u_view)
        return block_edit_part.view


        
    def changeTxDisplayMode(self):
        if self.txDisplayMode == 0:
            count = 0
            delta = 2*math.pi / 12
            radius_tx_display = 4
            for b_ep in self.blockchain_edit_part.blocks_edit_parts:
                for t_ep in b_ep.txs_edit_parts:
                    t_ep.view.x = t_ep.view.x + radius_tx_display * math.cos(count*delta)
                    t_ep.view.y = t_ep.view.y + radius_tx_display * (1+math.sin(count*delta))
                    count +=1
                    t_ep.view.updateBox()
            self.txDisplayMode = 1
        else:
            for b_ep in self.blockchain_edit_part.blocks_edit_parts:
                for i,t_ep in enumerate(b_ep.txs_edit_parts):
                    t_ep.view.setPos(*b_ep.view.getPosForIndex(i))
                    t_ep.view.updateBox()
                    
        for b_ep in self.blockchain_edit_part.blocks_edit_parts:
            for t_ep in b_ep.txs_edit_parts:
                t_ep.view.updateLinkRenders()

    def Print(self):
        print(f"rx_validated_tx_board_edit_part : {len(self.rx_validated_tx_board_edit_part.rxs_edit_parts)}")
        print(f"rx_in_new_block_board_edit_part : {len(self.rx_in_new_block_board_edit_part.rxs_edit_parts)}")
        print(f"living_board_edit_part : {len(self.living_board_edit_part.rxs_edit_parts)}")
        print(f"limbo_edit_part : {len(self.limbo_edit_part.rxs_edit_parts)}")
        print(f"cementery_edit_part : {len(self.cementery_edit_part.rxs_edit_parts)}")


####################################################
# OBJECTS
####################################################

class BlockEditPart():
    # Block
    def __init__(self, scene_edit_part, model):
        self.model = model
        self.scene_edit_part = scene_edit_part
        self.view = BlockView()
        self.model.listeners.append(self)
        self.prev_edit_part = None
        self.txs_edit_parts = []
    def model_changed(self):
        None
class TransactionEditPart():
    # Transaction
    def addNewTransactionToQueue(scene_edit_part, ins_indexes, count_outs):
        queue_edit_part = scene_edit_part.transaction_queue_edit_part
        queue_model = queue_edit_part.model

        if queue_model.state != TransactionQueue.States.Ready:
            print("Transaction already being added or being loaded to validator")
            return

        tx = Transaction()
        tx_edit_part = TransactionEditPart(scene_edit_part, tx)
        tx_view = TransactionView()
        scene_edit_part.view_manager.txs_views.append(tx_view)
        tx_edit_part.view = tx_view
        for u in range(count_outs):
            u = Utxo()
            tx.outs.append(u)
            u.tx_of_born = tx

            u_edit_part = UtxoEditPart(scene_edit_part, u)
            tx_edit_part.outs_edit_parts.append(u_edit_part)
            u_edit_part.tx_of_born_edit_part = tx_edit_part

            u_view = UtxoView()
            u_view.visible=False
            scene_edit_part.view_manager.us_views.append(u_view)
            u_view.tx_view = tx_view
            tx_view.outs_views.append(u_view)

        queue_edit_part.txs_edit_parts.append(tx_edit_part)

        queue_model.txs.append(tx)

        queue_view = queue_edit_part.view
        queue_view.txs_views.append(tx_view)

        for in_i in ins_indexes:
            found = False
            for living_rx_ep in scene_edit_part.living_board_edit_part.rxs_edit_parts:
                if living_rx_ep.model.u.index == in_i:
                    tx_edit_part.ins_edit_part.append(living_rx_ep.u_edit_part)
                    tx.ins.append(living_rx_ep.model.u)
                    found = True
                    break
            if not found:
                found = False
                for dead_rx_ep in scene_edit_part.cementery_edit_part.rxs_edit_parts:
                    if dead_rx_ep.model.u.index == in_i:
                        tx_edit_part.ins_edit_part.append(dead_rx_ep.u_edit_part)
                        tx.ins.append(dead_rx_ep.model.u)
                        found = True
                        break
            if not found:
                tx_edit_part.ins_edit_part.append(UtxoEditPart.Dummy)

        queue_edit_part.model.state = TransactionQueue.States.Loading

        queue_model.state = TransactionQueue.States.Loading
        scene_edit_part.animator.loadAnimation(
            tx_view, 
            duration=scene_edit_part.configs['times']['enter_tx_queue'],
            pos0=queue_view.getPosForIndex(len(queue_view.txs_views)+1), 
            pos1=queue_view.getPosForIndex(len(queue_view.txs_views)-1),
            after=[lambda:tx_edit_part.afterAddNewTransaction()]
        )

    def afterAddNewTransaction(self):
        queue_model = self.scene_edit_part.transaction_queue_edit_part.model
        queue_model.state = TransactionQueue.States.Ready

    def initInterTxLinks(self):
        for out_ep in self.outs_edit_parts:
            if out_ep.tx_of_death_edit_part:
                self.view.addInterTxLink(out_ep.tx_of_death_edit_part.view)
                self.view.visibleLinks = True
                self.view.updateLinkRenders()

    def __init__(self, scene_edit_part, model):
        self.model = model
        self.scene_edit_part = scene_edit_part
        self.view = TransactionView()
        self.model.listeners.append(self)
        self.tx_holder_edit_part=[]
        self.ins_edit_part = []
        self.outs_edit_parts = []
    def model_changed(self):
        None
class UtxoEditPart():
    # Utxo
    Dummy=None
    settingDummy=False
    def __init__(self, scene_edit_part, model, isDummy=False):
        if  UtxoEditPart.Dummy == None and not UtxoEditPart.settingDummy:
            UtxoEditPart.settingDummy = True
            UtxoEditPart.Dummy = UtxoEditPart(None, None, isDummy=True)
            UtxoEditPart.Dummy.rx_edit_part = ReflectionEditPart(None,None)
            UtxoEditPart.Dummy.rx_edit_part.u_edit_part = UtxoEditPart.Dummy
            a = UtxoEditPart.Dummy.rx_edit_part.view
            (a.x,a.y,a.z)=(0,0,0)
        self.model = model
        self.scene_edit_part = scene_edit_part
        self.view = UtxoView()
        if self.model:
            self.model.listeners.append(self)
        self.rx_edit_part = None
        self.tx_of_born_edit_part = []
        self.tx_of_death_edit_part = []
    def model_changed(self):
        None
class ReflectionEditPart():
    # Reflection
    def __init__(self, scene_edit_part, model):
        self.model = model
        self.scene_edit_part = scene_edit_part
        self.view = ReflectionView(self)
        if self.model:
            self.model.listeners.append(self)
        self.u_edit_part = None
    def model_changed(self):
        None

####################################################
# BOARDS
####################################################
####################
# TX FLOW

class TransactionQueueEditPart():
    # TransactionQueueEditPart
    def __init__(self, scene_edit_part, model, view_manager):
        self.model = model
        self.scene_edit_part = scene_edit_part
        self.view = view_manager.transaction_queue_view
        self.model.listeners.append(self)
        self.txs_edit_parts = []
    def initTxViews(self):
        None
    def model_changed(self):
        None
class ValidatorEditPart():
    # ValidatorEditPart
    def __init__(self, scene_edit_part, model, view_manager):
        self.model = model
        self.model.listeners.append(self)
        self.scene_edit_part = scene_edit_part
        self.view = view_manager.validator_view
        self.model.listeners.append(self)
        self.txs_edit_parts = []

    def loadNextTransaction(self):
        queue_model = self.scene_edit_part.transaction_queue_edit_part.model
        validator_model = self.scene_edit_part.model.validator

        if validator_model.state != Validator.States.EmptyState and queue_model.state != TransactionQueue.States.Ready:
            print("Not Ready to Load")
            return
        if len(self.scene_edit_part.transaction_queue_edit_part.view.txs_views)==0:
            print("Empty Queue")
            return


        validator_view = self.view
        queue_view = self.scene_edit_part.transaction_queue_edit_part.view
        tx_view = queue_view.txs_views.pop(0)
        self.txs_edit_parts = [self.scene_edit_part.transaction_queue_edit_part.txs_edit_parts.pop(0)]

        validator_model.state = Validator.States.LoadingTransactionState
        queue_model.state = TransactionQueue.States.SendingToValidator

        self.scene_edit_part.animator.loadAnimation(
            tx_view,  
            duration=self.scene_edit_part.configs['times']['queue_to_validator'],
            pos0=queue_view.getPosForIndex(0),
            pos1=validator_view.getPosForTx(),
            after=[lambda:self.afterAnimationTransactionLoaded()]
        )
        for i, tx_view in enumerate(queue_view.txs_views):
            self.scene_edit_part.animator.loadAnimation(
                tx_view, 
                duration=self.scene_edit_part.configs['times']['down_one_level_in_queue'],
                pos0=queue_view.getPosForIndex(i+1),
                pos1=queue_view.getPosForIndex(i) 
            )

    def afterAnimationTransactionLoaded(self):
        queue_model = self.scene_edit_part.transaction_queue_edit_part.model
        queue_model.state = TransactionQueue.States.Ready
        self.model.finishLoadNextTransaction()

    def createLinks(self):
        for i,u_ep in enumerate(self.txs_edit_parts[0].outs_edit_parts):
            rx_ep = ReflectionEditPart(self.scene_edit_part,u_ep.model.rx)
            rx_v = ReflectionView(rx_ep)
            rx_ep.view = rx_v
            self.scene_edit_part.view_manager.rxs_views.append(rx_v)
            rx_ep.u_edit_part = u_ep
            u_ep.rx_edit_part = rx_ep
            self.scene_edit_part.rx_validated_tx_board_edit_part.rxs_edit_parts.append(rx_ep)
            rx_ep.view.setPos(*self.scene_edit_part.rx_validated_tx_board_edit_part.view.getPosForIndex(i))
            rx_ep.view.visible = True
            self.txs_edit_parts[0].view.addOutLink(_to=rx_v)

        for i, u_ep in enumerate(self.txs_edit_parts[0].ins_edit_part):
            self.txs_edit_parts[0].view.addInLink(u_ep.rx_edit_part.view)
        self.txs_edit_parts[0].view.visibleLinks = False

    def validateTransaction(self):
        if self.model.state != Validator.States.LoadedNonTestedState:
            print("Transaction already validated or not loaded")
            return

        a = lambda:self.afterValidation()
        self.createLinks()
        self.scene_edit_part.animator.startValidationAnimation(self, self.txs_edit_parts[0], self.scene_edit_part.configs['times']['validate'], [a])

    def afterValidation(self):
        self.model.validateTransaction()
        if self.model.state == Validator.States.LoadedValidTxState:
            self.txs_edit_parts[0].view.visibleLinks=True
            for u_ep in self.txs_edit_parts[0].ins_edit_part:
                rx_ep = u_ep.rx_edit_part
                rx_ep.view.setAlive(False)
            self.view.setValidTx(True)
        else:
            self.view.setValidTx(False)
            self.txs_edit_parts[0].view.setValidTx(False)
            for u_ep in self.txs_edit_parts[0].outs_edit_parts:
                rx_ep = u_ep.rx_edit_part
                rx_ep.view.setAlive(False)


    def dispatch(self):
        if self.model.state not in Validator.ValidatedStates:
            print("Transaction not loaded or not validated")
            return

        self.txs_edit_parts[0].view.animateLinks(True)
        tx_view = self.txs_edit_parts[0].view
        tx_ep = self.txs_edit_parts[0]
        if self.model.state == Validator.States.LoadedValidTxState:
            prep_view = self.scene_edit_part.preparing_block_edit_part.view
            self.scene_edit_part.animator.loadAnimation(
                tx_view,
                duration=self.scene_edit_part.configs['times']['from_validator_to_preparing_block'],
                pos0=self.view.getPosForTx(), 
                pos1=prep_view.getPosForIndex(len(self.scene_edit_part.preparing_block_edit_part.block_edit_part.txs_edit_parts)),
                after=[lambda:self.afterDispatch(tx_ep,False)]
            )
            c = len(self.scene_edit_part.rx_in_new_block_board_edit_part.rxs_edit_parts)
            for i, u_edit_part in enumerate(self.txs_edit_parts[0].outs_edit_parts):
                rx_ep = u_edit_part.rx_edit_part
                newPos = self.scene_edit_part.rx_in_new_block_board_edit_part.view.getPosForIndex(c+i)
                self.scene_edit_part.animator.loadAnimation(
                    rx_ep.view, 
                    duration=self.scene_edit_part.configs['times']['from_validator_to_preparing_block'],
                    pos0=(rx_ep.view.x, rx_ep.view.y, rx_ep.view.z),
                    pos1=newPos
                )
        else:
            self.scene_edit_part.animator.loadAnimation(
                tx_view,
                duration=self.scene_edit_part.configs['times']['from_validator_to_preparing_block'],
                pos0=self.view.getPosForTx(), 
                pos1=self.scene_edit_part.trash_edit_part.view.getPos(),
                after=[lambda:self.afterDispatch(tx_ep,True)]
            )
            for i, u_edit_part in enumerate(self.txs_edit_parts[0].outs_edit_parts):
                rx_ep = u_edit_part.rx_edit_part
                self.scene_edit_part.animator.loadAnimation(
                    rx_ep.view, 
                    duration=self.scene_edit_part.configs['times']['from_validator_to_preparing_block'],
                    pos0=(rx_ep.view.x, rx_ep.view.y, rx_ep.view.z),
                    pos1=self.scene_edit_part.trash_edit_part.view.getPos()
                )


    def afterDispatch(self,tx_ep, sent_to_trash):
        self.model.dispatch()
        tx_ep.view.animateLinks(False)
        tx_ep.view.updateLinkRenders()
        [u_ep.rx_edit_part.view.updateDisplays() for u_ep in tx_ep.outs_edit_parts]
        self.scene_edit_part.rx_in_new_block_board_edit_part.rxs_edit_parts += self.scene_edit_part.rx_validated_tx_board_edit_part.rxs_edit_parts
        self.scene_edit_part.rx_validated_tx_board_edit_part.rxs_edit_parts = []
        if sent_to_trash:
            self.scene_edit_part.view_manager.txs_views.remove(tx_ep.view)
            for u_ep in tx_ep.outs_edit_parts:
                self.scene_edit_part.view_manager.rxs_views.remove(u_ep.rx_edit_part.view)
        else:
            self.scene_edit_part.preparing_block_edit_part.block_edit_part.txs_edit_parts.append(tx_ep)
            for u_ep in tx_ep.outs_edit_parts:
                self.scene_edit_part.rx_in_new_block_board_edit_part.rxs_edit_parts.append(u_ep)

    def model_changed(self, event):
        None
        # if event == Validator.DISPATCH_EVENT:
        #     self.scene_edit_part.preparing_block_edit_part.block_edit_part.txs_edit_parts.append(self.txs_edit_parts.pop(0))
class TrashEditPart():
    # Trash
    def __init__(self, scene_edit_part, model, view_manager):
        self.model = model
        self.scene_edit_part = scene_edit_part
        self.view = view_manager.trash_view
        self.model.listeners.append(self)
        self.txs_edit_parts = []
    def model_changed(self):
        None

####################
# BLOCK FLOW
class PreparingBlockEditPart():
    # PreparingBlockEditPart
    def __init__(self, scene_edit_part, model, view_manager):
        self.model = model
        self.scene_edit_part = scene_edit_part
        self.view = view_manager.preparing_block_view
        self.model.listeners.append(self)
        self.block_edit_part = None

    def loadBlock(self):
        if self.model.state != PreparingBlock.States.ReadyToIncludeTransactions:
            print("PreparingBlock not ready to include Transactions")
            return
        self.model.state = PreparingBlock.States.LoadingBlockToChain
        self.scene_edit_part.animator.startBlockToBlockchainAnimation(self.scene_edit_part, after=[lambda:self.afterLoadBlock()])


    def afterLoadBlock(self):
        self.model.loadBlock()
        self.scene_edit_part.living_board_edit_part.model.update()
        self.scene_edit_part.limbo_edit_part.model.update()

        self.scene_edit_part.rx_in_new_block_board_edit_part.rxs_edit_parts = []

        self.view.block_view = self.scene_edit_part.create_block_view(self.block_edit_part)
        self.updateChildrenPositions()

        self.scene_edit_part.Print()

    def updateChildrenPositions(self):
        self.block_edit_part.view.setPos(*self.view.getBlockPosition())
        
    def model_changed(self):
        None
class BlockchainEditPart():
    # Blockchain
    def __init__(self, scene_edit_part, model, view_manager):
        self.model = model
        self.scene_edit_part = scene_edit_part
        self.view = view_manager.blockchain_view
        self.model.listeners.append(self)
        self.blocks_edit_parts = []
    def model_changed(self):
        None
    def updateChildrenPositions(self):
        for i,ep in enumerate(self.blocks_edit_parts):
            ep.view.setPos(*self.view.getPosForIndex(i))
            ep.view.updateChildrenPositions()
        for i,ep in enumerate(self.blocks_edit_parts):
            ep.view.updateBox()

####################
# RX FLOW
class RxValidatedTxBoardEditPart():
    # UtxosValidatedTxBoard
    def __init__(self, scene_edit_part, model, view_manager):
        self.model = model
        self.scene_edit_part = scene_edit_part
        self.view = view_manager.rx_validated_tx_board_view
        self.model.listeners.append(self)
        self.rxs_edit_parts = []
    def model_changed(self):
        None
class RxInNewBlockBoardEditPart():
    # UtxosInNewBlockBoard
    def __init__(self, scene_edit_part, model, view_manager):
        self.model = model
        self.scene_edit_part = scene_edit_part
        self.view = view_manager.rx_in_new_block_board_view
        self.model.listeners.append(self)
        self.rxs_edit_parts = []
    def model_changed(self):
        None
class LivingBoardEditPart():
    # LivingBoard
    def __init__(self, scene_edit_part, model, view_manager):
        self.model = model
        self.scene_edit_part = scene_edit_part
        self.view = view_manager.living_board_view
        self.model.listeners.append(self)
        self.rxs_edit_parts = []
    def model_changed(self):
        None
    def updateChildrenPositions(self):
        for i,rx_ep in enumerate(self.rxs_edit_parts):
            rx_ep.view.setPos(*self.view.getPosForIndex(i))
            rx_ep.view.visible = True
            rx_ep.view.updateBox()

class LimboEditPart():
    # Limbo
    def __init__(self, scene_edit_part, model, view_manager):
        self.model = model
        self.scene_edit_part = scene_edit_part
        self.view = view_manager.limbo_view
        self.model.listeners.append(self)
        self.rxs_edit_parts = []
    def model_changed(self):
        None
class CementeryEditPart():
    # Cementery
    def __init__(self, scene_edit_part, model, view_manager):
        self.model = model
        self.scene_edit_part = scene_edit_part
        self.view = view_manager.cementery_view
        self.model.listeners.append(self)
        self.rxs_edit_parts = []
    def model_changed(self):
        None



