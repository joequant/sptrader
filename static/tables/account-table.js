import React from 'react';
import {AgGridReact} from 'ag-grid-react';
var AccountTable = React.createClass({
    getInitialState: function() {
	return {
	    columnDefs: [
		{headerName: "Name",
		 field: "name",
		 enableRowGroup: true, enablePivot: true,
		 width: 150, pinned: true}],
	    rowData: [{name: "foobar"}]
	};
    },
    render: function() {
	return (
	<AgGridReact
	    // column definitions and row data are immutable, the grid
	    // will update when these lists change
	    columnDefs={this.state.columnDefs}
	    rowData={this.state.rowData}

	    // or provide props the old way with no binding
	    rowSelection="multiple"
	    enableSorting="true"
	    enableFilter="true"
                   rowHeight="22"
		/>
	)
    }
});
    
module.exports = AccountTable;
