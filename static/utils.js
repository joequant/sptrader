function isNumber(obj) {
    return !isNaN(parseFloat(obj))
};

function formatNumber(n) {
    return Number(n).toFixed(2).replace(/(\d)(?=(\d{3})+\.)/g, '$1,')
};

function renderNumber(params) {
    var x = params.data.value;
    if (isNumber(x)) {
	return formatNumber(x);
    } else {
	return x;
    }
};

function renderBuySell(params) {
    var x = params.data.value;
    if (x == 66) {
	return "Buy";
    } else if (x == 83) {
	return "Sell";
    } else {
	return x;
    }
};
module.exports.isNumber = isNumber;
module.exports.formatNumber = formatNumber;
module.exports.renderNumber = renderNumber;
module.exports.shortnumberwidth = 100;
