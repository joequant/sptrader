import React from 'react';
import {Button, FormControl} from 'react-bootstrap';
import {AgGridReact} from 'ag-grid-react';

export default class TickerControl extends React.Component {
    constructor(props) {
	super(props);
	this.state = {
	    tickers_add: ''
	};
	this.onChange = this.onChange.bind(this);
	this.add_ticker = this.add_ticker.bind(this);
	this.clear_ticker = this.clear_ticker.bind(this);
	this.view_ticker = this.view_ticker.bind(this);
	this.unsubscribe_ticker = this.unsubscribe_ticker.bind(this);
    }
    onChange(e) {
	this.setState({tickers_add: e.target.value});
    }
    add_ticker(e) {
	$.get("/ticker/subscribe/" + this.state.tickers_add);
    }
    clear_ticker(e) {
	$.get("/ticker/clear/" + e.target.name);
    }
    view_ticker(e) {
	var myWindow = window.open("/ticker/view/" + e.target.name);
    }
    unsubscribe_ticker(e) {
	$.get("/ticker/unsubscribe/" + e.target.name);
    }
    render() {
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
}
