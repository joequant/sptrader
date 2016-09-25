import React from 'react';
import {StrategyTable} from './tables/strategy-table';

var StrategyTab = React.createClass( {
    getInitialState: function() {
	return null;
    },
    render: function() {
	var info = this.props.info;
	return (
		<div>
		{this.props.strategylist.map(function(s) {
		    return (<div key={s}><b>{s}</b><br/>
			    <StrategyTable
			    strategy={s}
			    info={info[s]}/></div>);
		})}
	    </div>);
    }
});

module.exports = StrategyTab;


