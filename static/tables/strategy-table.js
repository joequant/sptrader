import React from 'react';
import {AgGridReact} from 'ag-grid-react';
import {Button} from 'react-bootstrap';
import {StrategyControl, renderLog, pad} from '../../static/utils';

class StrategyTable extends React.Component {
    constructor(props) {
	super(props);
	this.state = {
	    columnDefs: [],
	    rowData: [],
	    idList: new Set(),
	    defaultData: {}
	};
	this.onGridReady = this.onGridReady.bind(this);
	this.addRow = this.addRow.bind(this);
	this.removeRow = this.removeRow.bind(this);
    }
    addRow() {
	var r = Object.assign({}, this.state.defaultData);
	var c = this.state.idList;
	var rows = this.state.rowData;
	var i = 0;
	var id = undefined;
	do {
	    i += 1;
	    id = r.strategy + "-" + pad(i, 5);
	} while (c.has(id));
	r['id'] = id;
	this.state.rowData.push(r);
	this.state.idList.add(id);
	this.api.setRowData(rows);
    }
    removeRow(props) {
	console.log("remove row", props);
	props.api.removeItems([props.node]);
	this.state.rowData.splice(props.rowIndex, 1);
	this.state.idList.delete(props.data.id);
	$.get("/strategy/remove-row/" + props.data.id);
    }
    // in onGridReady, store the api for later use
    componentWillReceiveProps(newprops) {
	var l = this;
	if (newprops.info != undefined) {
	    var r = this.state.rowData;
	    for(var i=0; i < r.length; i++) {
		var newr = newprops.info[r[i]['id']];
		if (newr != undefined) {
		    for (var attrname in newr){
		    r[i][attrname] = newr[attrname];
		    }
		}
	    }
	    this.setState({rowData: r});
	    this.api.setRowData(r);
	}
	if (newprops.header != undefined) {
	    var d = newprops.header;
	    var start = [
		{headerName: "Id",
		 field: "id"},
		{headerName: "Status",
		 volatile: true,
		 field: "status"},
		{headerName: "Comment",
		 volatile: true,
		 field: "comment"},
		{headerName: "Instrument",
		 field: "dataname",
		 editable: true,
		 defaultData: ''}
	    ];
	    var end = [
		{headerName: "Log",
		 field: "log",
		 cellRenderer: renderLog},
		{headerName: "Actions",
		 field: "start",
		 cellRendererFramework: StrategyControl,
		 parent: l
		}];
	    for (var i=0; i < d.length; i++) {
		d[i]['editable'] = true;
		d[i]['volatile'] = true;
	    }
	    var items = start.concat(d).concat(end);
	    var defaultData = {};
	    for (var i=0; i < items.length; i++) {
		if (items[i].defaultData != undefined) {
		    defaultData[items[i].field] =
			items[i].defaultData;
		}
	    }
	    defaultData['status'] = 'stopped';
	    defaultData['strategy'] = l.props.strategy;
	    l.setState({columnDefs: items,
			defaultData: defaultData});
	}
	if (newprops.data != undefined) {
	    var d = newprops.data;
	    l.setState({rowData: d});
	    l.api.setRowData(d);
	}
    }
    onGridReady(params) {
	this.api = params.api;
	this.columnApi = params.columnApi;
    }
    render() {
	return (
	    <div>
		<Button onClick={this.addRow}>New Strategy</Button>
	<AgGridReact
	    // column definitions and row data are immutable, the grid
	    // will update when these lists change
	    columnDefs={this.state.columnDefs}
	    rowData={this.state.rowData}
	    onGridReady={this.onGridReady}
		/></div>
	)
    }
}
    
module.exports.StrategyTable = StrategyTable;
