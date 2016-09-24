import React from 'react';
import {StrategyTable} from '../strategy/strategy-table';
import {StrategyList} from '../strategy/strategy-list';

var StrategyTab = React.createClass( {
    getInitialState: function() {
	return {};
    },
    render: function() {
	var status = this.props.status;
	return (
		<div>
		{StrategyList.strategies.map(function(s) {
		    return (<div><b>{s}</b><br/>
			    <StrategyTable
			    strategy={s}
			    columns={StrategyList.columns[s]}
			    status={status[s]}/></div>);
		})}
	    </div>);
/*	for(var i=0; i < StrategyList.length; i++) {
	    var strategy = StrategyList.strategies[i];
	    retval = retval + (<StrategyTable
			       strategy={strategy}
			       columns={StrategyList.columns[strategy]}
			       status={this.props.status[strategy]}/>);

	}
	console.log(retval);
	return retval; */
    }
});

module.exports = StrategyTab;


