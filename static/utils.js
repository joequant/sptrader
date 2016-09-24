function isNumber(obj) {
    return !isNaN(parseFloat(obj))
};

function formatNumber(n, d) {
    return Number(n).toFixed(2).replace(/(\d)(?=(\d{3})+\.)/g, '$1,')
};

function renderNumber(params) {
    var x = params.value;
    if (isNumber(x)) {
	return formatNumber(x, 2);
    } else {
	return x;
    }
};

function renderBuySell(params) {
    var x = params.value;
    if (x == 66) {
	return "Buy";
    } else if (x == 83) {
	return "Sell";
    } else {
	return x;
    }
};


function zeroPad(num, places) {
    var zero = places - num.toString().length + 1;
    return Array(+(zero > 0 && zero)).join("0") + num;
}
function renderDateTime(params) {
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

function renderDate(params) {
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

function renderTime(params) {
    var x = parseInt(params.value);
    var a = new Date(x * 1000);
    var hour = zeroPad(a.getHours(), 2);
    var min = zeroPad(a.getMinutes(), 2);
    var sec = zeroPad(a.getSeconds(), 2);
    var time = hour + ':' + min + ':' + sec ;
    return time;
};


module.exports.isNumber = isNumber;
module.exports.formatNumber = formatNumber;
module.exports.renderNumber = renderNumber;
module.exports.shortnumberwidth = 100;
module.exports.renderDateTime = renderDateTime;
module.exports.renderDate = renderDate;
module.exports.renderTime = renderTime;
module.exports.renderBuySell = renderBuySell;
