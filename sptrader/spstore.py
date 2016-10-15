#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# Copyright (C) 2015,2016 Daniel Rodriguez
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import collections
from datetime import datetime, timedelta
import time as _time
import json
import threading
import requests
import sseclient
import logging
import backtrader as bt
from backtrader.metabase import MetaParams
from backtrader.utils.py3 import queue, with_metaclass
from backtrader.utils import AutoDict
from backtrader.position import Position
from copy import copy

class MetaSingleton(MetaParams):
    '''Metaclass to make a metaclassed class a singleton'''
    def __init__(cls, name, bases, dct):
        super(MetaSingleton, cls).__init__(name, bases, dct)
        cls._singleton = None

    def __call__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = (
                super(MetaSingleton, cls).__call__(*args, **kwargs))

        return cls._singleton


class SharpPointStore(with_metaclass(MetaSingleton, object)):
    '''Singleton class wrapping to control the connections to SharpPoint.

    Params:

      - ``token`` (default:``None``): API access token

      - ``account`` (default: ``None``): account id

      - ``practice`` (default: ``False``): use the test environment

      - ``account_tmout`` (default: ``10.0``): refresh period for account
        value/cash refresh
    '''

    BrokerCls = None  # broker class will autoregister
    DataCls = None  # data class will auto register
    BackTestCls = None

    params = (
        ('gateway', 'http://localhost:5000/'),
        ('token', ''),
        ('account', ''),
        ('login', None),
        ('practice', False),
        ('loglevel', logging.INFO),
        ('account_tmout', 30.0),
    )

    _DTEPOCH = datetime(1970, 1, 1)
    _ENVPRACTICE = 'practice'
    _ENVLIVE = 'live'

    @classmethod
    def getdata(cls, *args, **kwargs):
        '''Returns ``DataCls`` with args, kwargs'''
        return cls.DataCls(*args, **kwargs)

    @classmethod
    def getbroker(cls, *args, **kwargs):
        '''Returns broker with *args, **kwargs from registered ``BrokerCls``
or ``BackTestCls``
        '''
        backtest = kwargs.pop('backtest', False)
        if backtest:
            return cls.BackTestCls(*args, **kwargs)
        return cls.BrokerCls(*args, **kwargs)

    def __init__(self):
        super(SharpPointStore, self).__init__()

        self.positions = collections.defaultdict(Position)
        self.notifs = collections.deque()  # store notifications for cerebro

        self._env = None  # reference to cerebro for general notifications
        self.broker = None  # broker instance
        self.datas = list()  # datas that have registered over start

        self._orders = collections.OrderedDict()  # map order.ref to oid
        self._ordersrev = collections.OrderedDict()  # map oid to order.ref
        self._transpend = collections.defaultdict(collections.deque)

        self._oenv = self._ENVPRACTICE if self.p.practice else self._ENVLIVE

        self._cash = 0.0
        self._value = 0.0
        self.q_account = queue.Queue()
        self.q_ordercreate = queue.Queue()
        self.q_orderclose = queue.Queue()
        self.streaming_events()

    def start(self, data=None, broker=None):
        # Datas require some processing to kickstart data reception
        if data is None and broker is None:
            self.cash = None
            return

        if data is not None:
            self._env = data._env
            # For datas simulate a queue with None to kickstart co
            self.datas.append(data)

            if self.broker is not None:
                self.broker.data_started(data)

        elif broker is not None:
            self.broker = broker
            self.broker_threads()

    def stop(self):
        # signal end of thread
        if self.broker is not None:
            self.q_ordercreate.put(None)
            self.q_orderclose.put(None)
            self.q_account.put(None)

    def put_notification(self, msg, *args, **kwargs):
        self.notifs.append((msg, args, kwargs))

    def get_notifications(self):
        '''Return the pending "store" notifications'''
        self.notifs.append(None)  # put a mark / threads could still append
        return [x for x in iter(self.notifs.popleft, None)]

    def get_positions(self):
        pass

    def get_granularity(self, timeframe, compression):
        pass

    def get_instrument(self, dataname):
        pass

    def _get_request(self, method, **kwargs):
        return requests.get(self.p.gateway + method,
                            **kwargs)

    def _post_request(self, method, **kwargs):
        return requests.post(self.p.gateway + method,
                             **kwargs)

    def streaming_events(self, tmout=None):
        q = queue.Queue()
        kwargs = {'q': q, 'tmout': tmout}

        t = threading.Thread(target=self._t_streaming_listener, kwargs=kwargs)
        t.daemon = True
        t.start()

    def updateposition(self, data):
        """Update position from streamer"""
        position = Position(data['Qty'],
                            abs(data['TotalAmt']/data['Qty']))
        self.positions[data['ProdCode']] = position

    def getposition(self, data, clone=False):
        position =  self.positions[data]
        if clone:
            return copy(position)
        else:
            return position

    def _t_streaming_listener(self, q, tmout=None):
        response = self._get_request("log/subscribe", stream=True)
        client = sseclient.SSEClient(response)
        for event in client.events():
            data = json.loads(event.data)
            info = data.get('data', None)
            oref = 0

            if event.event == "AccountPositionPush":
                if self.p.loglevel <= logging.DEBUG:
                    print(event.event, data)
                self.updateposition(data)
                continue
            if self.broker is None:
                continue

            try:
                oref = int(info['Ref2'])
            except:
                if self.p.loglevel <= logging.DEBUG:
                    print("Unhandled event")
                continue

            if self.p.loglevel <= logging.DEBUG:
                print(event)
            if event.event == "OrderBeforeSendReport":
                if self.p.loglevel <= logging.DEBUG:
                    print(data)
                self.broker._submit(oref)
            elif event.event == "OrderRequestFailed":
                if self.p.loglevel <= logging.DEBUG:
                    print(data)
                self.broker._reject(oref)
            elif event.event == "OrderReport":
                if self.p.loglevel <= logging.DEBUG:
                    print(data)
                status = int(info['Status'])
                if status == 4:
                    self.broker._accept(oref)
                elif status == 6:
                    self.broker._cancel(oref)
            elif event.event == "TradeReport":
                if self.p.loglevel <= logging.DEBUG:
                    print(data)
                qty = int(info['Qty'])
                price = float(info['Price'])
                self.broker._fill(oref, qty, price)

    def streaming_prices(self, dataname, tmout=None):
        q = queue.Queue()
        kwargs = {'q': q, 'dataname': dataname, 'tmout': tmout}
        t = threading.Thread(target=self._t_streaming_prices, kwargs=kwargs)
        t.daemon = True
        t.start()
        return q

    def _t_streaming_prices(self, dataname, q, tmout):
        r = self._get_request("ticker/subscribe/" + dataname)

    def get_cash(self):
        return self._cash

    def get_value(self):
        return self._value

    def broker_threads(self):
        self.q_account.put(True)  # force an immediate update
        t = threading.Thread(target=self._t_account)
        t.daemon = True
        t.start()

        t = threading.Thread(target=self._t_order_create)
        t.daemon = True
        t.start()

        t = threading.Thread(target=self._t_order_cancel)
        t.daemon = True
        t.start()

    _ORDEREXECS = {
        bt.Order.Market: 'market',
        bt.Order.Limit: 'limit',
        bt.Order.Stop: 'stop',
        bt.Order.StopLimit: 'stop',
    }

    def isloggedin(self):
        login_info = self._get_request("login-info").json()
        if self.p.loglevel <= logging.DEBUG:
            print("login-info", login_info)
        return int(login_info['status']) != -1

    def setlogin(self, login):
        self.p.login = login
        self.q_account.put(True)  # force an immediate update

    def _t_account(self):
        if self.p.loglevel <= logging.DEBUG:
            print("t_account")
        while True:
            try:
                msg = self.q_account.get(timeout=self.p.account_tmout)
                if msg is None:
                    break  # end of thread
            except queue.Empty:  # tmout -> time to refresh
                pass
            try:
                if self.p.login is not None and not self.isloggedin():
                    if self.p.loglevel <= logging.DEBUG:
                        print("login", self.p.login)
                    r = self._post_request("login", json=self.p.login)
            except Exception as e:
                self.put_notification(e)
                continue

    def order_create(self, order, **kwargs):
        okwargs = {"DecInPrice": 0,
                   "ClOrderId": "test2",
                   "OpenClose": 0,
                   "CondType": 0,
                   "OrderType": 0,
                   "ValidType": 0,
                   "StopType": 0,
                   "OrderOptions": 0}
        if order.isbuy():
            okwargs['BuySell'] = "B"
        elif order.issell():
            okwargs['BuySell'] = "S"
        okwargs['Price'] = order.created.price
        okwargs['Qty'] = abs(order.created.size)
        okwargs['ProdCode'] = order.data._dataname
        okwargs['Ref'] = kwargs.get('Ref', '')
        okwargs['Ref2'] = str(order.ref)
        if self.p.loglevel <= logging.DEBUG:
            print(okwargs)
        self.q_ordercreate.put((order.ref, okwargs,))
        return order

    def _t_order_create(self):
        while True:
            msg = self.q_ordercreate.get()
            if msg is None:
                break
            oref, okwargs = msg
            if self.p.loglevel <= logging.DEBUG:
                print(msg)
            try:
                r = self._post_request("order/add", json=okwargs)
            except Exception as e:
                self.put_notification(e)
                self.broker._reject(order.ref)
                return

    def order_cancel(self, order):
        self.q_orderclose.put(order.ref)
        return order

    def _t_order_cancel(self):
        while True:
            order = self.q_orderclose.get()
            if oref is None:
                break

            oid = self._orders.get(oref, None)
            if oid is None:
                continue  # the order is no longer there
            try:
                o = self.oapi.close_order(self.p.account, oid)
            except Exception as e:
                continue  # not cancelled - FIXME: notify
            self.broker._cancel(oref)

if __name__ == '__main__':
    s = SharpPointStore()
