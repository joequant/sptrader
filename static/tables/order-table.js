import React from 'react';
import {AgGridReact} from 'ag-grid-react';
import {shortnumberwidth, renderNumber} from '../utils';

var OrderTable = React.createClass({
    getInitialState: function() {
	return {
	    columnDefs: [
		{headerName: "Orders",
		 field: "orders"},
		{headerName: "Id",
		 field: "id",
		 width: shortnumberwidth},
		{headerName: "Name",
		 field: "name"},
		{headerName: "OS BQty",
		 field: "osbqty",
		 width: shortnumberwidth},
		{headerName: "OS SQty",
		 field: "ossqty",
		 width: shortnumberwidth},
		{headerName: "Price",
		 field: "Price",
		 width: shortnumberwidth,
		 cellRenderer: renderNumber},
		{headerName: "Valid",
		 field: "ValidType",
		 width: shortnumberwidth},
		{headerName: "Cond.",
		 field: "CondType",
		 width: shortnumberwidth},
		{headerName: "Status",
		 field: "Status",
		 width: shortnumberwidth},
		{headerName: "Traded",
		 field: "TradedQty",
		 width: shortnumberwidth},
		{headerName: "Initiator",
		 field: "Initiator"},
		{headerName: "Ref",
		 field: "Ref"},
		{headerName: "T.Stam",
		 field: "UpdateTime"},
		{headerName: "Ext.Order#",
		 field: "ExtOrderNo",
		 width: shortnumberwidth}]
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
