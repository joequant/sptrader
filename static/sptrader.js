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
	return {data: "HelloWorld\n"};
    },
    addData: function (data) {
	var log = this.state.data;
	this.setState({data: log + data.level + ": " + data.msg + "\n"});
    },
    componentDidMount: function() {
	var source = new EventSource(this.props.url);
	var obj = this;
	source.addEventListener(this.props.event, function(event) {
	    var data = JSON.parse(event.data);
	    obj.addData(data);
	});
    },
    render: function() {
        return (<FormControl componentClass="textarea" defaultValue={this.state.data} />);
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
console.log("HEELOO!!!");console.log
var LoginForm = React.createClass({
    getInitialState: function() {
	return {
	    host: '',
	    port: 8080,
	    license: '',
	    app_id : '',
	    user_id : '',
	    password: ''
	};
    },
    onChange: function(e) {
	var change = {}
	change[e.target.id] = e.target.value;
	this.setState(change);
    },
    onSubmit: function(e) {
	console.log(this.state);
    },
    render: function() {
	return (
		<Modal.Dialog>
		<Modal.Header>
		<Modal.Title>Login</Modal.Title>
		</Modal.Header>
		<Modal.Body>
		<FieldGroup
	    id="host"
	    type="text"
	    label="Host"
	    placeholder="Enter host"
	    onChange={this.onChange}
	    value={this.state.host}
		/>
		<FieldGroup
	    id="port"
	    type="text"nodejs windows installer
	    label="Port"
	    placeholder="Enter port"
	    onChange={this.onChange}
	    value={this.state.port}
		/>
		<FieldGroup
	    id="license"
	    type="text"
	    label="License"
	    placeholder="Enter license"
	    onChange={this.onChange}
	    value={this.state.license}
		/>
		<FieldGroup
	    id="app_id"
	    type="text"
	    label="App Id"
	    placeholder="Enter app id"
	    onChange={this.onChange}
	    	    value={this.state.app_id}
		/>
		<FieldGroup
	    id="user_id"
	    type="text"
	    label="User Id"
	    placeholder="Enter user id"
	    onChange={this.onChange}
	    value={this.state.user_id}
		/>
		<FieldGroup
	    id="password"
	    label="Password"
	    type="password"
	    onChange={this.onChange}
	    value={this.state.password}
		/>
		</Modal.Body>
		<Modal.Footer>
		<Button
	    onClick={this.onSubmit}>
		Login
	    </Button>
		</Modal.Footer>
		</Modal.Dialog>
	);
    }
});

const tabsInstance = (

	<Tabs>
	<Tab eventKey={1} title="Login"><LoginForm/></Tab>
    <Tab eventKey={2} title="Scratchpad">
      <ButtonToolbar>
	<Button bsStyle="success" onClick={publish}>Ping</Button>
	</ButtonToolbar>
	<SubscribeBox url="/subscribe" event="ping" />
	<DataGrid
    idProperty='id' emptyText={'No records'} columns={columns} dataSource={data} style={{height:400}} />

    </Tab>
</Tabs>
);


var helloWorld = React.createClass({
    render: function() {
	return (<h2>Greetings from algobroker</h2>)
    }
});

ReactDOM.render(
    React.createElement(helloWorld, null),
    document.getElementById('content')
);
ReactDOM.render(tabsInstance, document.getElementById('test'));
