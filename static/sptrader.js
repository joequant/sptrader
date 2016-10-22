import React from 'react';
import ReactDOM from 'react-dom';
import {Tabs, Tab, ButtonToolbar, Button, FormControl,
	FormGroup, ControlLabel, HelpBlock, Modal,
	Form,Checkbox} from 'react-bootstrap';
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

class AlertBox extends React.Component {
    ok() {
	this.props.ok();
    }
    clear() {
	this.props.clear();
    }
    render() {
	return (<Modal show={this.props.show}>
		<Modal.Header>
		</Modal.Header>
		<Modal.Body>
		<FormControl componentClass="textarea"
		value={this.props.text} />
		<Button
		onClick={this.ok.bind(this)}>
		OK
		</Button>
		<Button
		onClick={this.clear.bind(this)}>
		Clear
		</Button>
		</Modal.Body>
		</Modal>);
    }
}

class SubscribeBox extends React.Component {
    constructor(props) {
	super(props);
	this.state = {
	    source: this.connect()
	}
    }
    connect() {
	var source = new EventSource(this.props.url); 

	var obj = this;
	$.each(this.props.event, function(k, v) {
	    source.addEventListener(k, v);
	});
	source.onerror = function(e) {
	    obj.props.onerror(e);
	};
	return source;
    }
    reconnect() {
	console.log("reconnect", this.state.source.readyState);
	if (this.state.source.readyState == EventSource.CLOSED) {
	    console.log("closed");
	    var source = this.connect();
	    this.setState({source: source});
	} 
	return new Promise(function(resolve, reject) {
	    resolve();
	});
    }
    render() {
        return null;
    }
}

function publish() {
    $.get("/ping");
}

var data = [];

class SpTraderApp extends React.Component {
    constructor(props) {
	super(props);
		this.state = {
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
	    strategy_data: {},
	    backtest_data: {},
	    strategy_headers: {},
	    strategy_list: []
	};

	var l = this;
	this.fill_data();
	this.submitModal = this.submitModal.bind(this);
	this.logout = this.logout.bind(this);
	this.onerror = this.onerror.bind(this);
	this.addToLog = this.addToLog.bind(this);
	this.loginReply = this.loginReply.bind(this);
	this.connectedReply = this.connectedReply.bind(this);
	this.showOrderForm = this.showOrderForm.bind(this);
	this.hideOrderForm = this.hideOrderForm.bind(this);
	this.hideAlertBox = this.hideAlertBox.bind(this);
	this.clearAlertBox = this.clearAlertBox.bind(this);
	this.orderFailed = this.orderFailed.bind(this);
	this.submitOrder = this.submitOrder.bind(this);
	this.accountInfoPush = this.accountInfoPush.bind(this);
	this.updateTickers = this.updateTickers.bind(this);
	this.updateTrades = this.updateTrades.bind(this);
	this.updateOrders = this.updateOrders.bind(this);
	this.updatePositions = this.updatePositions.bind(this);
	this.strategyStatus = this.strategyStatus.bind(this);
    }
    submitModal(data) {
	var l = this;
	this._subscribe_box.reconnect().then(function() {
	    $.post('/login', data)
	}).then (function() {
		l.fill_data();
	});
    }
    fill_data() {
	var l = this;
	$.getJSON("/login-info").done(function(d) {
	    var new_state = {};
	    if (parseInt(d.status) != -1) {
		new_state.showLoginForm = false;
		l.fillTables();
	    }
	    if (d.connected != undefined) {
		new_state.connection_info = d.connected;
	    }
	    if (d.account_info != undefined) {
		new_state.account_info = d.account_info;
	    }
	    if (d.account_fields != undefined) {
	    	new_state.account_fields = d.account_fields;
	    }
	    if (d.strategy_list != undefined) {
	    	new_state.strategy_list = d.strategy_list;
	    }
	    if (d.strategy_data != undefined) {
	    	new_state.strategy_data = d.strategy_data;
	    }
	    if (d.backtest_data != undefined) {
	    	new_state.backtest_data = d.backtest_data;
	    }
	    if (d.strategy_headers != undefined) {
	    	new_state.strategy_headers = d.strategy_headers;
	    }
	    new_state.info = d.info;
	    l.setState(new_state);
	});
    }
    logout() {
	$.get("/logout");
	this.setState({loginLabel: '',
		       showLoginForm: true});
    }
    onerror(event) {
	if (!this.state.showLoginForm) {
	    this.setState({loginLabel: 'Connection broken',
			   showLoginForm: true});
	}
    }
    addToLog(event) {
	data = JSON.parse(event.data);
	console.log(data);
	this.setState({log: this.state.log + event.data + "\n"});
    }
    loginReply(event) {
	data = JSON.parse(event.data);
	console.log(data);
	this.setState({log: this.state.log + event.data + "\n"});
	if (parseInt(data.ret_code) != 0) {
	    this.setState({loginLabel: data.ret_msg});
	} else {
	    this.setState({showLoginForm: false});
	}
    }
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
    }
    fillTables() {
	var l = this;
	$when($.getJSON("/account-info"),
	      $.getJSON("/ticker/list"),
	      $.getJSON("/order/list"),
	      $.getJSON("/trade/list")).done(function(d1, d2, d3, d4) {
		  l.setState({tickers: d2.data,
			      orders: d3.data,
			      trades: d4.data});
	      });
    }
    showOrderForm(event) {
	this.setState({showOrderForm: true});
    }
    hideOrderForm(event) {
	this.setState({showOrderForm: false});
    }
    hideAlertBox(event) {
	this.setState({showAlertBox: false});
    }
    clearAlertBox(event) {
	this.setState({alertText: ""});
    }
    orderFailed(event) {
	this.setState({alertText: this.state.alertText + "\n" +
		       JSON.stringify(event.data),
		       showAlertBox: true});
    }
    submitOrder(data) {
	console.log(data);
	$.post('/order/add', data);
	this.setState({showOrderForm: false});
    }
    accountInfoPush(event) {
	data = JSON.parse(event.data);
	console.log(data);
	this.setState({account_info: data.data});
    }
    updateTickers(event) {
	data = JSON.parse(event.data);
	console.log(data);
	this.setState({tickers: data.data});
    }
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
    }
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
    }
    updatePositions(event) {
	var data = JSON.parse(event.data).data;
	console.log(data);
	var d = this.state.positions;
	var found = false;
	for (var i =0; i < d.length; i++) {
	    if (d[i].ProdCode == data.ProdCode) {
		d[i] = data;
		found = true;
	    }
	}
	if (!found) {
	    console.log("position added");
	    d.push(data);
	}
	console.log("position", d);
	this.setState({positions: d});
    }
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
    }
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
	    "AccountPositionPush" : this.updatePositions,
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
	return(<div>
	    	<SubscribeBox url="/log/subscribe" event={events}
	       onerror={this.onerror}
	       ref={(c) => this._subscribe_box = c}
	       />

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
	       strategylist={this.state.strategy_list}
	       headers={this.state.strategy_headers}
	       data={this.state.strategy_data}
	       />
		</Tab>
		<Tab eventKey={3} title="Backtest" >
	       <BacktestTab strategylist={this.state.strategy_list}
	       headers={this.state.strategy_headers}
	       data={this.state.backtest_data}	       
	       />
		</Tab>
		<Tab eventKey={4} title="Scratchpad">
		<ButtonToolbar>
		<Button bsStyle="success" onClick={publish}>Ping</Button>
		</ButtonToolbar>
		<FormControl componentClass="textarea" value={this.state.log} />
	       <SampleTable/>
           <Form inline horizontal className="backtest-control">
	       <Button onClick={this.backtest}>Backtest</Button>
	                      <Checkbox inline>Upload</Checkbox>
	                      <FormControl
	                  type='file' label='Upload' accept='.txt'/>
	                      </Form>
		</Tab>
	       </Tabs>
	       </div>
	)
    }
}

ReactDOM.render(
    <SpTraderApp />,
    document.getElementById('test')
);
