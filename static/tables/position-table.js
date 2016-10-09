import React from 'react';
import {AgGridReact} from 'ag-grid-react';
var PositionTable = React.createClass({
    getInitialState: function() {
	return {
	    columnDefs: [
		{headerName: "Qty",
		 field: "Qty"},
		{headerName: "Name",
		 field: "ProdCode"},
		{headerName: "In/Out",
		 field: "LongShort"},
		{headerName: "Day Long",
		 field: "LongTotalAmt"},
		{headerName: "Day Short",
		 field: "ShortTotalAmt"},
		{headerName: "Day Net",
		 field: "DepTotalAmt"},
		{headerName: "Net",
		 field: "TotalAmt"},
		{headerName: "P/L",
		 field: "PL"},
		{headerName: "ExchangeRate",
		 field: "ExchangeRate"},
		{headerName: "P/L (Base Ccy)",
		 field: "PLBaseCcy"}]
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
