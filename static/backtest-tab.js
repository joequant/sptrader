import React from 'react';
import {BacktestTable} from './tables/backtest-table';

var BacktestTab = React.createClass( {
    getInitialState: function() {
	return null;
    },
    render: function() {
	var info = this.props.info;
	return (
		<div>
		{this.props.strategylist.map(function(s) {
		    return (<div key={s}><b>{s}</b><br/>
			    <BacktestTable
			    strategy={s}/></div>);
		})}
	    </div>);
    }
});

module.exports = BacktestTab;


