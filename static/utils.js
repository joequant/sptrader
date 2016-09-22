function isNumber(obj) {
    return !isNaN(parseFloat(obj))
};

function formatNumber(n) {
    return n.toFixed(2).replace(/(\d)(?=(\d{3})+\.)/g, '$1,')
};

function renderNumber(params) {
    var x = params.data.value;
    if (isNumber(x)) {
	return formatNumber(x);
    } else {
	return x;
    }
};
module.exports.isNumber = isNumber;
module.exports.formatNumber = formatNumber;
module.exports.renderNumber = renderNumber;

