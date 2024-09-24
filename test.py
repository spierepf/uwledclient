import os

import install

if 'unittest' not in os.listdir(install.libpath):
    import mip
    mip.install('unittest', target=install.libpath)

import unittest

from uwledclient import SegmentBuilder


class Callback:
    def __init__(self):
        self.segments = None

    def __call__(self, segments):
        self.segments = segments


class TestSegmentBuilder(unittest.TestCase):
    def test_segmentbuilder_invokes_callback_when_done(self):
        callback = Callback()
        SegmentBuilder(1, 1, {'Solid': 0}, {}, callback).done()
        assert callback.segments is not None

    def test_segmentbuilder_creates_maxseg_segments(self):
        for maxseg in [1, 2]:
            callback = Callback()
            SegmentBuilder(maxseg, 1, {'Solid': 0}, {}, callback).done()
            assert len(callback.segments) == maxseg
            for i in range(maxseg):
                assert callback.segments[i]['id'] == i
                assert callback.segments[i]['stop'] == 0

    def test_segmentbuilder_first_segment_starts_at_zero(self):
        callback = Callback()
        SegmentBuilder(1, 1, {'Solid': 0}, {}, callback).next().done()
        assert callback.segments[0]['start'] == 0

    def test_segmentbuilder_segment_defaults_to_using_all_leds(self):
        for led_count in [1, 2]:
            callback = Callback()
            SegmentBuilder(1, led_count, {'Solid': 0}, {}, callback).next().done()
            assert callback.segments[0]['stop'] == led_count

    def test_segmentbuilder_defaults_to_solid_black(self):
        for effect_id in range(2):
            callback = Callback()
            SegmentBuilder(1, 1, {'Solid': effect_id}, {}, callback).next().done()
            assert callback.segments[0]['fx'] == effect_id
            assert callback.segments[0]['col'] == [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    def test_segmentbuilder_length(self):
        for led_count in [5, 6]:
            for first_segment_length in [1, 2]:
                for second_segment_length in [1, 2]:
                    callback = Callback()
                    (SegmentBuilder(3, led_count, {'Solid': 0}, {}, callback)
                     .length(first_segment_length).next()
                     .length(second_segment_length).next()
                     .next().done())
                    assert callback.segments[0]['start'] == 0
                    assert callback.segments[0]['stop'] == first_segment_length
                    assert callback.segments[1]['start'] == first_segment_length
                    assert callback.segments[1]['stop'] == first_segment_length + second_segment_length
                    assert callback.segments[2]['start'] == first_segment_length + second_segment_length
                    assert callback.segments[2]['stop'] == led_count

    def test_segmentbuilder_set(self):
        callback = Callback()
        SegmentBuilder(1, 1, {'Solid': 0}, {}, callback).set('bogus', 1).next().done()
        assert callback.segments[0]['bogus'] == 1

    def test_segmentbuilder_dunder_get_attr(self):
        callback = Callback()
        SegmentBuilder(1, 1, {'Solid': 0}, {}, callback).bogus(1).next().done()
        assert callback.segments[0]['bogus'] == 1

    def test_segmentbuilder_fx_sets_effect_by_effect_id(self):
        callback = Callback()
        SegmentBuilder(1, 1, {'Solid': 0, 'Test Effect': 1}, {}, callback).fx('Test Effect').next().done()
        assert callback.segments[0]['fx'] == 1

    def test_segmentbuilder_fx_special_strings(self):
        for special_string in ['~', '~-', 'r']:
            callback = Callback()
            SegmentBuilder(1, 1, {'Solid': 0}, {}, callback).fx(special_string).next().done()
            assert callback.segments[0]['fx'] == special_string

    def test_segmentbuilder_pal_sets_palette_by_palette_id(self):
        callback = Callback()
        SegmentBuilder(1, 1, {'Solid': 0}, {'Test Palette': 1}, callback).pal('Test Palette').next().done()
        assert callback.segments[0]['pal'] == 1

    def test_segmentbuilder_pal_special_strings(self):
        for special_string in ['~', '~-', 'r']:
            callback = Callback()
            SegmentBuilder(1, 1, {'Solid': 0}, {}, callback).pal(special_string).next().done()
            assert callback.segments[0]['pal'] == special_string

if __name__ == "__main__":
    unittest.main()
