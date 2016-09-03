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
    onSubmit: function(e) {
	this.props.onSubmit(this.state.data);
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
	    name="product"
	    type="text"
	    label="Product"
	    onChange={this.onChange}
	    value={this.state.data.product}
		/>
		<FieldGroup
	    name="price"
	    type="text"
	    label="Price"
	    onChange={this.onChange}
	    value={this.state.data.price}
		/>
		<FieldGroup
	    name="qty"
	    type="text"
	    label="Qty"
	    onChange={this.onChange}
	    value={this.state.data.qty}
		/>
		</Col>
		<Col sm={6} md={3}>
				<FieldGroup
	    name="cond"
	    type="text"
	    label="Cond"
	    onChange={this.onChange}
	    value={this.state.data.cond}
		/>
		<FieldGroup
	    name="type"
	    type="text"
	    label="Type"
	    onChange={this.onChange}
	    value={this.state.data.type}
		/>
		<FieldGroup
	    name="date"
	    type="text"
	    label="Date"
	    onChange={this.onChange}
	    value={this.state.data.date}
		/>
		<FieldGroup
	    name="Stop"
	    type="text"
	    label="Stop/Trigger"
	    onChange={this.onChange}
	    value={this.state.data.stoplimit}
		/>
		<FieldGroup
	    name="ref"
	    type="text"
	    label="Ref"
	    onChange={this.onChange}
	    value={this.state.data.ref}
		/>

		</Col>
		</Row>
		</Grid>
		<Button
	    onClick={this.onSubmit}>
		Buy
		</Button>
		<Button
	    onClick={this.onSubmit}>
		Sell
		</Button>
		<Button
	    onClick={this.onSubmit}>
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
