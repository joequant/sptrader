import React from 'react';
import {Modal, Button, FormControl, FormGroup,
	ControlLabel, HelpBlock, Col, Row, Grid} from 'react-bootstrap';

function FieldGroup({ id, label, help, ...props }) {
  return (
    <div>
      <label>{label}</label>
      <FormControl {...props} />
      {help && <HelpBlock>{help}</HelpBlock>}
    </div>
  );
}

var OrderForm = React.createClass({
    getInitialState: function() {
	var l = this;
	return {
	    data: {
	    },
	    confirm_text: '',
	    confirm_show: false
	};
    },
    onChange: function(e) {
	var change = this.state.data;
	change[e.target.name] = e.target.value;
	this.setState({"data": change});
    },
    onChangeFloat: function(e) {
	var change = this.state.data;
	change[e.target.name] = e.target.value;
	this.setState({"data": change});
    },
    onChangeInt: function(e) {
	var change = this.state.data;
	change[e.target.name] = parseInt(e.target.value);
	this.setState({"data": change});
    },
    onBuy: function(e) {
	var d = this.state.data;
	d['BuySell'] = 'B';
	d['CondType'] = 0;
	d['OrderType'] = 0;
	d['Price'] = parseFloat(d['Price']);
	this.setState({"confirm_show": true,
		       "data": d,
		       "confirm_text" : JSON.stringify(d)});
    },
    onSell: function(e) {
	var d = this.state.data;
	d['BuySell'] = 'S';
	d['CondType'] = 0;
	d['OrderType'] = 0;
	d['Price'] = parseFloat(d['Price']);
	this.setState({"confirm_show": true,
		       "data": d,
		       "confirm_text" : JSON.stringify(d)});
    },
    onConfirm: function(e) {
	this.setState({"confirm_show": false});
	this.props.onSubmit(this.state.data);
    },
    onCancel: function(e) {
	this.setState({"confirm_show": false});
	this.props.onCancel();
    },
    render: function() {
	return (<div>
		<Modal show={this.state.confirm_show}>
		<Modal.Header>
		</Modal.Header>
		<Modal.Body>
		{this.state.confirm_text}
		<Button
		onClick={this.onConfirm}>
		Confirm
		</Button>
		<Button
		onClick={this.onCancel}>
		Cancel
		</Button>
		</Modal.Body>
		</Modal>
		<Modal show={this.props.show}>
		<Modal.Header>
		<Modal.Title>Order</Modal.Title>
		</Modal.Header>
		<Modal.Body>
		<Grid>
		<Row>
		<Col sm={6} md={3}>
		<FieldGroup
	    name="ProdCode"
	    type="text"
	    label="Product"
	    onChange={this.onChange}
	    value={this.state.data.ProdCode}
		/>
		<FieldGroup
	    name="Price"
	    type="text"
	    label="Price"
	    onChange={this.onChangeFloat}
	    value={this.state.data.Price}
		/>
		<FieldGroup
	    name="Qty"
	    type="text"
	    label="Qty"
	    onChange={this.onChangeInt}
	    value={this.state.data.Qty}
		/>
		</Col>
		<Col sm={6} md={3}>
<FormGroup controlId="formControlsSelect">
      <ControlLabel>CondType</ControlLabel>
		<FormControl componentClass="select" placeholder="select"
		name="CondType"
		onChange={this.onChangeInt}
		value={this.state.data.CondType}
		>
        <option value="0">Normal order</option>
      </FormControl>
    </FormGroup>
<FormGroup controlId="formControlsSelect">
<ControlLabel>Order Type</ControlLabel>
<FormControl componentClass="select" placeholder="select"
		name="OrderType" onChange={this.onChangeInt}
		value={this.state.data.CondType}
		>
<option value="0">Limit</option>
</FormControl>
</FormGroup>
		<FieldGroup
	    name="Ref"
	    type="text"
	    label="Ref"
	    onChange={this.onChange}
	    value={this.state.data.Ref}
		/>

		</Col> */
		</Row>
		</Grid>
		<Button
	    onClick={this.onBuy}>
		Buy
		</Button>
		<Button
	    onClick={this.onSell}>
		Sell
		</Button>
		<Button
	    onClick={this.onCancel}>
		Cancel
		</Button>
		</Modal.Body>
		<Modal.Footer>
		</Modal.Footer>
		</Modal>
		</div>
	);
    }
});
module.exports = OrderForm;
