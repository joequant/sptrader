var React = require('react');
var ReactDOM = require('react-dom');
var DataGrid = require('react-datagrid');
var ReactBootstrap = require('react-bootstrap');
var ReactAddonsLinkedStateMixin = require('react-addons-linked-state-mixin');

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
        return '';
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
var LoginForm = React.createClass({
    getInitialState: function() {
	var l = this;
	$.getJSON("/logininfo", function(d) {
	    d.password = '';
	    l.setState({"data" : d});
	});
	return {
	    data: {
		host: '',
		port: 8080,
		license: '',
		app_id: '',
		user_id: '',
		password: ''
	    }
	};
    },
    onChange: function(e) {
	var change = this.state.data;
	change[e.target.name] = e.target.value;
	this.setState({"data": change});
    },
    onSubmit: function(e) {
	this.props.onSubmit(this.state.data);
    },
    render: function() {
	return (<form>
		<Modal show={this.props.show}>
		<Modal.Header>
		<Modal.Title>Login</Modal.Title>
		</Modal.Header>
		<Modal.Body>
		<FieldGroup
	    name="host"
	    type="text"
	    label="Host"
	    placeholder="Enter host"
	    onChange={this.onChange}
	    value={this.state.data.host}
		/>
		<FieldGroup
	    name="port"
	    type="text"
	    label="Port"
	    placeholder="Enter port"
	    onChange={this.onChange}
	    value={this.state.data.port}
		/>
		<FieldGroup
	    name="license"
	    type="text"
	    label="License"
	    placeholder="Enter license"
	    onChange={this.onChange}
	    value={this.state.data.license}
		/>
		<FieldGroup
	    name="app_id"
	    type="text"
	    label="App Id"
	    placeholder="Enter app id"
	    onChange={this.onChange}
	    value={this.state.data.app_id}
		/>
		<FieldGroup
	    name="user_id"
	    type="text"
	    label="User Id"
	    placeholder="Enter user id"
	    onChange={this.onChange}
	    value={this.state.data.user_id}
		/>
		<FieldGroup
	    name="password"
	    label="Password"
	    type="password"
	    onChange={this.onChange}
	    value={this.state.data.password}
		/>
		</Modal.Body>
		<Modal.Footer>
		<Button
	    onClick={this.onSubmit}>
		Login
	    </Button>
		</Modal.Footer>
		</Modal>
		</form>
	);
    }
});

var SpTraderApp = React.createClass({
    getInitialState: function() {
	return {
	    log: '',
	    showModal: true
	};
    },
    submitModal: function(data) {
	this.setState({showModal: false});
	console.log(data);
	$.ajax({
	    type: 'post',
	    url: '/login',
	    data: JSON.stringify(data),
	    contentType: "application/json"
	});
    },
    logout: function() {
	$.get("/logout", data);
	this.setState({showModal: true});
    },
    addToLog: function(event) {
	this.setState({log: this.state.log + JSON.stringify(event.data) + "\n"});
    },
    render: function() {
	var events = {
	    "ping" : this.addToLog
	}
	return(
	<Tabs id="tabs">
		<Tab eventKey={1} title="Login">
		<LoginForm show={this.state.showModal}
	    onSubmit={this.submitModal}/>
	<Button bsStyle="success" onClick={this.logout}>Logout</Button>
    </Tab>
    <Tab eventKey={2} title="Scratchpad">
      <ButtonToolbar>
	<Button bsStyle="success" onClick={publish}>Ping</Button>
	</ButtonToolbar>
	<SubscribeBox url="/subscribe" event={events} />
	<FormControl componentClass="textarea" value={this.state.log} />
	<DataGrid
    idProperty='id' emptyText={'No records'} columns={columns} dataSource={data} style={{height:400}} />

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
