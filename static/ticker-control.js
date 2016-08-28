import React from 'react';
import {Button, FormControl} from 'react-bootstrap';
import {AgGridReact} from 'ag-grid-react';

var TickerControl = React.createClass({
    getInitialState: function() {
	return {
	    tickers_add: ''
	};
    },
    onChange: function(e) {
	this.setState({tickers_add: e.target.value});
    },
    add_ticker: function() {
    },
    render: function() {
	var retval = (<div>
		      <h2>Ticker Control</h2>
		      <FormControl
		      name="tickers"
		      onChange={this.onChange}
		      value={this.state.tickers_add}
		      />
		      <Button bsStyle="success" onClick={this.add_ticker}>Add Ticker</Button>
		      <br />
		      <a href="/ticker/get" target="_blank">Show ticker</a>
		 </div>)
	return retval;
    }
});
    
module.exports = TickerControl;
