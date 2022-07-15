odoo.define('consistence.dashboard', function (require) {
"use strict";

var core = require('web.core');
var ListController = require('web.ListController');
var ListModel = require('web.ListModel');
var ListRenderer = require('web.ListRenderer');
var ListView = require('web.ListView');
var KanbanController = require('web.KanbanController');
var KanbanModel = require('web.KanbanModel');
var KanbanRenderer = require('web.KanbanRenderer');
var KanbanView = require('web.KanbanView');

var PivotController = require('web.PivotController');
var PivotModel = require('web.PivotModel');
var PivotRenderer = require('web.PivotRenderer');
var PivotView = require('web.PivotView');
var SampleServer = require('web.SampleServer');
var view_registry = require('web.view_registry');
const patchMixin = require('web.patchMixin');

var QWeb = core.qweb;

// Add mock of method 'retrieve_dashboard' in SampleServer, so that we can have
// the sample data in empty purchase kanban and list view
let dashboardValues;
SampleServer.mockRegistry.add('price.consistence/retrieve_dashboard', () => {
    return Object.assign({}, dashboardValues);
});

//--------------------------------------------------------------------------
// List View
//--------------------------------------------------------------------------

var ConsistenceListDashboardRenderer = ListRenderer.extend({
    events:_.extend({}, ListRenderer.prototype.events, {
        'click .o_dashboard_action': '_onDashboardActionClicked',
    }),
    /**
     * @override
     * @private
     * @returns {Promise}
     */
    _renderView: function () {
        var self = this;
        return this._super.apply(this, arguments).then(function () {
            var values = self.state.dashboardValues;
            var consistence_dashboard = QWeb.render('consistence.ConsistenceDashboard', {
                values: values,
            });
            self.$el.prepend(consistence_dashboard);
        });
    },

    /**
     * @private
     * @param {MouseEvent}
     */
    _onDashboardActionClicked: function (e) {
        e.preventDefault();
        var $action = $(e.currentTarget);
        this.trigger_up('dashboard_open_action', {
            action_name: $action.attr('name')+"_list",
            action_context: $action.attr('context'),
        });
    },
});

var  ConsistenceListDashboardModel = ListModel.extend({

    init: function () {
        this.dashboardValues = {};
        this._super.apply(this, arguments);
    },

    __get: function (localID) {
        var result = this._super.apply(this, arguments);
        if (_.isObject(result)) {
            result.dashboardValues = this.dashboardValues[localID];
        }
        return result;
    },

    __load: function () {
        return this._loadDashboard(this._super.apply(this, arguments));
    },

    __reload: function () {
        return this._loadDashboard(this._super.apply(this, arguments));
    },

    _loadDashboard: function (super_def) {
        var self = this;
        var dashboard_def = this._rpc({
            model: 'price.consistence',
            method: 'retrieve_dashboard',
        });
        return Promise.all([super_def, dashboard_def]).then(function(results) {
            var id = results[0];
            dashboardValues = results[1];
            self.dashboardValues[id] = dashboardValues;
            return id;
        });
    },
});

var  ConsistenceListDashboardController = ListController.extend({
    custom_events: _.extend({}, ListController.prototype.custom_events, {
        dashboard_open_action: '_onDashboardOpenAction',
    }),

    /**
     * @private
     * @param {OdooEvent} e
     */
    _onDashboardOpenAction: function (e) {
        return this.do_action(e.data.action_name,
            {additional_context: JSON.parse(e.data.action_context)});
    },
});

var ConsistenceListDashboardView = ListView.extend({
    config: _.extend({}, ListView.prototype.config, {
        Model: ConsistenceListDashboardModel,
        Renderer: ConsistenceListDashboardRenderer,
        Controller: ConsistenceListDashboardController,
    }),
});

//--------------------------------------------------------------------------
// Kanban View
//--------------------------------------------------------------------------

var ConsistenceKanbanDashboardRenderer = KanbanRenderer.extend({
    events:_.extend({}, KanbanRenderer.prototype.events, {
        'click .o_dashboard_action': '_onDashboardActionClicked',
    }),
    /**
     * @override
     * @private
     * @returns {Promise}
     */
    _render: function () {
        var self = this;
        return this._super.apply(this, arguments).then(function () {
            var values = self.state.dashboardValues;
            var consistence_dashboard = QWeb.render('consistence.ConsistenceDashboard', {
                values: values,
            });
            self.$el.parent().find(".o_consistence_dashboard").remove();
            self.$el.before(consistence_dashboard);
        });
    },

    /**
     * @private
     * @param {MouseEvent}
     */
    _onDashboardActionClicked: function (e) {
        e.preventDefault();
        var $action = $(e.currentTarget);
        this.trigger_up('dashboard_open_action', {
            action_name: $action.attr('name')+"_kanban",
            action_context: $action.attr('context'),
        });
    },
});

var ConsistenceKanbanDashboardModel = KanbanModel.extend({
    /**
     * @override
     */
    init: function () {
        this.dashboardValues = {};
        this._super.apply(this, arguments);
    },

    /**
     * @override
     */
    __get: function (localID) {
        var result = this._super.apply(this, arguments);
        if (_.isObject(result)) {
            result.dashboardValues = this.dashboardValues[localID];
        }
        return result;
    },
    /**
     * @override
     * @returns {Promise}
     */
    __load: function () {
        return this._loadDashboard(this._super.apply(this, arguments));
    },
    /**
     * @override
     * @returns {Promise}
     */
    __reload: function () {
        return this._loadDashboard(this._super.apply(this, arguments));
    },

    /**
     * @private
     * @param {Promise} super_def a promise that resolves with a dataPoint id
     * @returns {Promise -> string} resolves to the dataPoint id
     */
    _loadDashboard: function (super_def) {
        var self = this;
        var dashboard_def = this._rpc({
            model: 'price.consistence',
            method: 'retrieve_dashboard',
        });
        return Promise.all([super_def, dashboard_def]).then(function(results) {
            var id = results[0];
            dashboardValues = results[1];
            self.dashboardValues[id] = dashboardValues;
            return id;
        });
    },
});

var ConsistenceKanbanDashboardController = KanbanController.extend({
    custom_events: _.extend({}, KanbanController.prototype.custom_events, {
        dashboard_open_action: '_onDashboardOpenAction',
    }),

    /**
     * @private
     * @param {OdooEvent} e
     */
    _onDashboardOpenAction: function (e) {
        return this.do_action(e.data.action_name,
            {additional_context: JSON.parse(e.data.action_context)});
    },
});

var ConsistenceKanbanDashboardView = KanbanView.extend({
    config: _.extend({}, KanbanView.prototype.config, {
        Model: ConsistenceKanbanDashboardModel,
        Renderer: ConsistenceKanbanDashboardRenderer,
        Controller: ConsistenceKanbanDashboardController,
    }),
});
//
//
//
//class ConsistencePivotDashboardRenderer extends PivotRenderer{
////    events:_.extend({}, PivotRenderer.prototype.events, {
////        'click .o_dashboard_action': '_onDashboardActionClicked',
////    }),
//    /**
//     * @override
//     * @private
//     * @returns {Promise}
//     */
////    render () {
////        var self = this;
////        return this._super.apply(this, arguments).then(function () {
////            var values = self.state.dashboardValues;
////            var consistence_dashboard = QWeb.render('consistence.ConsistenceDashboard', {
////                values: values,
////            });
////            self.$el.parent().find(".o_consistence_dashboard").remove();
////            self.$el.before(consistence_dashboard);
////        });
////    }
//
//    /**
//     * @private
//     * @param {MouseEvent}
//     */
//    _onDashboardActionClicked(e) {
//        e.preventDefault();
//        var $action = $(e.currentTarget);
//        this.trigger_up('dashboard_open_action', {
//            action_name: $action.attr('name')+"_pivot",
//            action_context: $action.attr('context'),
//        });
//    }
//};
//
//var ConsistencePivotDashboardModel = PivotModel.extend({
//    /**
//     * @override
//     */
//    init: function () {
//        this.dashboardValues = {};
//        this._super.apply(this, arguments);
//    },
//
//    /**
//     * @override
//     */
//    __get: function (localID) {
//        var result = this._super.apply(this, arguments);
//        if (_.isObject(result)) {
//            result.dashboardValues = this.dashboardValues[localID];
//        }
//        return result;
//    },
//    /**
//     * @override
//     * @returns {Promise}
//     */
//    __load: function () {
//        return this._loadDashboard(this._super.apply(this, arguments));
//    },
//    /**
//     * @override
//     * @returns {Promise}
//     */
//    __reload: function () {
//        return this._loadDashboard(this._super.apply(this, arguments));
//    },
//
//    /**
//     * @private
//     * @param {Promise} super_def a promise that resolves with a dataPoint id
//     * @returns {Promise -> string} resolves to the dataPoint id
//     */
//    _loadDashboard: function (super_def) {
//        var self = this;
//        var dashboard_def = this._rpc({
//            model: 'price.consistence',
//            method: 'retrieve_dashboard',
//        });
//        return Promise.all([super_def, dashboard_def]).then(function(results) {
//            var id = results[0];
//            dashboardValues = results[1];
//            self.dashboardValues[id] = dashboardValues;
//            return id;
//        });
//    },
//});
//
//var ConsistencePivotDashboardController = PivotController.extend({
//    custom_events: _.extend({}, PivotController.prototype.custom_events, {
//        dashboard_open_action: '_onDashboardOpenAction',
//    }),
//
//    /**
//     * @private
//     * @param {OdooEvent} e
//     */
//    _onDashboardOpenAction: function (e) {
//        return this.do_action(e.data.action_name,
//            {additional_context: JSON.parse(e.data.action_context)});
//    },
//});
//
//var ConsistencePivotDashboardView = PivotView.extend({
//    config: _.extend({}, PivotView.prototype.config, {
//        Model: ConsistencePivotDashboardModel,
//        Renderer: ConsistencePivotDashboardRenderer,
//        Controller: ConsistencePivotDashboardController,
//    }),
//});


view_registry.add('consistence_list_dashboard', ConsistenceListDashboardView);
view_registry.add('consistence_kanban_dashboard', ConsistenceKanbanDashboardView);
//view_registry.add('consistence_pivot_dashboard', ConsistencePivotDashboardView);
//
return {
    ConsistenceListDashboardModel: ConsistenceListDashboardModel,
    ConsistenceListDashboardRenderer: ConsistenceListDashboardRenderer,
    ConsistenceListDashboardController: ConsistenceListDashboardController,
    ConsistenceKanbanDashboardModel: ConsistenceKanbanDashboardModel,
    ConsistenceKanbanDashboardRenderer:ConsistenceKanbanDashboardRenderer,
    ConsistenceKanbanDashboardController: ConsistenceKanbanDashboardController,

//    ConsistencePivotDashboardModel: ConsistencePivotDashboardModel,
// ConsistencePivotDashboardRenderer:ConsistencePivotDashboardRenderer,
//    ConsistencePivotDashboardController: ConsistencePivotDashboardController
};

});
