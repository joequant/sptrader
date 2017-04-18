#!/usr/bin/python3

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import os
import sys
location = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(location, "..", "sptrader"))
sys.path.insert(0, os.path.join(location, ".."))
data_dir = os.path.join(location, "..", "data")

import argparse

import backtrader as bt
import sptrader
from spfeed import SharpPointCSVData
from spwriter import SharpPointWriter
import backtrader.feeds as btfeeds


def runstrat():
    args = parse_args()

    # Create a cerebro entity
    cerebro = bt.Cerebro(stdstats=False)

    # Add a strategy
    cerebro.addstrategy(bt.Strategy)

    # Load the Data
    datapath = args.dataname or '../../datas/ticksample.csv'

    if not os.path.isfile(datapath):
        datapath_new = os.path.join(data_dir, datapath)
        if os.path.isfile(datapath_new):
            datapath = datapath_new
        else:
            print('cannot find %s or %s' % (datapath, datapath_new))
            exit

    if args.outfile == '':
        outfile = sys.stdout
    else:
        outfile = open(args.outfile, 'w')

    data = SharpPointCSVData(
        dataname=datapath,
        timeframe=bt.TimeFrame.Ticks,
        gateway=None
    )

    # Handy dictionary for the argument timeframe conversion
    tframes = dict(
        ticks=bt.TimeFrame.Ticks,
        microseconds=bt.TimeFrame.MicroSeconds,
        seconds=bt.TimeFrame.Seconds,
        minutes=bt.TimeFrame.Minutes,
        daily=bt.TimeFrame.Days,
        weekly=bt.TimeFrame.Weeks,
        monthly=bt.TimeFrame.Months)

    # Resample the data
    data = cerebro.resampledata(data,
                                timeframe=tframes[args.timeframe],
                                compression=args.compression)

    # add a writer
    cerebro.addwriter(SharpPointWriter, csv=True,
                      out=outfile)

    # Run over everything
    cerebro.run()


def parse_args():
    parser = argparse.ArgumentParser(
        description='Resampling script down to tick data')

    parser.add_argument('dataname', default='',
                        help='File Data to Load')

    parser.add_argument('--timeframe', default='minutes', required=False,
                        choices=['ticks', 'microseconds', 'seconds',
                                 'minutes', 'daily', 'weekly', 'monthly'],
                        help='Timeframe to resample to')

    parser.add_argument('--compression', default=5, required=False, type=int,
                        help=('Compress n bars into 1'))

    parser.add_argument('--outfile', default='', required=False,
                        help='Output file')

    return parser.parse_args()


if __name__ == '__main__':
    runstrat()
