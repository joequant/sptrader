import React from 'react';
import {AgGridReact} from 'ag-grid-react';
var TradeTable = React.createClass({
    getInitialState: function() {
	return {
	    columnDefs: [
		{headerName: "Id",
		 field: "RecNo"},
		{headerName: "Name",
		 field: "ProdCode"},
		{headerName: "Time",
		 field: "TradeTime"}
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
