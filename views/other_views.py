from graphic_primitives.link import Link


class AnimatedLink():
    def __init__(self, _from, _to, animate, color='magenta', radius = 0.5, onlyLines =False):
        self._from = _from
        self._to = _to
        self.animate = animate
        self.link = Link(color, radius, onlyLines)

    def updateVertices(self,x0,y0,z0,x1,y1,z1):
        self.link.updateVertices(x0,y0,z0,x1,y1,z1)

    def setColor(self,color):
        self.link.setColor(color)

    def updateRender(self):
            self.updateVertices(
                self._from.x+self._from.w/2,
                self._from.y+self._from.h/2,
                self._from.z+self._from.d/2,
                self._to.x+self._to.w/2,
                self._to.y+self._to.h/2,
                self._to.z+self._to.d/2)

        
    def renderS(self):
        self.common_pre_render()
        self.link.renderS()

    def renderL(self):
        self.common_pre_render()
        self.link.renderL()
        
    def render(self):
        self.common_pre_render()
        self.link.render()

    def common_pre_render(self):
        if self.animate:
            # self.updateRender()
            self.updateVertices(
                self._from.x+self._from.w/2,
                self._from.y+self._from.h/2,
                self._from.z+self._from.d/2,
                self._to.x+self._to.w/2,
                self._to.y+self._to.h/2,
                self._to.z+self._to.d/2)


