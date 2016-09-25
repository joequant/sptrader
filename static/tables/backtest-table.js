import React from 'react';
import {AgGridReact, reactCellRendererFactory} from 'ag-grid-react';
import {Button} from 'react-bootstrap';
import {StrategyControl, renderLog} from '../../static/utils';

var BacktestTable = React.createClass({
    getInitialState() {
	var l = this;
	$.getJSON("/strategy/headers/" + l.props.strategy,
		  function(d) {
		      var start = [
			  {headerName: "Instrument",
			   field: "dataname",
			   editable: true,
			   defaultData: ''}
		      ];
		      var end = [
			  {headerName: "Log",
			   field: "log",
			   cellRenderer: renderLog}];
		      for (var i=0; i < d.length; i++) {
			  d[i]['editable'] = true;
		      }
		      var items = start.concat(d).concat(end);
		      var defaultData = {};
		      for (var i=0; i < items.length; i++) {
			  if (items[i].defaultData != undefined) {
			      defaultData[items[i].field] =
				  items[i].defaultData;
			  }
		      }
		      defaultData['strategy'] = l.props.strategy;
		      l.setState({columnDefs: items,
				  defaultData: defaultData});
		  });
	return {
	    columnDefs: [],
	    rowData: [],
	    defaultData: {}
	};
    },
    // in onGridReady, store the api for later use
    componentWillReceiveProps(newprops) {
    },
    onGridReady(params) {
	this.api = params.api;
	this.columnApi = params.columnApi;
    },
    addRow() {
	var r = this.state.defaultData;
	var rows = this.state.rowData;
	rows.push(r);
	this.setState({rowData: rows});
	this.api.setRowData(rows);
    },
    status() {
    },
    render() {
	return (
	    <div>
		<Button onClick={this.addRow}>Add Row</Button>
	<AgGridReact
	    // column definitions and row data are immutable, the grid
	    // will update when these lists change
	    columnDefs={this.state.columnDefs}
	    rowData={this.state.rowData}
	    onGridReady={this.onGridReady}
		/></div>
	)
    }
});
    
module.exports.BacktestTable = BacktestTable;
