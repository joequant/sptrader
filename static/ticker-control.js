import React from 'react';
import {Button} from 'react-bootstrap';
import {AgGridReact} from 'ag-grid-react';

var TickerControl = React.createClass({
    getInitialState: function() {
	return {
	};
    },
    add_ticker: function() {
    },
    render: function() {
	var retval = (<div>
		<h2>Ticker Control</h2>
		  <Button bsStyle="success" onClick={this.add_ticker}>Add Ticker</Button>
		 </div>)
	return retval;
    }
});
    
module.exports = TickerControl;
