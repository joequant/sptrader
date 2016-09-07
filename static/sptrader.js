import React from 'react';
import ReactDOM from 'react-dom';
import {Tabs, Tab, ButtonToolbar, Button, FormControl,
	FormGroup, ControlLabel, HelpBlock } from 'react-bootstrap';
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
    },
    render: function() {
        return null;
    }
});

var Injector = React.createClass( {
    mixins: [ReactAddonsLinkedStateMixin],
    getInitialState: function() {
	return {message: 'Hello!',
		textinput : ''};
    },
    inject : function() {
	var self = this;
	jQuery.ajax({
	    url: "/inject",
	    type: "POST",
	    data: self.state.textinput,
	    contentType: "application/json; charset=utf-8",
	    success: function (response) {
		self.setState({message: response});
	    }
	});
    },
    injectTest : function() {
	this.setState({message : "test inject"});
    },
    clear: function() {
	this.setState({textinput : ''});
    },
    fileOpen: function(e) {
	var self = this;
	var files = e.target.files,
	    reader = new FileReader();
	reader.onload = function() {
	    self.setState({textinput: this.result});
	}
	reader.readAsText(files[0]);
    },
    render: function() {
	return (
<div>
<Button bsStyle="success" onClick={this.inject}>Inject</Button>
<Button bsStyle="success" onClick={this.clear}>Clear</Button>
<Button bsStyle="success" onClick={this.injectTest}>Test</Button>
<FormControl componentClass="file" onChange={this.fileOpen} />
<FormControl componentClass="textarea" valueLink={this.linkState('textinput')} />
<FormControl componentClass="textarea" valueLink={this.linkState('message')} />
</div>
	);
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
console.log("New SPTrader");

var SpTraderApp = React.createClass({
    getInitialState: function() {
	var l = this;
	$.getJSON("/login-info", function(d) {
	    if (parseInt(d.status) != -1) {
		l.setState({showLoginForm: false});
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
	    tickers: [],
	    orders: [],
	    trades: []
	};
    },
    submitModal: function(data) {
	$.ajax({
	    type: 'post',
	    url: '/login',
	    data: JSON.stringify(data),
	    contentType: "application/json"
	});
    },
    logout: function() {
	$.get("/logout");
	this.setState({loginLabel: ''});
	this.setState({showLoginForm: true});
    },
    addToLog: function(event) {
	data = JSON.parse(event.data);
	console.log(data);
	this.setState({log: this.state.log + event.data + "\n"});
    },
    loginReply: function(event) {
	data = JSON.parse(event.data);
	console.log(data);
	this.setState({log: this.state.log + event.data + "\n"});
	if (parseInt(data.ret_code) != 0) {
	    this.setState({loginLabel: data.ret_msg});
	} else {
	    this.setState({showLoginForm: false});
	}
    },
    connectedReply: function(event) {
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
	    var l = this;
	    $.getJSON("/ticker/list", function(d) {
		l.setState({tickers: d.data});
	    });
	    $.getJSON("/account-info");
	    $.getJSON("/order/list", function(d) {
		l.setState({orders: d.data});
		});
	    $.getJSON("/trade/list", function(d) {
		l.setState({trades: d.data});
	    });
	}
    },
    showOrderForm: function(event) {
	this.setState({showOrderForm: true});
    },
    hideOrderForm: function(event) {
	this.setState({showOrderForm: false});
    },
    submitOrder: function(data) {
	console.log(data);
	$.ajax({
	    type: 'post',
	    url: '/order/add',
	    data: JSON.stringify(data),
	    contentType: "application/json"
	});
	this.setState({showOrderForm: false});
    },
    accountInfoPush: function(event) {
	data = JSON.parse(event.data);
	console.log(data);
	this.setState({log: this.state.log + event.data + "\n"});
	this.setState({account_info: data});
    },
    updateTickers: function(event) {
	data = JSON.parse(event.data);
	console.log(data);
	this.setState({tickers: data.data});
    },
    render: function() {
	var events = {
	    "ping" : this.addToLog,
	    "LoginReply" : this.loginReply,
	    "ConnectedReply" : this.connectedReply,
	    "AccountInfoPush" : this.accountInfoPush,
	    "UpdateTickers" : this.updateTickers,
	    "AccountPositionPush" : this.addToLog,
	    "ApiTradeReport" : this.addToLog,
	    "ApiPriceUpdate" : this.addToLog,
	    "InstrumentListReply" : this.addToLog,
	    "ProductListByCodeReply" : this.addToLog
	}
	return(
		<Tabs id="tabs">
		<Tab eventKey={1} title="Login">
		<LoginForm show={this.state.showLoginForm}
	    label={this.state.loginLabel}
	    data={this.state.info}
	    onSubmit={this.submitModal}/>
		<Button bsStyle="success" onClick={this.logout}>Logout</Button>
		<ConnectionTable data={this.state.connection_info}/>
		<Tabs id="tab1">
		<Tab eventKey={1} title="Account">
		<AccountTable data={this.state.account_info} />
		</Tab>
		<Tab eventKey={2} title="Order">
		<OrderForm show={this.state.showOrderForm}
	    onSubmit={this.submitOrder}
	    onCancel={this.hideOrderForm}/>
		<Button bsStyle="success" onClick={this.showOrderForm}>Show Order Form</Button>
		<OrderTable data={this.state.orders} />
		</Tab>
		<Tab eventKey={3} title="Position">
		<PositionTable />
		</Tab>
		<Tab eventKey={4} title="Trade">
		<TradeTable data={this.state.trades}/>
		</Tab>
		<Tab eventKey={5} title="Ticker">
		<TickerControl tickers={this.state.tickers}/>
		</Tab>
		</Tabs>
		</Tab>
		<Tab eventKey={2} title="Strategy">
		<StrategyTab />
		</Tab>
		<Tab eventKey={3} title="Scratchpad">
		<ButtonToolbar>
		<Button bsStyle="success" onClick={publish}>Ping</Button>
		</ButtonToolbar>
		<SubscribeBox url="/log/subscribe" event={events} />
		<FormControl componentClass="textarea" value={this.state.log} />
		<SampleTable/>
		</Tab>
		</Tabs>
	)
    }
});


var helloWorld = React.createClass({
    render: function() {
	return (<h2>Greetings from SPTrader</h2>)
    }
});

ReactDOM.render(
    <helloWorld />,
    document.getElementById('content')
);

ReactDOM.render(
    <SpTraderApp />,
    document.getElementById('test')
);
