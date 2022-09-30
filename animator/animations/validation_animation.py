
from animator.IAnimation import IAnimation

class ValidationAnimation(IAnimation):

    def __init__(self, validator_ep, link_holder_ep, t0, duration,after=[]):
        self.validator_ep = validator_ep
        self.link_holder_ep = link_holder_ep
        self.t0 = t0
        self.after = after
        self.duration = duration
        self.hasEnded_v = False
        self.after = after
        self.dead_rxs_ep = []
        for u_ep in self.validator_ep.txs_edit_parts[0].ins_edit_part:
            if not u_ep.rx_edit_part.view.isAlive:
                self.dead_rxs_ep.append(u_ep.rx_edit_part)

    def animate(self, now):
        delta_t = (now-self.t0)/self.duration

        phase = int(delta_t*6)

        if delta_t >= 1:
            return
        if phase%2 == 0:
            self.validator_ep.view.setProcessingPhase(0)
            self.link_holder_ep.view.visibleLinks=True
            for u_ep in self.validator_ep.txs_edit_parts[0].ins_edit_part:
                rx_ep = u_ep.rx_edit_part
                if rx_ep not in self.dead_rxs_ep:
                    rx_ep.view.setAlive(False)
        else:
            self.validator_ep.view.setProcessingPhase(1)
            self.link_holder_ep.view.visibleLinks=False
            for u_ep in self.validator_ep.txs_edit_parts[0].ins_edit_part:
                rx_ep = u_ep.rx_edit_part
                if rx_ep not in self.dead_rxs_ep:
                    rx_ep.view.setAlive(True)

    def hasEnded(self, now):
        if self.hasEnded_v:
            return True

        self.hasEnded_v = self.t0 + self.duration < now
        return self.hasEnded_v

    def after_animation_listeners(self):
        for a in self.after:
            a()
