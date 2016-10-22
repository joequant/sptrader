import React from 'react';
import {BacktestTable} from './tables/backtest-table';

export default class BacktestTab extends React.Component {
    render() {
	var l = this;
	return (
		<div>
		{this.props.strategylist.map(function(s) {
		    return (<div key={s}><b>{s}</b><br/>
			    <BacktestTable
			    strategy={s}
			    data={l.props.data[s]}
			    header={l.props.headers[s]}
			    /></div>);
		})}
	    </div>);
    }
}


