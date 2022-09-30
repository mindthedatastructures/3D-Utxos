
from graphic_primitives.box import Box
from graphic_primitives.validator_box import ValidatorBox
from views.other_views import AnimatedLink
from graphic_primitives.link import Link
from graphic_primitives.number_view import NumberView

from graphic_primitives.letter_view import DisplayView

####################################################
# OBJECTS
####################################################

class BlockView():
    # Block
    w = 3
    h = 0.5
    d = 3

    def __init__(self):
        self.txs_views = []
        self.x = 0
        self.y = 0
        self.z = 0
        self.prev_block_view=None
        self.box = Box(self.x, self.y, self.z, BlockView.w, BlockView.h, BlockView.d, color='blue')
        self.link = Link(radius=0.1, color='blue')

    def updateBox(self):
        self.box.updateVertices(self.x, self.y, self.z, BlockView.w, BlockView.h, BlockView.d)
        if self.prev_block_view != None:
            self.link.updateVertices(
                self.x+BlockView.w/2,
                self.y+BlockView.h/2,
                self.z+BlockView.d/2,
                self.prev_block_view.x+BlockView.w/2,
                self.prev_block_view.y+BlockView.h/2,
                self.prev_block_view.z+BlockView.d/2,
                )

    def getPosForIndex(self,i):
        return (self.x + (BlockView.w - TransactionView.w)/2, self.y + (i+1)*(TransactionView.h),self.z + (BlockView.d - TransactionView.d)/2)

    def setPos(self,x,y,z):
        (self.x, self.y, self.z) = (x,y,z)
        self.updateBox()

    def updateChildrenPositions(self):
        x = self.x + (BlockView.w - TransactionView.w)/2
        z = self.z + (BlockView.d - TransactionView.d)/2
        for i,v in enumerate(self.txs_views):
            (v.x,v.y,v.z) = (x, self.y + (i+1)*(TransactionView.h),z)
            v.updateBox()

    def render(self):
        self.box.render()
        self.link.render()

    def renderS(self):
        self.box.renderS()
        self.link.renderS()

    def renderL(self):
        self.box.renderL()
        self.link.renderL()

class TransactionView():
    # Transaction
    w = 0.5
    h = 0.5
    d = 0.5
    def __init__(self):
        self.outs_views = []
        self.block_view=None
        self.x = 0
        self.y = 0
        self.z = 0
        self.box = Box(self.x, self.y, self.z, TransactionView.w, TransactionView.h, TransactionView.d, 'yellow')
        self.visibleLinks = False
        self.interTxLinks = []
        self.inLinks = []
        self.outLinks = []

    def setPos(self, o):
        self.setPos(*o)
    def setPos(self, x,y,z):
        (self.x,self.y,self.z) = (x,y,z)

    def addInterTxLink(self, _to):
        l = self.createOneLink(_to, 'red')
        self.interTxLinks.append(l)


    def addInLink(self, _to):
        l = self.createOneLink(_to, 'red')
        self.inLinks.append(l)

    def addOutLink(self, _to):
        l = self.createOneLink(_to, 'green')
        self.outLinks.append(l)

    def createOneLink(self, _to, color):
        l = AnimatedLink(self, _to, False, radius=0.01, color=color)
        x0 = self.x + self.w/2
        y0 = self.y + self.h/2
        z0 = self.z + self.d/2
        x1 = _to.x + _to.w/2
        y1 = _to.y + _to.h/2
        z1 = _to.z + _to.d/2
        print((x0,y0,z0,x1,y1,z1))
        l.updateVertices(x0,y0,z0,x1,y1,z1)
        return l

    def animateLinks(self,value):
        for l in self.inLinks+self.outLinks:
            l.animate=value

    def setValidTx(self, isValid):
        if isValid:
            self.box.setColor('yellow')
            self.box.white_borders = False
        else:
            self.box.setColor('black')
            self.box.white_borders = True

    def updateLinkRenders(self):
        for l in self.inLinks + self.outLinks + self.interTxLinks:
            l.updateRender()

    def updateBox(self):
        self.box.updateVertices(self.x, self.y, self.z, TransactionView.w, TransactionView.h, TransactionView.d)

    def render(self):
        self.box.render()
        if self.visibleLinks:
            for l in self.inLinks + self.outLinks + self.interTxLinks:
                l.render()

    def renderS(self):
        self.box.renderS()
        if self.visibleLinks:
            for l in self.inLinks + self.outLinks + self.interTxLinks:
                l.renderS()

    def renderL(self):
        self.box.renderL()
        if self.visibleLinks:
            for l in self.inLinks + self.outLinks + self.interTxLinks:
                l.renderL()


class UtxoView():
    # Utxo
    w = 0.5
    h = 0.5
    d = 0.5
    def __init__(self):
        self.tx_view = None
        self.x = 0
        self.y = 0
        self.z = 0
        self.visible = True
        self.box = Box(self.x, self.y, self.z, UtxoView.w, UtxoView.h, UtxoView.d, 'green',False)
        self.setAlive(True)

    def updateBox(self):
        self.box.updateVertices(self.x, self.y, self.z, UtxoView.w, UtxoView.h, UtxoView.d)

    def setAlive(self,isAlive):
        self.isAlive = True
        color = 'Green' if self.isAlive else 'Red'
        self.box.setColor(color)
        
    def render(self):
        self.box.render()

    def renderS(self):
        self.box.renderS()

    def renderL(self):
        self.box.renderL()

class ReflectionView():
    # Reflection
    w = 0.7
    h = 0.7
    d = 0.1

    def __init__(self, rx_ep):
        self.x = 0
        self.y = 0
        self.z = 0
        self.w = ReflectionView.w
        self.h = ReflectionView.h
        self.d = ReflectionView.d

        self.rx_ep = rx_ep

        self.visible = False
        self.box = Box(self.x, self.y, self.z, ReflectionView.w, ReflectionView.h, ReflectionView.d, 'green')

        self.margin_digit = 1/17
        self.size_digit = (self.w-2*self.margin_digit)/3

        self.n = [NumberView(self.x+self.margin_digit+i*self.size_digit, 0, self.z+self.d+0.01,self.size_digit) for i in range(3)]
        [n.setY(self.y + ((self.h - n.h)/2)) for n in self.n]

        try:
            v = self.rx_ep.model.u.index
            [n.setNumber(int(v/10**(2-i)) %10) for i,n in enumerate(self.n)]
        except:
            [n.setNumber('-') for n in self.n]
        self.updateDisplays()

        self.setAlive(True)

    def setPos(self, o):
        self.setPos(*o)

    def setPos(self, x,y,z):
        (self.x,self.y,self.z) = (x,y,z)
        self.updateBox()
        self.updateDisplays()

    def updateDisplays(self):
        [n.setPos(self.x+self.margin_digit+i*self.size_digit, self.y + ((self.h - n.h)/2), self.z+self.d+0.01) for i,n in enumerate(self.n)]
        
    def setAlive(self,isAlive):
        self.isAlive = isAlive
        color = 'Green' if self.isAlive else 'Red'
        self.box.setColor(color)

    def updateBox(self):
        self.box.updateVertices(self.x, self.y, self.z, ReflectionView.w, ReflectionView.h, ReflectionView.d)

    def render(self):
        if self.visible:
            self.box.render()
            [n.render() for n in self.n]

    def renderS(self):
        if self.visible:
            self.box.renderS()
            [n.renderS() for n in self.n]

    def renderL(self):
        if self.visible:
            self.box.renderL()
            [n.renderL() for n in self.n]



####################################################
# BOARDS
####################################################


class Board():
    def __init__(self, origin, dimensions, color):
        self.x0 = origin[0]
        self.y0 = origin[1]
        self.z0 = origin[2]
        self.w  = dimensions[0]
        self.h  = dimensions[1]
        self.d  = dimensions[2]

        self.utxos = []
        self.box = Box(self.x0,self.y0,self.z0,self.w,self.h,self.d, color=color)

    def render(self):
        self.box.render()
    def renderS(self):
        self.box.renderS()
    def renderL(self):
        self.box.renderL()



####################
# TX FLOW
class TransactionQueueView(Board):
    w = 1.5
    h = 0.2
    d = 1.5
    pad = 0.2

    # Reflection
    def __init__(self, validator_view):
        x = validator_view.origin[0]-2
        y = validator_view.origin[1]
        z = validator_view.origin[2]+(ValidatorView.border+TransactionView.d/2-TransactionQueueView.d/2)

        self.origin = (x,y,z)

        super(TransactionQueueView,self).__init__(self.origin, (TransactionQueueView.w,TransactionQueueView.h,TransactionQueueView.d),'red')
        self.txs_views = []
        self.x0 = self.origin[0] + (TransactionQueueView.w-TransactionView.w)/2
        self.z0 = self.origin[2] + (TransactionQueueView.d-TransactionView.d)/2

    # def updateChildrenPositions(self):
    #     for i, tx_view in enumerate(self.txs_views):
    #         (tx_view.x, tx_view.y, tx_view.z) = self.getPosForIndex(i)
    #         tx_view.updateBox()

    def getPosForIndex(self, i):
        y = self.origin[1] + TransactionQueueView.h + i * (TransactionView.h + TransactionQueueView.pad)
        return (self.x0, y, self.z0)



class ValidatorView():
    # (7,0,10)
    border=0.05
    def __init__(self, living_board_view):
        w1 = TransactionView.w
        h1 = TransactionView.h
        d1 = TransactionView.d
        self.w  = w1+2*ValidatorView.border
        self.h  = h1+2*ValidatorView.border
        self.d  = d1+2*ValidatorView.border

        x = living_board_view.origin[0] + (living_board_view.w - self.w)/2
        y = 0
        z = 10
        self.origin = (x,y,z)
        self.validator_box = ValidatorBox(x,y,z,self.w,self.h,self.d,w1,h1,d1, 'green')


    def setValidTx(self, isValidTx):
        self.isValidTx = isValidTx
        color = 'green' if isValidTx else 'red'
        self.validator_box.setColor(color)

    def setProcessingPhase(self, phase):
        if phase == 0:
            self.validator_box.setColor('white')
        elif phase == 1:
            self.validator_box.setColor('yellow')

    def getPosForTx(self):
        return (self.origin[0]+ValidatorView.border, self.origin[1]+ValidatorView.border, self.origin[2]+ValidatorView.border)

    def renderS(self):
        self.validator_box.renderS()
    def renderL(self):
        self.validator_box.renderL()


class TrashView():
    def __init__(self, preparingBlockView):
        self.x = preparingBlockView.x + PreparingBlockView.w + 2
        self.y = preparingBlockView.y
        self.z = preparingBlockView.z + (PreparingBlockView.d - TransactionView.d)/2

        self.box = Box(self.x,self.y,self.z,TransactionView.w,TransactionView.h,TransactionView.d, 'black', white_borders=True)

    def getPos(self):
        return (self.x,self.y,self.z)
    def render(self):
        self.box.render()

    def renderS(self):
        self.box.renderS()

    def renderL(self):
        self.box.renderL()


####################
# BLOCK FLOW
class PreparingBlockView(Board):
    # (7,0,10)
    w=5
    h=0.5
    d=5
    offsetx = 0.15 
    offsetz = 0.15 
    paddingx = 0.3
    paddingz = 0.3
    def __init__(self, rx_in_new_block_board_view):
        self.txPerLine = 3
        self.origin = (rx_in_new_block_board_view.origin[0], 0, rx_in_new_block_board_view.origin[2])
        self.x = self.origin[0]
        self.y = self.origin[1]
        self.z = self.origin[2]
        self.box = Box(self.x, self.y, self.z, PreparingBlockView.w,PreparingBlockView.h,PreparingBlockView.d, color='cyan', drawLines =True, drawSurfaces=True, white_borders=False)

    # def updateChildrenPositions(self):
    #     v = self.block_view
    #     v.x = self.origin[0] + (PreparingBlockView.w -BlockView.w)/2
    #     v.y = self.origin[1]
    #     v.z = self.origin[2] - PreparingBlockView.d -0.5
    #     v.updateBox()
    
    def getBlockPosition(self):
        return (
            self.origin[0] + (PreparingBlockView.w -BlockView.w)/2,
            self.origin[1],
            self.origin[2] - PreparingBlockView.d -0.5
        )
    def getPosForIndex(self,i):
        return (
            self.origin[0] + PreparingBlockView.offsetx + (i % self.txPerLine) * (TransactionView.w+PreparingBlockView.paddingx),
            self.origin[1] + self.h,
            self.origin[2] + self.d - PreparingBlockView.offsetz - TransactionView.d - int(i/self.txPerLine) * (TransactionView.d+PreparingBlockView.paddingz)
        )

    def render(self):
        super(PreparingBlockView,self).render()

class BlockchainView(Board):
    block_separation = 0.5
    # (6,0.5,-5),(0,0,-1)
    def __init__(self, living_board_view):
        # super(BlockchainView,self).__init__(origin, (1,1,1), 'yellow')
        self.x = living_board_view.origin[0] + (living_board_view.w - BlockView.w)/2
        self.y = 0
        self.z = - 5
        self.origin = (self.x,self.y,self.z)
        self.blocks_views = []
        self.living_board_view = living_board_view

    def getPosForIndex(self,i):
            return (self.origin[0],self.origin[1],self.origin[2]-i*(BlockView.d + BlockchainView.block_separation))

    def getTxPosForBlockIndexAndTxIndex(self, i_block, i_tx):
        tmp_block = BlockView()
        (tmp_block.x, tmp_block.y, tmp_block.z) = self.getPosForIndex(i_block)
        return tmp_block.getPosForIndex(i_tx)


    # def updateChildrenPositions(self):
    #     for i,v in enumerate(self.blocks_views):
    #         (v.x, v.y, v.z) = self.getPosForIndex(i)
    #         v.updateChildrenPositions()
    #     for i,v in enumerate(self.blocks_views):
    #         v.updateBox()
            
    def renderS(self):
        None
    def renderL(self):
        None
    def render(self):
        None

####################
# RX FLOW

class RxValidatedTxBoardView(Board):
    # RxValidatedTxBoard
    def __init__(self, livingBoardView, utxosPerLine):
        self.utxosPerLine = utxosPerLine
        utxosPerColumn = 3
        x = livingBoardView.origin[0] + livingBoardView.w + 0.5
        if utxosPerLine == 1:
            self.w =  2*LivingBoardView.offsetx + ReflectionView.w
        else:
            self.w = (utxosPerLine-1)*LivingBoardView.paddingx + 2*LivingBoardView.offsetx + utxosPerLine*ReflectionView.w

        if utxosPerColumn == 1:
            self.h =  2*LivingBoardView.offsety + ReflectionView.h
        else:
            self.h = (utxosPerColumn-1)*LivingBoardView.paddingy + 2*LivingBoardView.offsety + utxosPerColumn*ReflectionView.h

        d = LivingBoardView.d

        y = livingBoardView.origin[1] + livingBoardView.h - self.h
        z = livingBoardView.origin[2]

        self.origin=(x,y,z)
        super(RxValidatedTxBoardView,self).__init__((x,y,z), (self.w,self.h,d), 'white')

    def getPosForIndex(self, i):
        return (
                self.origin[0] + LivingBoardView.offsetx + (i % self.utxosPerLine) * (ReflectionView.w+LivingBoardView.paddingx),
                self.origin[1] + self.h - LivingBoardView.offsety - ReflectionView.h - int(i/self.utxosPerLine) * (ReflectionView.h+LivingBoardView.paddingy),
                self.origin[2] + self.d
            )

    def render(self):
        super(RxValidatedTxBoardView,self).render()

class RxInNewBlockBoardView(Board):
    # RxInNewBlockBoardView
    def __init__(self, livingBoardView,rxValidatedTxBoardView,utxosPerLine):
        self.utxosPerLine = utxosPerLine
        utxosPerColumn = 4
        x = rxValidatedTxBoardView.origin[0] + rxValidatedTxBoardView.w + 0.5
        if utxosPerLine == 1:
            self.w =  2*LivingBoardView.offsetx + ReflectionView.w
        else:
            self.w = (utxosPerLine-1)*LivingBoardView.paddingx + 2*LivingBoardView.offsetx + utxosPerLine*ReflectionView.w

        if utxosPerColumn == 1:
            self.h =  2*LivingBoardView.offsety + ReflectionView.h
        else:
            self.h = (utxosPerColumn-1)*LivingBoardView.paddingy + 2*LivingBoardView.offsety + utxosPerColumn*ReflectionView.h
        d = LivingBoardView.d

        y = rxValidatedTxBoardView.origin[1] + rxValidatedTxBoardView.h - self.h
        z = rxValidatedTxBoardView.origin[2]

        self.origin=(x,y,z)

        super(RxInNewBlockBoardView,self).__init__((x,y,z), (self.w,self.h, d), 'yellow')

    def getPosForIndex(self, i):
        return (
                self.origin[0] + LivingBoardView.offsetx + (i % self.utxosPerLine) * (ReflectionView.w+LivingBoardView.paddingx),
                self.origin[1] + self.h - LivingBoardView.offsety - ReflectionView.h - int(i/self.utxosPerLine) * (ReflectionView.h+LivingBoardView.paddingy),
                self.origin[2] + self.d
            )
    def render(self):
        super(RxInNewBlockBoardView,self).render()

class LivingBoardView(Board):
    offsetx = 0.15
    offsety = 0.15
    paddingx = 0.3
    paddingy = 0.3
    d=0.1
    def __init__(self, origin, utxosPerLine):
        utxosPerColumn = 12

        # LivingBoardView((5,0,0),(5, 10, 1),LivingBoard.UTXOS_PER_LINE)
        self.utxosPerLine = utxosPerLine
        self.origin = origin

        if utxosPerLine == 1:
            self.w =  2*LivingBoardView.offsetx + ReflectionView.w
        else:
            self.w = (utxosPerLine-1)*LivingBoardView.paddingx + 2*LivingBoardView.offsetx + utxosPerLine*ReflectionView.w

        if utxosPerColumn == 1:
            self.h =  2*LivingBoardView.offsety + ReflectionView.h
        else:
            self.h = (utxosPerColumn-1)*LivingBoardView.paddingy + 2*LivingBoardView.offsety + utxosPerColumn*ReflectionView.h


        super(LivingBoardView,self).__init__(origin, (self.w,self.h,LivingBoardView.d), (0,0.7,0.3))
        self.rxs_views = []
        
        letter_size = 0.5
        text="living utxos"
        margin = 0.1
        (x,y,z)=origin
        self.display = DisplayView(x, y+self.h+margin, z, text, letter_size)

    def render(self):
        super(LivingBoardView,self).render()
        self.display.render()

    def getPosForIndex(self, i):
        return (
                self.origin[0] + LivingBoardView.offsetx + (i % self.utxosPerLine) * (ReflectionView.w+LivingBoardView.paddingx),
                self.origin[1] + self.h - LivingBoardView.offsety - ReflectionView.w - int(i/self.utxosPerLine) * (ReflectionView.w+LivingBoardView.paddingy),
                self.origin[2] + LivingBoardView.d
            )

    # def updateChildrenPositions(self):
    #     for i,v in enumerate(self.rxs_views):
    #         v.setPos(self.getPosForIndex(i))
    #         v.visible = True
    #         v.updateBox()


class LimboView(Board):
    def __init__(self, livingBoardView, utxosPerLine):
        self.utxosPerLine = utxosPerLine
        utxosPerColumn = 8
        if utxosPerLine == 1:
            self.w =  2*LivingBoardView.offsetx + ReflectionView.w
        else:
            self.w = (utxosPerLine-1)*LivingBoardView.paddingx + 2*LivingBoardView.offsetx + utxosPerLine*ReflectionView.w

        if utxosPerColumn == 1:
            self.h =  2*LivingBoardView.offsety + ReflectionView.h
        else:
            self.h = (utxosPerColumn-1)*LivingBoardView.paddingy + 2*LivingBoardView.offsety + utxosPerColumn*ReflectionView.h
        x = livingBoardView.origin[0] - self.w - 0.5
        d = LivingBoardView.d

        y = livingBoardView.origin[1] + livingBoardView.h - self.h
        z = livingBoardView.origin[2]
        self.origin=(x,y,z)
        letter_size = 0.5

        self.box = Box(x,y,z,self.w,self.h,d, 'black', drawLines =True, drawSurfaces=False, white_borders=True)
    def render(self):
        self.box.render()
    def getPosForIndex(self, i):
        return (
                self.origin[0] + LivingBoardView.offsetx + (i % self.utxosPerLine) * (ReflectionView.w+LivingBoardView.paddingx),
                self.origin[1] + self.h - LivingBoardView.offsety - ReflectionView.w - int(i/self.utxosPerLine) * (ReflectionView.w+LivingBoardView.paddingy),
                self.origin[2] + LivingBoardView.d
            )


class CementeryView(Board):
    # (1,-3,-3)
    def __init__(self, limboView, utxosPerLine):
        self.utxosPerLine = utxosPerLine
        utxosPerColumn = 8
        if utxosPerLine == 1:
            self.w =  2*LivingBoardView.offsetx + ReflectionView.w
        else:
            self.w = (utxosPerLine-1)*LivingBoardView.paddingx + 2*LivingBoardView.offsetx + utxosPerLine*ReflectionView.w

        if utxosPerColumn == 1:
            self.h =  2*LivingBoardView.offsety + ReflectionView.h
        else:
            self.h = (utxosPerColumn-1)*LivingBoardView.paddingy + 2*LivingBoardView.offsety + utxosPerColumn*ReflectionView.h
        x = limboView.origin[0] - self.w - 0.5
        d = LivingBoardView.d

        y = limboView.origin[1] + limboView.h - self.h
        z = limboView.origin[2]
        self.origin=(x,y,z)


        letter_size = 0.5
        text="cementery"
        margin = 0.1
        self.display = DisplayView(x + self.w - letter_size*len(text), y+self.h+margin, z, text, letter_size)

        self.box = Box(x,y,z,self.w,self.h,d, 'black', drawLines =True, drawSurfaces=False, white_borders=True)
    def render(self):
        self.display.render()
        self.box.render()
    def getPosForIndex(self, i):
        return (
                self.origin[0] + LivingBoardView.offsetx + (self.utxosPerLine - 1 - (i % self.utxosPerLine)) * (ReflectionView.w+LivingBoardView.paddingx),
                self.origin[1] + self.h - LivingBoardView.offsety - ReflectionView.w - int(i/self.utxosPerLine) * (ReflectionView.w+LivingBoardView.paddingy),
                self.origin[2] + LivingBoardView.d
                )

