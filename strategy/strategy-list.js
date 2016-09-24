import {reactCellRendererFactory} from 'ag-grid-react';
import {StrategyControl} from '../static/utils';

module.exports.StrategyList = {
    strategies : ["sample"],
    columns : {"sample":
	       [
		   {headerName: "Id",
		    field: "id"},
		   {headerName: "Status",
		    volatile: true,
		    field: "status"},
		   {headerName: "Product",
		    field: "product",
		    editable: true },
		   {headerName: "Parameter",
		    field: "param1",
		    editable: true },
		   {headerName: "Log",
		    field: "log",
		    cellRenderer: function(params) {
			return "<a href='/strategy/log/" +
			    params.data.strategy + "/" +
			    params.data.id + "' target='_blank'>Log</a>";
		    }},
		   {headerName: "Actions",
		    field: "start",
		    volatile: true,
		    cellRenderer: reactCellRendererFactory(StrategyControl)
		   }]}
}
