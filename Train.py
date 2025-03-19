import logging

logger = logging.getLogger(__name__)

class Train:
    def __init__(self, tid, name, traintype, delay, visible):
        self.tid = int(tid)
        self.name = name
        self.traintype = traintype
        self.delay = delay
        self.visible = visible

    def diff(self, newdelay):
        # old: +4 | new: +2 -> 2-4=-2
        # old: -3 | new: 0  -> 0-(-3)=3
        # old: +3 | new: -1 -> -1-3=-4
        diff = newdelay - self.delay
        self.delay = newdelay
        return diff

    def __hash__(self):
        return self.tid

    def __eq__(self, other):
        return isinstance(other, Train) and self.tid == other.tid

    def __repr__(self):
        return f'{self.tid}_{self.name}'
