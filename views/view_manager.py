from views.views import *
from model.models import *

from graphic_primitives.clock import Clock
from views.views import LivingBoardView

from OpenGL.GL import *
from OpenGL.GLU import *

class ViewManager():
    def __init__(self):
        self.other_objects = []
        self.objects = []

        self.txs_views = []
        self.us_views = []
        self.rxs_views = []
        self.blocks_views = []

    def initBoardViewObjects(self):


        ####################################################
        # BOARDS
        ####################################################
        
        ####################
        # RX FLOW
        self.living_board_view = LivingBoardView((5,0,0),LivingBoard.UTXOS_PER_LINE)
        self.rx_validated_tx_board_view = RxValidatedTxBoardView(self.living_board_view, 2)
        self.rx_in_new_block_board_view = RxInNewBlockBoardView(self.living_board_view,self.rx_validated_tx_board_view,5)
        self.limbo_view = LimboView(self.living_board_view, 3)
        self.cementery_view = CementeryView(self.limbo_view, 50)

        ####################
        # BLOCK FLOW
        self.preparing_block_view = PreparingBlockView(self.rx_in_new_block_board_view)
        self.blockchain_view = BlockchainView(self.living_board_view)

        ####################
        # TX FLOW
        self.validator_view = ValidatorView(self.living_board_view)
        self.transaction_queue_view = TransactionQueueView(self.validator_view)
        self.trash_view = TrashView(self.preparing_block_view)

        self.boards = [self.transaction_queue_view, self.validator_view, self.trash_view, self.preparing_block_view, self.blockchain_view, self.rx_validated_tx_board_view, self.rx_in_new_block_board_view, self.living_board_view, self.limbo_view, self.cementery_view]
        
        self.initClock()



    def initClock(self):
        radius_clock = 2
        offsety = 0.5
        x_clock = self.living_board_view.origin[0]+(self.living_board_view.w-radius_clock)/2
        y_clock = self.living_board_view.origin[1]+self.living_board_view.h + offsety + radius_clock
        z_clock = self.living_board_view.origin[2]

        self.clock = Clock(x_clock, y_clock, z_clock, radius_clock)
        self.clock.setPercentage(67)


    def render_all(self):
        glBegin(GL_QUADS)
        self.renderS()
        glEnd()

        glBegin(GL_LINES)
        self.renderL()
        glEnd()

    def renderS(self):
        [o.renderS() for o in self.other_objects + self.boards + self.txs_views + self.us_views + self.rxs_views + self.blocks_views + [self.clock]]

    def renderL(self):
        [o.renderL() for o in self.other_objects + self.boards + self.txs_views + self.us_views + self.rxs_views + self.blocks_views + [self.clock]]


