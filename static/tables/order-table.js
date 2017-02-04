import React from 'react';
import {Button} from 'react-bootstrap';
import {AgGridReact, reactCellRendererFactory} from 'ag-grid-react';
import {shortnumberwidth, renderNumber, renderDateTime,
       renderBuySell} from '../utils';


var OrderControl = React.createClass({
    post(url, data) {
	$.post(url, data);
    },
    delete() {
	var data = this.props.data;
	console.log(data);
	var d = {
	    'ClOrderId' : data.ClOrderId,
	    'IntOrderNo' : data.IntOrderNo,
	    'ProdCode' : data.ProdCode
	};
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
	var status = this.props.data.Status;
	var delete_disabled = true;
	var activate_disabled = true;
	var inactivate_disabled = true;
	if (status == 2) {
	    activate_disabled = false;
	    delete_disabled = false;
	}
	if (status == 3 || status == 8) {
	    inactivate_disabled = true;
	    delete_disabled = false;
	}
	    
	return (
	    <div>
		<Button onClick={this.delete}
	    disabled={delete_disabled}>Delete</Button>
		<Button onClick={this.activate}
	    disabled={activate_disabled}>Activate</Button>
		<Button onClick={this.inactivate}
	    disabled={inactivate_disabled}>Inactivate</Button>
		</div>
	);
    }
});

function renderStatus(params) {
    var x = params.value;
    if ( x == 0) {
	return "Sent";
    } else if ( x== 1) {
	return "Working";
    } else if ( x == 2 ) {
	return "Inactive";
    } else if ( x== 3 ) {
	return "Pending";
    } else if ( x == 4) {
	return "Adding";
    } else if ( x == 5 ) {
	return "Changing";
    } else if ( x == 6 ) {
	return "Deleting";
    } else if ( x == 7 ) {
	return "Inactivating";
    } else if ( x == 8) {
	return "Partially filled";
    } else if ( x == 9 ) {
	return "Filled";
    } else if ( x == 10) {
	return "Deleted";
    } else if ( x == 18 ) {
	return "Pending approval";
    } else {
	return x;
    }
}

export default class OrderTable extends React.Component {
    constructor(props) {
	super(props);
	this.state = {
	    columnDefs: [
		{headerName: "Ref",
		 field: "Ref"},
		{headerName: "Ref2",
		 field: "Ref2"},
		{headerName: "Product",
		 field: "ProdCode"},
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
		 width: shortnumberwidth,
		 cellRenderer: renderStatus},
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
		{headerName: "ClOrderId",
		 field: "ClOrderId"},
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
