import React from 'react';
import {AgGridReact} from 'ag-grid-react';
import {Button} from 'react-bootstrap';
var SampleUi = React.createClass({
    getInitialState: function() {
	return {
	    counter:0,
	    columnDefs: [
		{headerName: "Id",
		 field: "id"},
		{headerName: "Product",
		 field: "product"},
		{headerName: "Log",
		 field: "log",
		 cellRenderer: function(params) {
		     return "<a href='/strategy/log/" +
			 params.data.id + "'>Log</a>";
		 }},
		{headerName: "operator",
		 field: "start",
		 cellRenderer: function(params) {
		     return "<Button>Start</Button>";
		 }
		}],
	    rowData: [{id:0, product: "a"}]
	};
    },
    // in onGridReady, store the api for later use
    onGridReady: function(params) {
	this.api = params.api;
	this.columnApi = params.columnApi;
    },
    addRow: function() {
	var r = this.state.rowData;
	var c = this.state.counter;
	c = c+1;
	r.push({id: c});
	this.setState({rowData: r,
		       counter: c});
	this.api.setRowData(r);
    },
    render: function() {
	return (
	    <div>
		<Button onClick={this.addRow}>Add Row</Button>
	<AgGridReact
	    // column definitions and row data are immutable, the grid
	    // will update when these lists change
	    columnDefs={this.state.columnDefs}
	    rowData={this.state.rowData}
	    onGridReady={this.onGridReady}
	    // or provide props the old way with no binding
	    rowSelection="multiple"
	    enableSorting="true"
	    enableFilter="true"
                   rowHeight="22"
		/></div>
	)
    }
});
    
module.exports = SampleUi;
