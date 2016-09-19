import React from 'react';
import {AgGridReact} from 'ag-grid-react';
var OrderTable = React.createClass({
    getInitialState: function() {
	return {
	    columnDefs: [
		{headerName: "Orders",
		 field: "orders"},
		{headerName: "Id",
		 field: "id"},
		{headerName: "Name",
		 field: "name"},
		{headerName: "OS BQty",
		 field: "osbqty"},
		{headerName: "OS SQty",
		 field: "ossqty"},
		{headerName: "Price",
		 field: "Price"},
		{headerName: "Valid",
		 field: "ValidType"},
		{headerName: "Cond.",
		 field: "CondType"},
		{headerName: "Status",
		 field: "Status"},
		{headerName: "Traded",
		 field: "TradedQty"},
		{headerName: "Initiator",
		 field: "Initiator"},
		{headerName: "Ref",
		 field: "Ref"},
		{headerName: "T.Stam",
		 field: "UpdateTime"},
		{headerName: "Ext.Order#",
		 field: "ExtOrderNo"}]
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
