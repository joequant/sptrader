import React from 'react';
import ReactDOM from 'react-dom';
var ReactBootstrap = require('react-bootstrap');
var ReactAddonsLinkedStateMixin = require('react-addons-linked-state-mixin');
import {AgGridReact} from 'ag-grid-react';
import LoginForm from './login-form';

var Tabs = ReactBootstrap.Tabs;
var Tab = ReactBootstrap.Tab;
var ButtonToolbar = ReactBootstrap.ButtonToolbar;
var Button = ReactBootstrap.Button;
var FormControl = ReactBootstrap.FormControl;
var FormGroup = ReactBootstrap.FormGroup;
var ControlLabel = ReactBootstrap.ControlLabel;
var HelpBlock = ReactBootstrap.HelpBlock;
var Modal = ReactBootstrap.Modal;

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
	$.getJSON("/get-login-status/80", function(d) {
	    if (parseInt(d) != -1) {
		l.setState({showModal: false});
	    }
	});
	return {
	    log: '',
	    loginLabel: '',
	    showModal: true,
	    columnDefs: [
		{headerName: "Name",
		 field: "name",
		 enableRowGroup: true, enablePivot: true,
		 width: 150, pinned: true}],
	    rowData: [{name: "foobar"}]
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
	$.get("/logout", data);
	this.setState({loginLabel: ''});
	this.setState({showModal: true});
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
	if (parseInt(data.ret_code) == 0) {
	    this.setState({showModal: false});
	} else {
	    this.setState({loginLabel: data.ret_msg});
	}
    },
    connectedReply: function(event) {
	data = JSON.parse(event.data);
	console.log(data);
	this.setState({log: this.state.log + event.data + "\n"});
	if (parseInt(data.host_type) == 80 &&
	    parseInt(data.con_status) == 3) {
	    this.setState({showModal: false});
	    $.get("/get-account-info");
	}
    },
    accountInfoPush: function(event) {
	data = JSON.parse(event.data);
	console.log(data);
	this.setState({log: this.state.log + event.data + "\n"});
    },
    render: function() {
	var events = {
	    "ping" : this.addToLog,
	    "LoginReply" : this.loginReply,
	    "ConnectedReply" : this.connectedReply,
	    "AccountInfoPush" : this.accountInfoPush
	}
	return(
	<Tabs id="tabs">
		<Tab eventKey={1} title="Login">
		<LoginForm show={this.state.showModal}
	    label={this.state.loginLabel}
	    onSubmit={this.submitModal}/>
	<Button bsStyle="success" onClick={this.logout}>Logout</Button>
    </Tab>
    <Tab eventKey={2} title="Scratchpad">
      <ButtonToolbar>
	<Button bsStyle="success" onClick={publish}>Ping</Button>
	</ButtonToolbar>
	<SubscribeBox url="/subscribe" event={events} />
		<FormControl componentClass="textarea" value={this.state.log} />
		<div className="ag-material">
		<AgGridReact
	    // column definitions and row data are immutable, the grid
	    // will update when these lists change
	    columnDefs={this.state.columnDefs}
	    rowData={this.state.rowData}

	    // or provide props the old way with no binding
	    rowSelection="multiple"
	    enableSorting="true"
	    enableFilter="true"
                   rowHeight="22"
		/>
		</div>
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
