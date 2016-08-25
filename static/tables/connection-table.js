import React from 'react';
import {AgGridReact} from 'ag-grid-react';
var ConnectionTable = React.createClass({
    getInitialState: function() {
	return {
	    columnDefs: [
		{headerName: "Link",
	     field: "link",
	     enableRowGroup: true, enablePivot: true,
	     width: 150, pinned: true},
	    {headerName: "Status",
	     field: "status",
	     enableRowGroup: true, enablePivot: true,
	     width: 150, pinned: true}
	    ],
	    rowData: [{link: "Transaction Link",
		       status: ''},
		      {link: "Price Link",
		      status: ''},
		      {link: "Long Depth Link",
		      status: ''},
		      {link: "Information Link",
		      status: ''}
		 ]
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
    
module.exports = ConnectionTable;
