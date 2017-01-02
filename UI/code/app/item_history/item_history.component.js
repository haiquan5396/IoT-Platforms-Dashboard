"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
require("rxjs/add/operator/switchMap");
var core_1 = require("@angular/core");
var item_service_1 = require("../items/item.service");
var item_history_service_1 = require("./item_history.service");
var router_1 = require("@angular/router");
var ItemHistoryComponent = (function () {
    function ItemHistoryComponent(itemHistoryService, itemService, route) {
        this.itemHistoryService = itemHistoryService;
        this.itemService = itemService;
        this.route = route;
    }
    ItemHistoryComponent.prototype.getHistoryFromScratch = function (name, time_start) {
        var _this = this;
        this.itemHistoryService.getHistoryFromScratch(name, time_start).subscribe(
        // res => this.items = res,
        function (res) {
            for (var _i = 0, res_1 = res; _i < res_1.length; _i++) {
                var i = res_1[_i];
                console.log(i['state']);
            }
        }, function (error) { return _this.errorMessage = error; });
    };
    ItemHistoryComponent.prototype.getUpdatedHistory = function (name, time_start) {
        var _this = this;
        this.itemHistoryService.getUpdatedHistory(name, time_start).subscribe(function (res) { return _this.items = res; }, function (error) { return _this.errorMessage = error; });
    };
    ItemHistoryComponent.prototype.getItemType = function (name) {
        var _this = this;
        this.itemService.getItemByName(name).subscribe(function (res) { return _this.selectedType = res['type']; });
        // console.log(this.selectedType)
    };
    ItemHistoryComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.route.params.subscribe(function (params) {
            _this.selectedName = params['name'];
            _this.getItemType(_this.selectedName);
            _this.getHistoryFromScratch(_this.selectedName, _this.selectedType);
        });
    };
    ItemHistoryComponent.prototype.ngAfterViewInit = function () {
        this.renderChart();
    };
    ItemHistoryComponent.prototype.renderChart = function () {
        Highcharts.setOptions({
            global: {
                useUTC: false
            }
        });
        // Create the chart
        Highcharts.stockChart('container', {
            chart: {
                events: {
                    load: function () {
                        // set up the updating of the chart each second
                        var series = this.series[0];
                        setInterval(function () {
                            var x = (new Date()).getTime(), // current time
                            y = Math.round(Math.random() * 100);
                            series.addPoint([x, y], true, true);
                        }, 1000);
                    }
                }
            },
            rangeSelector: {
                buttons: [{
                        count: 1,
                        type: 'minute',
                        text: '1M'
                    }, {
                        count: 5,
                        type: 'minute',
                        text: '5M'
                    }, {
                        type: 'all',
                        text: 'All'
                    }],
                inputEnabled: false,
                selected: 0
            },
            title: {
                text: this.selectedName
            },
            exporting: {
                enabled: false
            },
            series: [{
                    name: 'Random data',
                    data: (function () {
                        // generate an array of random data
                        var data = [], time = (new Date()).getTime(), i;
                        for (i = -999; i <= 0; i += 1) {
                            data.push([
                                time + i * 1000,
                                Math.round(Math.random() * 100)
                            ]);
                        }
                        return data;
                    }())
                }]
        });
    };
    return ItemHistoryComponent;
}());
ItemHistoryComponent = __decorate([
    core_1.Component({
        moduleId: module.id,
        selector: 'pm-item-history',
        templateUrl: 'item_history.template.html',
        providers: [item_history_service_1.ItemHistoryService, item_service_1.ItemService]
    }),
    __metadata("design:paramtypes", [item_history_service_1.ItemHistoryService,
        item_service_1.ItemService,
        router_1.ActivatedRoute])
], ItemHistoryComponent);
exports.ItemHistoryComponent = ItemHistoryComponent;
//# sourceMappingURL=item_history.component.js.map