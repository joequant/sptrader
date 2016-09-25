# Adding other items
import strategy
import strategy.sample
import collections

dispatch = collections.OrderedDict([
    ('sample', strategy.sample.SampleStrategy)
    ])

