import React from 'react';
import {AgGridReact} from 'ag-grid-react';
var TradeTable = React.createClass({
    getInitialState: function() {
	return {
	    columnDefs: [
		{headerName: "Id",
		 field: "RecNo"},
		{headerName: "Price",
		 field: "Price"},
		{headerName: "TradeNo",
		 field: "TradeNo"},
		{headerName: "ExtOrderNo",
		 field: "ExtOrderNo"},
		{headerName: "IntOrderNo",
		 field: "IntOrderNo"},
		{headerName: "Qty",
		 field: "Qty"},
		{headerName: "TradeDate",
		 field: "TradeDate"},
		{headerName: "TradeTime",
		 field: "TradeTime"},
		{headerName: "AccNo",
		 field: "AccNo"},
		{headerName: "ProdCode",
		 field: "ProdCode"},
		{headerName: "Initiator",
		 field: "Initiator"},
		{headerName: "Ref",
		 field: "Ref"},
		{headerName: "Ref2",
		 field: "Ref2"},
		{headerName: "GatewayCode",
		 field: "GatewayCode"},
		{headerName: "ClOrderId",
		 field: "ClOrderId"},
		{headerName: "BuySell",
		 field: "BuySell"},
		{headerName: "OpenClose",
		 field: "OpenClose"},
		{headerName: "Status",
		 field: "Status"},
		{headerName: "DecInPrice",
		 field: "DecInPrice"},
		{headerName: "OrderPrice",
		 field: "OrderPrice"},
		{headerName: "TradeRef",
		 field: "TradeRef"},
		{headerName: "TotalQty",
		 field: "TotalQty"},
		{headerName: "RemainingQty",
		 field: "RemainingQty"},
		{headerName: "TradedQty",
		 field: "TradedQty"},
		{headerName: "AvgTradedPrice",
		 field: "AvgTradedPrice"}
	    ]
	};
    },
    render: function() {
	return (
	<AgGridReact
	    // column definitions and row data are immutable, the grid
	    // will update when these lists change
	    columnDefs={this.state.columnDefs}
	    rowData={this.props.data}
        />)
    }
});
    
module.exports = TradeTable;
