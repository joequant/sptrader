import React from 'react';
import ReactDOM from 'react-dom';
import {Tabs, Tab, ButtonToolbar, Button, FormControl,
	FormGroup, ControlLabel, HelpBlock, Modal} from 'react-bootstrap';
import ReactAddonsLinkedStateMixin from 'react-addons-linked-state-mixin';
import {AgGridReact} from 'ag-grid-react';
import LoginForm from './login-form';
import ConnectionTable from './tables/connection-table';
import SampleTable from './tables/sample-table';
import OrderTable from './tables/order-table';
import OrderForm from './order-form';
import PositionTable from './tables/position-table';
import TradeTable from './tables/trade-table';
import AccountTable from './tables/account-table';
import TickerControl from './ticker-control';
import StrategyTab from './strategy-tab';
import BacktestTab from './backtest-tab';
// load (Polyfill) EventSource, in case browser does not support it...
require('eventsource-polyfill');

var AlertBox = React.createClass( {
    ok() {
	this.props.ok();
    },
    clear() {
	this.props.clear();
    },
    render() {
	return (<Modal show={this.props.show}>
		<Modal.Header>
		</Modal.Header>
		<Modal.Body>
		<FormControl componentClass="textarea"
		value={this.props.text} />
		<Button
		onClick={this.ok}>
		OK
		</Button>
		<Button
		onClick={this.clear}>
		Clear
		</Button>
		</Modal.Body>
		</Modal>);
    }
});

var SubscribeBox = React.createClass( {
    getInitialState: function() {
	return {};
    },
    componentDidMount: function() {
	var source = new EventSource(this.props.url);
	var obj = this;
	$.each(this.props.event, function(k, v) {
	    source.addEventListener(k, v);
	});
	source.onerror = function(e) {
	    obj.props.onerror(e);
	};
    },
    render: function() {
        return null;
    }
});

function publish() {
    $.get("/ping");
};

var columns = [
    { name : 'index' },
    { name : 'firstName' },
    { name : 'city' }
]

var data = [];

function FieldGroup({ id, label, help, ...props }) {
  return (
    <div>
      <label>{label}</label>
      <FormControl {...props} />
      {help && <HelpBlock>{help}</HelpBlock>}
    </div>
  );
}

var SpTraderApp = React.createClass({
    getInitialState() {
	var l = this;
	$.getJSON("/login-info", function(d) {
	    if (parseInt(d.status) != -1) {
		l.setState({showLoginForm: false});
		l.fillTables();
	    }
	    if (d.connected != undefined) {
		l.setState({connection_info: d.connected});
	    }
	    if (d.account_info != undefined) {
		l.setState({account_info: d.account_info});
	    }
	    if (d.account_fields != undefined) {
	    	l.setState({account_fields: d.account_fields});
	    }
	    if (d.strategy_list != undefined) {
	    	l.setState({strategy_list: d.strategy_list});
	    }
	    l.setState({info: d.info});
	});

	return {
	    log: '',
	    loginLabel: '',
	    account_info: {},
	    connection_info: {},
	    showLoginForm: true,
	    showOrderForm: false,
	    showAlertBox: false,
	    alertText: '',
	    tickers: [],
	    orders: [],
	    trades: [],
	    positions: [],
	    account_fields: [],
	    strategy_info: {},
	    strategy_list: []
	};
    },
    submitModal(data) {
	$.ajax({
	    type: 'post',
	    url: '/login',
	    data: JSON.stringify(data),
	    contentType: "application/json"
	});
    },
    logout() {
	$.get("/logout");
	this.setState({loginLabel: '',
		       showLoginForm: true});
    },
    onerror(event) {
	if (!this.state.showLoginForm) {
	    this.setState({loginLabel: 'Connection broken',
			   showLoginForm: true});
	}
    },
    addToLog(event) {
	data = JSON.parse(event.data);
	console.log(data);
	this.setState({log: this.state.log + event.data + "\n"});
    },
    loginReply(event) {
	data = JSON.parse(event.data);
	console.log(data);
	this.setState({log: this.state.log + event.data + "\n"});
	if (parseInt(data.ret_code) != 0) {
	    this.setState({loginLabel: data.ret_msg});
	} else {
	    this.setState({showLoginForm: false});
	}
    },
    connectedReply(event) {
	data = JSON.parse(event.data);
	console.log(data);
	this.setState({log: this.state.log + event.data + "\n"});
	var conn_info = this.state.connection_info;
	var host_type = parseInt(data.host_type);
	var con_status = parseInt(data.con_status);
	conn_info[host_type] = con_status;
	this.setState({conn_info: conn_info})
	if (parseInt(host_type) == 80 &&
	    parseInt(con_status) == 2) {
	    this.fillTables();
	}
    },
    fillTables() {
	var l = this;
	$.getJSON("/account-info");
	$.getJSON("/ticker/list", function(d) {
	    l.setState({tickers: d.data});
	});
	$.getJSON("/order/list", function(d) {
	    l.setState({orders: d.data});
	});
	$.getJSON("/trade/list", function(d) {
	    l.setState({trades: d.data});
	});
    },
    showOrderForm(event) {
	this.setState({showOrderForm: true});
    },
    hideOrderForm(event) {
	this.setState({showOrderForm: false});
    },
    hideAlertBox(event) {
	this.setState({showAlertBox: false});
    },
    clearAlertBox(event) {
	this.setState({alertText: ""});
    },
    orderFailed(event) {
	this.setState({alertText: this.state.alertText + "\n" +
		       JSON.stringify(event.data),
		       showAlertBox: true});
    },
    submitOrder(data) {
	console.log(data);
	$.ajax({
	    type: 'post',
	    url: '/order/add',
	    data: JSON.stringify(data),
	    contentType: "application/json"
	});
	this.setState({showOrderForm: false});
    },
    accountInfoPush(event) {
	data = JSON.parse(event.data);
	console.log(data);
	this.setState({account_info: data.data});
    },
    updateTickers(event) {
	data = JSON.parse(event.data);
	console.log(data);
	this.setState({tickers: data.data});
    },
    updateTrades(event) {
	var data = JSON.parse(event.data).data;
	var d = this.state.trades;
	var found = false;
	console.log(data);
	for (var i =0; i < d.length; i++) {
	    if (d[i].IntOrderNo == data.IntOrderNo) {
		d[i] = data;
		found = true;
	    }
	}
	if (!found) {
	    d.push(data);
	}
	this.setState({trades: d});
    },
    updateOrders(event) {
	var data = JSON.parse(event.data).data;
	console.log(data);
	var d = this.state.orders;
	var found = false;
	for (var i =0; i < d.length; i++) {
	    if (parseInt(d[i].IntOrderNo) == parseInt(data.IntOrderNo)) {
		d[i] = data;
		found = true;
	    }
	}
	if (!found) {
	    console.log("order added");
	    d.push(data);
	}
	console.log("orders", d);
	this.setState({orders: d});
    },
    strategyStatus(event) {
	var data = JSON.parse(event.data);
	console.log(data);
	var d = this.state.strategy_info;
	if (d[data['strategy']] == undefined) {
	    d[data['strategy']] = {};
	}
	d[data['strategy']][data['id']] =
	    {status: data['status'],
	     comment: data['comment']};
	console.log(d);
	this.setState({strategy_info: d});
    },
    render() {
	var events = {
	    "ping" : this.addToLog,
	    "LoginReply" : this.loginReply,
	    "ConnectedReply" : this.connectedReply,
	    "OrderRequestFailed" : this.orderFailed,
	    "OrderReport" : this.updateOrders,
	    "OrderBeforeSendReport" : this.addToLog,
	    "AccountLoginReply" : this.addToLog,
	    "AccountInfoPush" : this.accountInfoPush,
	    "AccountPositionPush" : this.addToLog,
	    "UpdatedAccountPositionPush" : this.addToLog,
	    "UpdatedAccountBalancePush" : this.addToLog,
	    "TradeReport" : this.updateTrades,
	    "PriceUpdate" : this.addToLog,
	    "TickerUpdate" : this.updateTickers,
	    "PswChangeReply" : this.addToLog,
	    "ProductListByCodeReply" : this.addToLog,
	    "InstrumentListReply" : this.addToLog,
	    "BusinessDateReply" : this.addToLog,
	    "MMOrderBeforeSendReport" : this.addToLog,
	    "MMOrderRequestFailed" : this.addToLog,
	    "QuoteRequestReceived" : this.addToLog,
	    "LocalStrategyStatus" : this.strategyStatus
	}
	return(
		<Tabs id="tabs">
		<Tab eventKey={1} title="Account" >
		<LoginForm show={this.state.showLoginForm}
	    label={this.state.loginLabel}
	    data={this.state.info}
	    onSubmit={this.submitModal}/>
		<Button bsStyle="success" onClick={this.logout}>Logout</Button>
		<ConnectionTable data={this.state.connection_info}/>
		<Tabs id="tab1">
		<Tab eventKey={1} title="Account" >
		<AccountTable
	    fields={this.state.account_fields} 
	    data={this.state.account_info} />
		</Tab>
		<Tab eventKey={2} title="Order" >
		<AlertBox show={this.state.showAlertBox}
	    text={this.state.alertText}
	    ok={this.hideAlertBox}
	    clear={this.clearAlertBox} />
		<OrderForm show={this.state.showOrderForm}
	    onSubmit={this.submitOrder}
	    onCancel={this.hideOrderForm}/>

		<Button bsStyle="success" onClick={this.showOrderForm}>Show Order Form</Button>
		<OrderTable data={this.state.orders} />
		</Tab>
		<Tab eventKey={3} title="Position" >
		<PositionTable data={this.state.positions} />
		</Tab>
		<Tab eventKey={4} title="Trade" >
		<TradeTable data={this.state.trades}/>
		</Tab>
		<Tab eventKey={5} title="Ticker" >
		<TickerControl tickers={this.state.tickers}/>
		</Tab>
		</Tabs>
		</Tab>
		<Tab eventKey={2} title="Strategy" >
		<StrategyTab info={this.state.strategy_info}
	    strategylist={this.state.strategy_list} />
		</Tab>
		<Tab eventKey={3} title="Backtest" >
		<BacktestTab strategylist={this.state.strategy_list} />
		</Tab>
		<Tab eventKey={4} title="Scratchpad">
		<ButtonToolbar>
		<Button bsStyle="success" onClick={publish}>Ping</Button>
		</ButtonToolbar>
		<SubscribeBox url="/log/subscribe" event={events}
	    onerror={this.onerror} />
		<FormControl componentClass="textarea" value={this.state.log} />
		<SampleTable/>
		</Tab>
		</Tabs>
	)
    }
});

ReactDOM.render(
    <SpTraderApp />,
    document.getElementById('test')
);
