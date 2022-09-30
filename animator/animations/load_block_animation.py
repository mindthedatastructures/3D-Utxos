
from animator.IAnimation import IAnimation

class LoadBlockAnimation(IAnimation):

    def __init__(self, animator, t0, configs, scene_edit_part, after):
        self.animator = animator
        self.t0 = t0
        self.configs = configs
        self.scene_ep = scene_edit_part
        self.preparing_block_ep = scene_edit_part.preparing_block_edit_part
        self.block_ep = self.preparing_block_ep.block_edit_part
        self.blockchain_ep = scene_edit_part.blockchain_edit_part
        self.after = after
        self.dur_phases = []

        self.loadPhase1()

        self.hasEnded_v = False


    def loadPhase1(self):
        d = self.configs['times']['add_block_to_chain']['camera_move_to_blockchain']
        self.animator.startCameraAnimation(d, 'BlockChainView1', [lambda:self.loadPhase2()])

    def loadPhase2(self):
        d = self.configs['times']['add_block_to_chain']['move_tx_from_prep_to_block']
        for i, tx_ep in enumerate(self.block_ep.txs_edit_parts):
            if i == 0:
                a = [lambda:self.loadPhase3()]
            else:
                a = []
            tx_ep.view.animateLinks(True)
            self.animator.loadAnimation(
                tx_ep.view,
                duration = d,
                pos0 = (tx_ep.view.x,tx_ep.view.y,tx_ep.view.z),
                pos1 = self.block_ep.view.getPosForIndex(i),
                after = a
                )
    def loadPhase3(self):
        d = self.configs['times']['add_block_to_chain']['wait_after_move_tx_from_prep_to_block']
        self.animator.loadWaitAnimation(
            duration=d,
            after=[lambda:self.loadPhase4()]
            )
    def loadPhase4(self):
        for i, block_ep in enumerate(self.blockchain_ep.blocks_edit_parts):
            d = self.configs['times']['add_block_to_chain']['leave_space_for_new_block']
            if i == 0:
                a = [lambda:self.loadPhase5()]
            else:
                a = []
            for j, tx_ep in enumerate(block_ep.txs_edit_parts):
                self.animator.loadAnimation(
                    tx_ep.view,
                    duration = d,
                    pos0 = self.blockchain_ep.view.getTxPosForBlockIndexAndTxIndex(i, j),
                    pos1 = self.blockchain_ep.view.getTxPosForBlockIndexAndTxIndex(i+1, j),
                    after = []
                    )    
            
            self.animator.loadAnimation(
                block_ep.view,
                duration = d,
                pos0 = self.blockchain_ep.view.getPosForIndex(i),
                pos1 = self.blockchain_ep.view.getPosForIndex(i+1),
                after = a
                )
    def loadPhase5(self):
        block_ep = self.block_ep
        d = self.configs['times']['add_block_to_chain']['move_block_to_blockchain']
        self.animator.loadAnimation(
            block_ep.view,
            duration = d,
            pos0 = (block_ep.view.x, block_ep.view.y, block_ep.view.z),
            pos1 = self.blockchain_ep.view.getPosForIndex(0),
            after = [lambda:self.loadPhase6()]
            )
        for j, tx_ep in enumerate(block_ep.txs_edit_parts):
            self.animator.loadAnimation(
                tx_ep.view,
                duration = d,
                pos0 = (tx_ep.view.x, tx_ep.view.y, tx_ep.view.z),
                pos1 = self.blockchain_ep.view.getTxPosForBlockIndexAndTxIndex(0, j),
                after = []
                )    

    def loadPhase6(self):
        d = self.configs['times']['add_block_to_chain']['camera_move_to_limbo']
        for tx_ep in self.block_ep.txs_edit_parts:
            tx_ep.view.visibleLinks = False
        self.animator.startCameraAnimation(d, 'InitialCamera', [lambda:self.loadPhase7()])


    def loadPhase7(self):
        d = self.configs['times']['add_block_to_chain']['wait_after_camera_move_']
        self.animator.loadWaitAnimation(
            duration=d,
            after=[lambda:self.loadPhase8()]
            )

    def loadPhase8(self):
        d = self.configs['times']['add_block_to_chain']['send_old_rx_to_limbo']
        total_to_move = 0
        for tx_ep in self.block_ep.txs_edit_parts:
            total_to_move += len(tx_ep.ins_edit_part)
        i=0
        for tx_ep in self.block_ep.txs_edit_parts:

            for u_ep in tx_ep.ins_edit_part:
                if i == 0:
                    a = [lambda:self.loadPhase9()]
                else:
                    a = []
                self.animator.loadAnimation(
                    u_ep.rx_edit_part.view,
                    duration = d,
                    pos0 = (u_ep.rx_edit_part.view.x, u_ep.rx_edit_part.view.y, u_ep.rx_edit_part.view.z),
                    pos1 = self.scene_ep.limbo_edit_part.view.getPosForIndex(i),
                    after = a
                    )
                i+=1


    def loadPhase9(self):
        d = self.configs['times']['add_block_to_chain']['relocate_new_alive_rx']
        removed_rx = []
        for tx_ep in self.block_ep.txs_edit_parts:
            for u_ep in tx_ep.ins_edit_part:
                removed_rx.append(u_ep.rx_edit_part)
        i = 0
        for rx_ep in self.scene_ep.living_board_edit_part.rxs_edit_parts:
            if rx_ep not in removed_rx:
                if i == 0:
                    a = [lambda:self.loadPhase10()]
                else:
                    a = []
                self.animator.loadAnimation(
                    rx_ep.view,
                    duration = d,
                    pos0 = (rx_ep.view.x, rx_ep.view.y, rx_ep.view.z),
                    pos1 = self.scene_ep.living_board_edit_part.view.getPosForIndex(i),
                    after = a
                    )
                i+=1
        for tx_ep in self.block_ep.txs_edit_parts:
            for u_ep in tx_ep.outs_edit_parts:
                rx_ep = u_ep.rx_edit_part
                self.animator.loadAnimation(
                    rx_ep.view,
                    duration = d,
                    pos0 = (rx_ep.view.x, rx_ep.view.y, rx_ep.view.z),
                    pos1 = self.scene_ep.living_board_edit_part.view.getPosForIndex(i)
                    )
                i+=1
                self.scene_ep.living_board_edit_part.rxs_edit_parts.append(rx_ep)
        for r in removed_rx:
            self.scene_ep.limbo_edit_part.rxs_edit_parts.append(r)
            self.scene_ep.living_board_edit_part.rxs_edit_parts.remove(r)

    def loadPhase10(self):
        d = self.configs['times']['add_block_to_chain']['wait_after_relocate']
        self.animator.loadWaitAnimation(
            duration=d,
            after=[lambda:self.loadPhase11()]
            )


    def loadPhase11(self):
        d = self.configs['times']['add_block_to_chain']['send_old_rx_to_cementery']
        q = len(self.scene_ep.cementery_edit_part.rxs_edit_parts)
        for i,rx_ep in enumerate(self.scene_ep.limbo_edit_part.rxs_edit_parts):
            if i == 0:
                a = [lambda:self.loadPhase12()]
            else:
                a = []
            self.animator.loadAnimation(
                    rx_ep.view,
                    duration = d,
                    pos0 = (rx_ep.view.x, rx_ep.view.y, rx_ep.view.z),
                    pos1 = self.scene_ep.cementery_edit_part.view.getPosForIndex(q+i),
                    after=a
                    )
            self.scene_ep.cementery_edit_part.rxs_edit_parts.append(rx_ep)
        self.scene_ep.limbo_edit_part.rxs_edit_parts = []


    def loadPhase12(self):
        self.hasEnded_v = True



    def animate(self, now):
        None

    def hasEnded(self, now):
        return self.hasEnded_v

    def after_animation_listeners(self):
        for a in self.after:
            a()
