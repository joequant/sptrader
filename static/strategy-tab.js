import React from 'react';
import {StrategyTable} from './tables/strategy-table';
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
		    return (<div key={s}><b>{s}</b><br/>
			    <StrategyTable
			    strategy={s}
			    columns={StrategyList.columns[s]}
			    status={status[s]}/></div>);
		})}
	    </div>);
    }
});

module.exports = StrategyTab;


