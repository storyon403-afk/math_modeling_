class UserBehavior:

    def __init__(
        self,
        brightness: float,
        cpu: float,
        gpu: float,
        network_traffic: float,
        signal_quality: float,
        gps: int,
        background: float
    ):

        self.brightness = brightness
        self.cpu = cpu
        self.gpu = gpu
        self.network_traffic = network_traffic
        self.signal_quality = signal_quality
        self.gps = gps
        self.background = background