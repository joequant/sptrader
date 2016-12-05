Modules in directories other than strategy are
Copyright (c) 2016 Bitquant Research Laboratories (Asia) Limited
Released under the Simplified BSD License

The modules in the directory "strategy" are copyright by their owners
and may contain proprietary and confidential code, which are not
intended for public release.

NOTE that this system is NOT supported by SharpPoint.

SYSTEM REQUIREMENTS
-------------------

Windows 10.  The python scripts don't work on linux because the
SPtrader modules have been build with C++ symbols.  It should be a
real easy thing to write an adapter.

INSTALL
-------

Right click. install and run the install script under PowerShell

RUN
---

Double click scripts/webui.py
Take web browser and point to http://localhost:5000/

BATCH_BACKTESTER
----------------

Put a configuration .json file in data (example sample)
Run scripts/webui.py
Run scripts/backtest_files.py (config name) (file names)

Files are log files exported by SPTrader application.  Sample file in
included in data HSI_20150409.txt



TESTS
-----
There are a number of other scripts in directory tests



DEMO ACCOUNTS
-------------

This software requires an SPTrader account.  Demo accounts are
available via

http://www.sharppoint.com.hk/algo.php?lang=1&mod=api




