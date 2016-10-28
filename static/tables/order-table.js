import React from 'react';
import {Button} from 'react-bootstrap';
import {AgGridReact, reactCellRendererFactory} from 'ag-grid-react';
import {shortnumberwidth, renderNumber, renderDateTime,
       renderBuySell} from '../utils';


var OrderControl = React.createClass({
    post(url, data) {
    },
    cancel() {
	var data = this.props.data;
	console.log(this.props);
	var d = {}
	d['clOrderId'] = data.clOrderId;
	d['IntOrderNo'] = data.IntOrderNo;
	this.post("/order/delete", d);
    },
    activate() {
	var data = this.props.data;
	console.log(this.props);
	var d = {}
	d['IntOrderNo'] = data.IntOrderNo;
	this.post("/order/activate", d);
    },
    inactivate() {
	var data = this.props.data;
	console.log(this.props);
	var d = {}
	d['IntOrderNo'] = data.IntOrderNo;
	this.post("/order/inactivate", d);
    },
    render() {
	return (
	    <div>
		<Button onClick={this.cancel}>Cancel</Button>
		<Button onClick={this.activate}>Activate</Button>
		<Button onClick={this.inactivate}>Inactivate</Button>
		</div>
	);
    }
});

export default class OrderTable extends React.Component {
    constructor(props) {
	super(props);
	this.state = {
	    columnDefs: [
		{headerName: "Ref",
		 field: "Ref"},
		{headerName: "Ref2",
		 field: "Ref2"},
		{headerName: "Price",
		 field: "Price",
		 width: shortnumberwidth,
		 cellRenderer: renderNumber},
		{headerName: "AccNo",
		 field: "AccNo",
		 width: shortnumberwidth},
		{headerName: "BuySell",
		 field: "BuySell",
		 width: shortnumberwidth,
		 cellRenderer: renderBuySell},
		{headerName: "StopType",
		 field: "StopType",
		 width: shortnumberwidth},
		{headerName: "OpenClose",
		 field: "OpenClose",
		 width: shortnumberwidth},
		{headerName: "Valid",
		 field: "ValidType",
		 width: shortnumberwidth},
		{headerName: "Cond.",
		 field: "CondType",
		 width: shortnumberwidth},
		{headerName: "Status",
		 field: "Status",
		 width: shortnumberwidth},
		{headerName: "Traded",
		 field: "TradedQty",
		 width: shortnumberwidth},
		{headerName: "TotalQty",
		 field: "TotalQty",
		 width: shortnumberwidth},
		{headerName: "Initiator",
		 field: "Initiator"},
		{headerName: "T.Stam",
		 field: "TimeStamp",
		 cellRenderer: renderDateTime
		},
		{headerName: "Ext.Order#",
		 field: "ExtOrderNo",
		 width: shortnumberwidth},
		{headerName: "Int.Order#",
		 field: "IntOrderNo",
		 width: shortnumberwidth},
		{headerName: "Actions",
		 field: "action",
		 cellRenderer: reactCellRendererFactory(OrderControl)}
	    ]
	};
	this.onGridReady = this.onGridReady.bind(this);
    }
    onGridReady(params) {
	this.api = params.api;
	this.columnApi = params.columnApi;
    }
    componentDidUpdate(prevprops, prevstate) {
	this.api.setRowData(this.props.data);
    }
    render() {
	return (
	<AgGridReact
	    // column definitions and row data are immutable, the grid
	    // will update when these lists change
	    columnDefs={this.state.columnDefs}
	    rowData={this.props.data}
	    onGridReady={this.onGridReady}
	/>
	)
    }
}
