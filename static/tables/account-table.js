import React from 'react';
import {AgGridReact} from 'ag-grid-react';
var AccountTable = React.createClass({
    getInitialState: function() {
	var l = this;
	$.getJSON("/schema/SPApiAccInfo", function(d) {
	    l.setState({fields: d.retval});
	});
	return {
	    columnDefs: [
		{headerName: "Name",
		 field: "name"},
		{headerName: "Value",
		 field: "value",
		 cellClass: ['cell-right']}],
	    fields: []
	};
    },
    render: function() {
        var rowData = []
	if (this.props.data != undefined) {
	    for(var i=0, len=this.state.fields.length; i < len; i++) {
		var field_name = this.state.fields[i];
		rowData.push({name: field_name,
			      value: this.props.data[field_name]})
	    }
	}

	return (
	<AgGridReact
	    // column definitions and row data are immutable, the grid
	    // will update when these lists change
	    columnDefs={this.state.columnDefs}
	    rowData={rowData}

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
