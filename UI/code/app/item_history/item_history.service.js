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
var core_1 = require("@angular/core");
var http_1 = require("@angular/http");
var Rx_1 = require("rxjs/Rx");
require("rxjs/add/operator/map");
require("rxjs/add/operator/catch");
var ItemHistoryService = (function () {
    function ItemHistoryService(http) {
        this.http = http;
    }
    ItemHistoryService.prototype.getHistoryFromScratch = function (name, time_start) {
        return this.http.get('http://localhost:1337/api/states/history/' + name + '/first_time/' + time_start).map(function (res) { return res.json(); });
    };
    ItemHistoryService.prototype.getUpdatedHistory = function (name, time_start) {
        var _this = this;
        return Rx_1.Observable
            .interval(3000).flatMap(function () {
            return _this.http.get('http://localhost:1337/api/states/history/' + name + '/first_time/' + time_start).map(function (res) { return res.json(); });
        });
        // return this.http.get('http://localhost:1337/api/states').map((res:Response) => res.json());
    };
    return ItemHistoryService;
}());
ItemHistoryService = __decorate([
    core_1.Injectable(),
    __metadata("design:paramtypes", [http_1.Http])
], ItemHistoryService);
exports.ItemHistoryService = ItemHistoryService;
//# sourceMappingURL=item_history.service.js.map