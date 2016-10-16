# Adding other items
import strategy
import strategy.sample
import strategy.immediate
import collections

dispatch = collections.OrderedDict([
    ('sample', strategy.sample.SampleStrategy),
    ('immediate', strategy.immediate.ImmediateStrategy)
    ])

