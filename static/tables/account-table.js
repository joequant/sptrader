import React from 'react';
import {AgGridReact} from 'ag-grid-react';
import {isNumber, formatNumber, renderNumber} from '../utils';

var AccountTable = React.createClass({
    getInitialState() {
	return {
	    columnDefs: [
		{headerName: "Name",
		 field: "name",
		 cellClass: ['cell-left']
		},
		{headerName: "Value",
		 field: "value",
		 cellRenderer: renderNumber}],
	    fields: []
	};
    },
    render() {
        var rowData = []
	if (this.props.data != undefined) {
	    for(var i=0, len=this.props.fields.length; i < len; i++) {
		var field_name = this.props.fields[i];
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
		/>
	)
    }
});

module.exports = AccountTable;
