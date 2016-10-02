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
	$.get("/ticker/subscribe/" + this.state.tickers_add);
    },
    clear_ticker: function(e) {
	$.get("/ticker/clear/" + e.target.name);
    },
    view_ticker: function(e) {
	var myWindow = window.open("/ticker/view/" + e.target.name);
    },
    unsubscribe_ticker: function(e) {
	$.get("/ticker/unsubscribe/" + e.target.name);
    },
    render: function() {
	var l = this;
	var items = this.props.tickers.map(function(i) {
	    return (<div key={i}>{i} -
		    <Button name={i} onClick={l.view_ticker}>View ticker</Button>
		    <Button name={i} onClick={l.unsubscribe_ticker}>Unsubscribe ticker</Button>
		    <Button name={i} onClick={l.clear_ticker}>Clear ticker</Button>

		    <br/></div>);});
	return (<div>
		<h2>Ticker Control</h2>
		<a href="/ticker/get" target="_blank">Show ticker</a>
		<FormControl
		name="tickers"
		type="text"
		onChange={this.onChange}
		value={this.state.tickers_add}
		/><Button bsStyle="success" onClick={this.add_ticker}>Add Ticker</Button><br/>
		{items}<br/></div>);
    }
});
    
module.exports = TickerControl;
