import React from 'react';
import {AgGridReact} from 'ag-grid-react';
export default class SampleTable extends React.Component {
    constructor(props) {
	super(props);
	this.state = {
	    columnDefs: [
		{headerName: "Name",
		 field: "name",
		 enableRowGroup: true, enablePivot: true,
		 width: 150, pinned: true}],
	    rowData: [{name: "foobar"}]
	};
    }
    render() {
	return (
	<AgGridReact
	    columnDefs={this.state.columnDefs}
	    rowData={this.state.rowData}
		/>
	)
    }
}
