import React from 'react';
import {AgGridReact, reactCellRendererFactory} from 'ag-grid-react';
import {Button} from 'react-bootstrap';

var StrategyControl = React.createClass({
    post(url, data) {
	$.ajax({
	    type: 'post',
	    url: url,
	    data: JSON.stringify(data),
	    contentType: "application/json"
	});
    },
    start() {
	var data = this.props.params.data;
	this.post("/strategy/start", data);
    },
    pause() {
	var data = this.props.params.data;
	this.post("/strategy/pause", data);
    },
    stop() {
	var data = this.props.params.data;
	this.post("/strategy/stop", data);
    },
    render() {
	var status = this.props.params.data.status;
	var start_disabled = true;
	var pause_disabled = true;
	var stop_disabled = true;
	console.log(this.props.params);
	if (status == undefined || status == "stopped" || status == "error") {
	    start_disabled = false;
	} else if (status == "paused") {
	    start_disabled = false;
	} else if (status == "running") {
	    pause_disabled = false;
	    stop_disabled = false;
	}
	return (
		<div>
		<Button onClick={this.start}
	    disabled={start_disabled}>Start</Button>
		<Button onClick={this.pause}
	    disabled={pause_disabled}>Pause</Button>
		<Button onClick={this.stop}
	    disabled={stop_disabled}>Stop</Button>
		</div>
	);
    }
});

var SampleUi = React.createClass({
    getInitialState() {
	return {
	    counter:0,
	    columnDefs: [
		{headerName: "Id",
		 field: "id"},
		{headerName: "Status",
		 volatile: true,
		 field: "status"},
		{headerName: "Product",
		 field: "product",
		 editable: true },
		{headerName: "Parameter",
		 field: "param1",
		 editable: true },
		{headerName: "Log",
		 field: "log",
		 cellRenderer: function(params) {
		     return "<a href='/strategy/log/" +
			 params.data.strategy + "/" +
			 params.data.id + "' target='_blank'>Log</a>";
		 }},
		{headerName: "Actions",
		 field: "start",
		 volatile: true,
		 cellRenderer: reactCellRendererFactory(StrategyControl)
		}],
	    rowData: []
	};
    },
    // in onGridReady, store the api for later use
    componentWillReceiveProps(newprops) {
	if (newprops.status['sample'] == undefined) {
	    return;
	}
	var r = this.state.rowData;
	console.log(r);
	console.log(newprops.status['sample']);
	for(var i=0; i < r.length; i++) {
	    if (newprops.status['sample'][r[i]['id']] != undefined) {
		r[i]['status'] = newprops.status['sample'][r[i]['id']];
	    }
	}
	this.setState({rowData: r});
	this.api.setRowData(r);
	this.api.softRefresh();
    },
    onGridReady(params) {
	this.api = params.api;
	this.columnApi = params.columnApi;
    },
    addRow() {
	var r = this.state.rowData;
	var c = this.state.counter;
	c = c+1;
	r.push({id: c,
		status: "stopped",
		strategy: "sample"});
	this.setState({rowData: r,
		       counter: c});
	this.api.setRowData(r);
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
    
module.exports = SampleUi;
