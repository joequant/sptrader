import React from 'react';
import {Modal, Button, FormControl, FormGroup,
	ControlLabel, HelpBlock, Form, Col} from 'react-bootstrap';

function FieldGroup({ id, label, help, ...props }) {
  return (
	  <FormGroup controlId={id}>
	  <Col componentClass={ControlLabel} sm={2}>{label}</Col>
	  <Col sm={10}>
      <FormControl {...props} />
	  {help && <HelpBlock>{help}</HelpBlock>}
      </Col>
    </FormGroup>
  );
}

export default class LoginForm extends React.Component {
    constructor(props) {
	super(props);
	this.state = {
	    data: {
		host: '',
		port: 8080,
		license: '',
		app_id: '',
		user_id: '',
		password: ''
	    }
	};
	this.onChange = this.onChange.bind(this);
	this.onSubmit = this.onSubmit.bind(this);
	this.onClose = this.onClose.bind(this);
    }
    componentWillReceiveProps(nextProps) {
	var d = nextProps.data;
	if (d != undefined) {
	    d.password = '';
	    this.setState({data: d});
	}
    }
    onChange(e) {
	var change = this.state.data;
	change[e.target.name] = e.target.value;
	this.setState({"data": change});
    }
    onSubmit(e) {
	this.props.onSubmit(this.state.data);
    }
    onClose(e) {
	this.props.onClose(this.state.data);
    }
    render() {
	return (<form>
		<Modal show={this.props.show}>
		<Modal.Header>
		<Modal.Title>Login</Modal.Title>
		</Modal.Header>
		<Modal.Body>
		<Form horizontal>
		<label>{this.props.label}</label>
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
		</Form>
		</Modal.Body>
		<Modal.Footer>
		<Button
	    onClick={this.onSubmit}>
		Login
	    </Button>
		<Button
	    onClick={this.onClose}>
		Close
	    </Button>
		</Modal.Footer>
		</Modal>
		</form>
	);
    }
}
