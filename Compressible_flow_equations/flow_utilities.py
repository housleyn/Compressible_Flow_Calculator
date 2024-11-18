
import math
class flow_utilities:
    def __init__(self, gamma):
        self.gamma = gamma

    def tt0(self, m):
        return math.pow((1.0 + (self.gamma - 1.0) / 2.0 * m * m), -1.0)

    def pp0(self, m):
        return math.pow((1.0 + (self.gamma - 1.0) / 2.0 * m * m), -self.gamma / (self.gamma - 1.0))

    def rr0(self, m):
        return math.pow((1.0 + (self.gamma - 1.0) / 2.0 * m * m), -1.0 / (self.gamma - 1.0))

    def tts(self, m):
        return self.tt0(m) * (self.gamma / 2.0 + 0.5)

    def pps(self, m):
        return self.pp0(m) * math.pow((self.gamma / 2.0 + 0.5), self.gamma / (self.gamma - 1.0))

    def rrs(self, m):
        return self.rr0(m) * math.pow((self.gamma / 2.0 + 0.5), 1.0 / (self.gamma - 1.0))

    def aas(self, m):
        return 1.0 / self.rrs(m) * math.sqrt(1.0 / self.tts(m)) / m

    def nu(self, m):
        n = math.sqrt((self.gamma + 1.0) / (self.gamma - 1.0)) * math.atan(math.sqrt((self.gamma - 1.0) / (self.gamma + 1.0) * (m * m - 1.0)))
        n -= math.atan(math.sqrt(m * m - 1.0))
        n *= 180.0 / math.pi
        return n

    def m2(self, m1):
        return math.sqrt((1.0 + 0.5 * (self.gamma - 1.0) * m1 * m1) / (self.gamma * m1 * m1 - 0.5 * (self.gamma - 1.0)))
