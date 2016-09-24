import React from 'react';
import {AgGridReact} from 'ag-grid-react';
import {isNumber, formatNumber, renderNumber, renderBuySell,
	shortnumberwidth, renderDate, renderTime} from '../utils';

var TradeTable = React.createClass({
    getInitialState: function() {
	return {
	    columnDefs: [
		{headerName: "Id",
		 field: "RecNo",
		 width: shortnumberwidth},
		{headerName: "Price",
		 field: "Price",
		 cellRenderer: renderNumber,
		 width: shortnumberwidth},
		{headerName: "TradeNo",
		 field: "TradeNo",
		 width: shortnumberwidth},
		{headerName: "ExtOrderNo",
		 field: "ExtOrderNo",
		 width: shortnumberwidth},
		{headerName: "IntOrderNo",
		 field: "IntOrderNo",
		 width: shortnumberwidth},
		{headerName: "Qty",
		 field: "Qty",
		 width: shortnumberwidth},
		{headerName: "TradeDate",
		 field: "TradeDate",
		 cellRenderer: renderDate
		},
		{headerName: "TradeTime",
		 field: "TradeTime",
		 cellRenderer: renderTime
		},
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
		 field: "BuySell",
		 cellRenderer: renderBuySell,
		},
		{headerName: "OpenClose",
		 field: "OpenClose"},
		{headerName: "Status",
		 field: "Status"},
		{headerName: "DecInPrice",
		 field: "DecInPrice"},
		{headerName: "OrderPrice",
		 field: "OrderPrice",
		 cellRenderer: renderNumber},
		{headerName: "TradeRef",
		 field: "TradeRef"},
		{headerName: "TotalQty",
		 field: "TotalQty",
		 width: shortnumberwidth},
		{headerName: "RemainingQty",
		 field: "RemainingQty",
		 width: shortnumberwidth},
		{headerName: "TradedQty",
		 field: "TradedQty",
		 width: shortnumberwidth},
		{headerName: "AvgTradedPrice",
		 field: "AvgTradedPrice",
		 width: shortnumberwidth,
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
