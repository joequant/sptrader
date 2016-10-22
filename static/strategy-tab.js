import React from 'react';
import {StrategyTable} from './tables/strategy-table';

export default class StrategyTab extends React.Component {
    render() {
	var info = this.props.info;
	var l = this;
	return (
		<div>
		{this.props.strategylist.map(function(s) {
		    return (<div key={s}><b>{s}</b><br/>
			    <StrategyTable
			    strategy={s}
			    data={l.props.data[s]}
			    header={l.props.headers[s]}
			    info={info[s]}/></div>);
		})}
	    </div>);
    }
}


