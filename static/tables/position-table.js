import React from 'react';
import {Button} from 'react-bootstrap';
import {AgGridReact, reactCellRendererFactory} from 'ag-grid-react';
import {renderChar, renderNumber} from '../utils';

var PositionControl = React.createClass({
    close() {
    },
    render() {
	return (
		<Button onClick={this.close}>Close</Button>
	);
    }
});

var PositionTable = React.createClass({
    getInitialState: function() {
	return {
	    columnDefs: [
		{headerName: "Name",
		 field: "ProdCode"},
		{headerName: "Qty",
		 field: "Qty"},
		{headerName: "DepQty",
		 field: "DepQty"},
		{headerName: "LongQty",
		 field: "LongQty"},
		{headerName: "ShortQty",
		 field: "ShortQty"},
		{headerName: "Net",
		 field: "TotalAmt",
		 cellRenderer: renderNumber},
		{headerName: "Day Long",
		 field: "LongTotalAmt",
		 cellRenderer: renderNumber},
		{headerName: "Day Short",
		 field: "ShortTotalAmt",
		 cellRenderer: renderNumber},
		{headerName: "Day Net",
		 field: "DepTotalAmt",
		 cellRenderer: renderNumber},
		{headerName: "P/L",
		 field: "PL",
		 cellRenderer: renderNumber},
		{headerName: "ExchangeRate",
		 field: "ExchangeRate"},
		{headerName: "P/L (Base Ccy)",
		 field: "PLBaseCcy",
		 cellRenderer: renderNumber},
		{headerName: "LongShort",
		 field: "LongShort",
		 cellRenderer: renderChar},
		{headerName: "Actions",
		 field: "action",
		 cellRenderer: reactCellRendererFactory(PositionControl)}
	    ]
	};
    },
    onGridReady(params) {
	this.api = params.api;
	this.columnApi = params.columnApi;
    },
    componentDidUpdate(prevprops, prevstate) {
	this.api.setRowData(this.props.data);
    },
    render: function() {
	return (
	<AgGridReact
	    // column definitions and row data are immutable, the grid
	    // will update when these lists change
	    columnDefs={this.state.columnDefs}
	    rowData={this.props.data}
	    onGridReady={this.onGridReady}
	/>)
    }
});
    
module.exports = PositionTable;
