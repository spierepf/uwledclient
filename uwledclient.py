class SegmentBuilder:
    def __init__(self, maxseg, led_count, effects, palettes, callback):
        self.maxseg = maxseg
        self.led_count = led_count
        self.effects = effects
        self.palettes = palettes
        self.segments = []
        self.init_next_segment()
        self.callback = callback

    def init_next_segment(self):
        self.next_segment = {'start': (0 if len(self.segments) == 0 else self.segments[-1]['stop']),
                             'stop': self.led_count,
                             'col': [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                             'fx': self.effects['Solid']}

    def next(self):
        self.segments.append(self.next_segment)
        self.init_next_segment()
        return self

    def length(self, segment_length):
        self.next_segment['stop'] = self.next_segment['start'] + segment_length
        return self

    def fx(self, effect_name):
        self.next_segment['fx'] = effect_name if effect_name in ['~', '~-', 'r'] else self.effects[effect_name]
        return self

    def pal(self, palette_name):
        self.next_segment['pal'] = palette_name if palette_name in ['~', '~-', 'r'] else self.palettes[palette_name]
        return self

    def set(self, key, value):
        self.next_segment[key] = value
        return self

    def __getattr__(self, key):
        return lambda value: self.set(key, value)

    def done(self):
        while len(self.segments) < self.maxseg:
            self.segments.append({'id': len(self.segments), 'stop': 0})
        self.callback(self.segments)


try:
    from urllib.urequest import urlopen
    import ujson

    class WLEDNode:
        def __init__(self, base_url):
            self.base_url = base_url
            self.leds = self.api_read('info')['leds']
            self.effects = dict((v, k) for (k, v) in enumerate(self.api_read('effects')))
            self.palettes = dict((v, k) for (k, v) in enumerate(self.api_read('palettes')))

        def api_read(self, endpoint):
            socket = urlopen(self.base_url + '/json/' + endpoint)
            buf = socket.recv(4096)
            retval = ujson.loads(buf)
            socket.close()
            return retval

        def callback(self, segments):
            urlopen(self.base_url + '/json/state', ujson.dumps({'seg': segments})).close()

        def update(self):
            return SegmentBuilder(self.leds['maxseg'], self.leds['count'], self.effects, self.palettes, self.callback)
except ImportError:
    pass
