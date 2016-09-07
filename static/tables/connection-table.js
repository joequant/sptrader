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
	     width: 150, pinned: true,
	     cellRenderer: function(params) {
		 if (params.data.status == undefined) {
		     return "";
		 };
		 var status = ["In progress",
			       "Established",
			       "Error",
			       "Failed"];
		 return status[params.data.status-1];
	     }
	    }
	   ],
	    ports: [80, 83, 88],
	    titles: {80: "Transaction Link",
		     83: "Long Depth Link",
		     88: "Information Link"}
	};
    },
    render: function() {
	var rowData = [];
	var ports = this.state.ports;
	for (var i=0, length=ports.length; i < length; i++) {
	    rowData.push({link: this.state.titles[ports[i]],
			  status: this.props.data[ports[i]]})
	};
	return (
		<AgGridReact
	    // column definitions and row data are immutable, the grid
	    // will update when these lists change
	    columnDefs={this.state.columnDefs}
	    rowData={rowData}
		/>
	)
    }
});
    
module.exports = ConnectionTable;
