import React from 'react';
import {AgGridReact} from 'ag-grid-react';
import {Button} from 'react-bootstrap';


var StrategyTable = React.createClass({
    getInitialState() {
	return {
	    counter:0,
	    rowData: []
	};
    },
    // in onGridReady, store the api for later use
    componentWillReceiveProps(newprops) {
	if (newprops.status == undefined) {
	    return;
	}
	var r = this.state.rowData;
	for(var i=0; i < r.length; i++) {
	    if (newprops.status[r[i]['id']] != undefined) {
		r[i]['status'] = newprops.status[r[i]['id']];
	    }
	}
	this.setState({rowData: r});
	this.api.setRowData(r);
    },
    onGridReady(params) {
	this.api = params.api;
	this.columnApi = params.columnApi;
    },
    addRow() {
	var r = this.state.rowData;
	var c = this.state.counter;
	c = c+1;
	r.push({id: c,
		status: "stopped",
		strategy: this.props.strategy});
	this.setState({rowData: r,
		       counter: c});
	this.api.setRowData(r);
    },
    status() {
    },
    render() {
	return (
	    <div>
		<Button onClick={this.addRow}>Add Row</Button>
	<AgGridReact
	    // column definitions and row data are immutable, the grid
	    // will update when these lists change
	    columnDefs={this.props.columns}
	    rowData={this.state.rowData}
	    onGridReady={this.onGridReady}
		/></div>
	)
    }
});
    
module.exports.StrategyTable = StrategyTable;
