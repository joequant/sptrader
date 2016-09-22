import React from 'react';
import {AgGridReact} from 'ag-grid-react';
var OrderTable = React.createClass({
    getInitialState: function() {
	return {
	    columnDefs: [
		{headerName: "Orders",
		 field: "orders"},
		{headerName: "Id",
		 field: "id",
		 cellClass: "short-number-field"},
		{headerName: "Name",
		 field: "name"},
		{headerName: "OS BQty",
		 field: "osbqty",
		 cellClass: "short-number-field"},
		{headerName: "OS SQty",
		 field: "ossqty",
		 cellClass: "short-number-field"},
		{headerName: "Price",
		 field: "Price",
		 cellClass: "short-number-field"},
		{headerName: "Valid",
		 field: "ValidType",
		 cellClass: "short-number-field"},
		{headerName: "Cond.",
		 field: "CondType",
		 cellClass: "short-number-field"},
		{headerName: "Status",
		 field: "Status",
		 cellClass: "short-number-field"},
		{headerName: "Traded",
		 field: "TradedQty",
		 cellClass: "short-number-field"},
		{headerName: "Initiator",
		 field: "Initiator"},
		{headerName: "Ref",
		 field: "Ref"},
		{headerName: "T.Stam",
		 field: "UpdateTime"},
		{headerName: "Ext.Order#",
		 field: "ExtOrderNo",
		 cellClass: "short-number-field"}]
	};
    },
    render: function() {
	return (
	<AgGridReact
	    // column definitions and row data are immutable, the grid
	    // will update when these lists change
	    columnDefs={this.state.columnDefs}
	    rowData={this.props.data}
	/>
	)
    }
});
    
module.exports = OrderTable;
