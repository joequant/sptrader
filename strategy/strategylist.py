# Adding other items
import strategy
import strategy.sample

_list = ['sample']
dispatch = {
    'sample': strategy.sample.SampleStrategy
}
