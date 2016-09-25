import React from 'react';
import {StrategyTable} from './tables/strategy-table';

var StrategyTab = React.createClass( {
    getInitialState: function() {
	var l = this;
	$.getJSON("/strategy/list", function(d) {
	    l.setState({'strategylist':d});
	});
	return {'strategylist': []};
    },
    render: function() {
	var info = this.props.info;
	return (
		<div>
		{this.state.strategylist.map(function(s) {
		    return (<div key={s}><b>{s}</b><br/>
			    <StrategyTable
			    strategy={s}
			    info={info[s]}/></div>);
		})}
	    </div>);
    }
});

module.exports = StrategyTab;


