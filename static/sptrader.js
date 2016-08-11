var React = require('react');
var ReactDOM = require('react-dom');
var ReactDataGrid = require('react-datagrid');
var ReactBootstrap = require('react-bootstrap');
var ReactAddonsLinkedStateMixin = require('react-addons-linked-state-mixin');

var Tabs = require('react-bootstrap').Tabs;
var Tab = require('react-bootstrap').Tab;
var ButtonToolbar = require('react-bootstrap').ButtonToolbar;
var Button = require('react-bootstrap').Button;
var FormControl = require('react-bootstrap').FormControl;

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

const tabsInstance = (
<Tabs>
    <Tab eventKey={1} title="Login"></Tab>
    <Tab eventKey={2} title="Scratchpad">
      <ButtonToolbar>
	<Button bsStyle="success" onClick={publish}>Ping</Button>

	<SubscribeBox url="/subscribe" event="ping" />
      </ButtonToolbar>
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
