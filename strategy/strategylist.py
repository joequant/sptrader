# Adding other items
import strategy
import strategy.sample
import strategy.immediate
import strategy.hammer
import strategy.engulfing
import collections

dispatch = collections.OrderedDict([
    ('hammer', strategy.hammer.HammerStrategy),
    ('engulfing', strategy.engulfing.EngulfingStrategy),
    ('sample', strategy.sample.SampleStrategy),
    ('immediate', strategy.immediate.ImmediateStrategy),
    ])

