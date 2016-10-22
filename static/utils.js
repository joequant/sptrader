import React from 'react';
import {Button,Checkbox,FormControl,FormGroup,Form} from 'react-bootstrap';

export class StrategyControl extends React.Component {
    constructor(props) {
	super(props);
	this.start = this.start.bind(this);
	this.stop = this.stop.bind(this);
	this.removeRow = this.removeRow.bind(this);
    }
    post(url, data) {
	$.post(url, data);
    }
    start() {
	var data = this.props.data;
	this.post("/strategy/start", data);
    }
    stop() {
	var data = this.props.data;
	this.post("/strategy/stop", data);
    }
    removeRow() {
	this.props.colDef.parent.removeRow(this.props);
    }
    render() {
	var status = this.props.data.status;
	var start_disabled = true;
	var pause_disabled = true;
	var stop_disabled = true;
	var remove_row_disabled = true;
	if (status == undefined || status == "stopped"
	    || status == "error" || status == "done") {
	    start_disabled = false;
	    remove_row_disabled = false;
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
		<Button onClick={this.stop}
	    disabled={stop_disabled}>Stop</Button>
		<Button onClick={this.removeRow}
	    disabled={remove_row_disabled}>Remove row</Button>
		</div>
	);
    }
}

export class BacktestControl extends React.Component {
    constructor(props) {
	super(props);
	this.backtest = this.backtest.bind(this);
	this.removeRow = this.removeRow.bind(this);
    }

    post(url, data) {
	var myWindow = window.open("", "Backtest " + Date.now().toString());
	myWindow.document.open();
	myWindow.document.write("<img src='/static/loading_anim.gif' width='20' height='20' />Generating backtest");
	myWindow.document.close();
	$.post(url, data, function(data) {
		myWindow.document.open();
		myWindow.document.write(data);
		myWindow.document.close();
	});
    }
    
    backtest() {
	var data = this.props.data;
	this.post("/backtest", data);
    }
    removeRow() {
	this.props.colDef.parent.removeRow(this.props);
    }
    render() {
	return (
	    <div>
		<Button onClick={this.backtest}>Backtest</Button>
		<Button onClick={this.removeRow}>Remove row</Button>
	    </div>
	);
    }
}



export function isNumber(obj) {
    return !isNaN(parseFloat(obj))
};

export function formatNumber(n, d) {
    return Number(n).toFixed(2).replace(/(\d)(?=(\d{3})+\.)/g, '$1,')
};

export function renderNumber(params) {
    var x = params.value;
    if (isNumber(x)) {
	return formatNumber(x, 2);
    } else {
	return x;
    }
};

export function renderBuySell(params) {
    var x = params.value;
    if (x == 66) {
	return "Buy";
    } else if (x == 83) {
	return "Sell";
    } else {
	return x;
    }
};

export function renderChar(params) {
    var x = params.value;
    return String.fromCharCode(x);
};


function zeroPad(num, places) {
    var zero = places - num.toString().length + 1;
    return Array(+(zero > 0 && zero)).join("0") + num;
}

export function renderDateTime(params) {
    var x = parseInt(params.value);
    var a = new Date(x * 1000);
    var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    var wday = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    var year = a.getFullYear();
    var month = months[a.getMonth()];
    var wdaystr = wday[a.getDay()]; 
    var date = zeroPad(a.getDate(), 2);
    var hour = zeroPad(a.getHours(), 2);
    var min = zeroPad(a.getMinutes(), 2);
    var sec = zeroPad(a.getSeconds(), 2);
    var time = wdaystr + ' ' + date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec ;
    return time;
};

export function renderDate(params) {
    var x = parseInt(params.value);
    var a = new Date(x * 1000);
    var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    var wday = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    var wdaystr = wday[a.getDay()]; 
    var year = a.getFullYear();
    var month = months[a.getMonth()];
    var date = zeroPad(a.getDate(), 2);
    var time = wdaystr + ' ' + date + ' ' + month + ' ' + year;
    return time;
};

export function renderTime(params) {
    var x = parseInt(params.value);
    var a = new Date(x * 1000);
    var hour = zeroPad(a.getHours(), 2);
    var min = zeroPad(a.getMinutes(), 2);
    var sec = zeroPad(a.getSeconds(), 2);
    var time = hour + ':' + min + ':' + sec ;
    return time;
};


export function renderLog(params) {
    return "<a href='/strategy/log/" +
	params.data.id + "' target='_blank'>Log</a>";
};

export function pad(num, size) {
    var s = num+"";
    while (s.length < size) s = "0" + s;
    return s;
}

export function process_headers(l, start, finish, d, default_columns) {
    for (var i=0; i < d.length; i++) {
	d[i]['editable'] = true;
	d[i]['volatile'] = true;
	if ("select" in d[i]) {
	    d[i]['cellEditor'] = 'select';
	    d[i]['cellEditorParams'] = {
		values: d[i]['select']
	    }
	}
    }
    var items = start.concat(d).concat(finish);
    var defaultData = default_columns;
    for (var i=0; i < items.length; i++) {
	if (items[i].defaultData != undefined) {
	    defaultData[items[i].field] =
		items[i].defaultData;
	}
    }
    l.setState({columnDefs: items,
		defaultData: defaultData});
}

export var shortnumberwidth = 100;





