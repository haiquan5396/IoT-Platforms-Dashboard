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
        this.raw_data = [];
    }
    ItemHistoryComponent.prototype.getHistoryFromScratch = function (name, time_start) {
        var _this = this;
        var flag = true;
        while (flag) {
            this.itemHistoryService.getHistoryFromScratch(name, time_start).subscribe(function (res) {
                for (var _i = 0, res_1 = res; _i < res_1.length; _i++) {
                    var i = res_1[_i];
                    _this.raw_data.push(i);
                }
            }, function (error) { return _this.errorMessage = error; });
            flag = false;
        }
    };
    ItemHistoryComponent.prototype.getUpdatedHistory = function (name, time_start) {
        var _this = this;
        this.itemHistoryService.getUpdatedHistory(name, time_start).subscribe(function (res) { return _this.raw_data = res; }, function (error) { return _this.errorMessage = error; });
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
            _this.getHistoryFromScratch(_this.selectedName, "2");
        });
    };
    ItemHistoryComponent.prototype.ngAfterViewInit = function () {
        this.renderChart(this.selectedName, '2');
    };
    ItemHistoryComponent.prototype.renderChart = function (name, time) {
        var url = 'http://localhost:1337/api/states/history/' + name + '/first_time/' + time;
        jQuery.getJSON(url, function (data) {
            //option
            Highcharts.setOptions({
                global: {
                    useUTC: false
                }
            });
            //##########################################################
            Highcharts.stockChart('container', {
                chart: {
                    events: {
                        load: function () {
                            // set up the updating of the chart each second
                            var series = this.series[0];
                            var time_start = data[data.length - 1]['0'];
                            setInterval(function () {
                                updateData(time_start);
                            }, 1000);
                            function updateData(time_start) {
                                console.log("update");
                                var url2 = 'http://localhost:1337/api/states/history/' + name + '/second_time/' + time_start;
                                data = jQuery.getJSON(url2, function (data1) {
                                    for (var _i = 0, data1_1 = data1; _i < data1_1.length; _i++) {
                                        var item = data1_1[_i];
                                        var time = new Date(item['0']).getTime();
                                        var state = Number(item['1']);
                                        series.addPoint([time * 1000, state], true, true);
                                    }
                                    ;
                                    update_time(data1[data1.length - 1] + '');
                                });
                                function update_time(time) {
                                    time_start = time;
                                }
                                console.log(time_start);
                            }
                            // updateData(time_start)
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
                            var newdata = [];
                            for (var _i = 0, data_1 = data; _i < data_1.length; _i++) {
                                var i = data_1[_i];
                                var time = new Date(i['0']).getTime();
                                var state = Number(i['1']);
                                newdata.push([time * 1000, state]);
                            }
                            return newdata;
                        }())
                    }]
            });
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