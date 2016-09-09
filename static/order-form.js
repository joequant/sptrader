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
	    }
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
	d['Price'] = parseFloat(d['Price']);
	this.props.onSubmit(d);
    },
    onSell: function(e) {
	var d = this.state.data;
	d['BuySell'] = 'S';
	d['Price'] = parseFloat(d['Price']);
	this.props.onSubmit(d);
    },
    onCancel: function(e) {
	this.props.onCancel();
    },
    render: function() {
	return (<Modal show={this.props.show}>
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
				<FieldGroup
	    name="CondType"
	    type="text"
	    label="Cond"
	    onChange={this.onChangeInt}
	    value={this.state.data.CondType}
		/>
		<FieldGroup
	    name="OrderType"
	    type="text"
	    label="Type"
	    onChange={this.onChangeInt}
	    value={this.state.data.OrderType}
		/>
		<FieldGroup
	    name="Ref"
	    type="text"
	    label="Ref"
	    onChange={this.onChange}
	    value={this.state.data.Ref}
		/>

		</Col>
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
	);
    }
});
module.exports = OrderForm;
