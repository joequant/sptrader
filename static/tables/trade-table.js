import React from 'react';
import {AgGridReact} from 'ag-grid-react';
import {isNumber, formatNumber, renderNumber} from '../utils';

var TradeTable = React.createClass({
    getInitialState: function() {
	return {
	    columnDefs: [
		{headerName: "Id",
		 field: "RecNo",
		 cellClass: "short-number-field"},
		{headerName: "Price",
		 field: "Price",
		 cellRenderer: renderNumber,
		 cellClass: "short-number-field"},
		{headerName: "TradeNo",
		 field: "TradeNo"},
		{headerName: "ExtOrderNo",
		 field: "ExtOrderNo"},
		{headerName: "IntOrderNo",
		 field: "IntOrderNo"},
		{headerName: "Qty",
		 field: "Qty",
		 cellClass: "short-number-field"},
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
		 field: "TotalQty",
		 cellClass: "short-number-field"},
		{headerName: "RemainingQty",
		 field: "RemainingQty",
		 cellClass: "short-number-field"},
		{headerName: "TradedQty",
		 field: "TradedQty",
		 cellClass: "short-number-field"},
		{headerName: "AvgTradedPrice",
		 field: "AvgTradedPrice",
		 cellClass: "short-number-field",
		 cellRenderer: renderNumber}
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
