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
var ItemService = (function () {
    function ItemService(http) {
        this.http = http;
    }
    ItemService.prototype.getItems = function () {
        var _this = this;
        return Rx_1.Observable
            .interval(1000).flatMap(function () {
            return _this.http.get('http://localhost:1337/api/states').map(function (res) { return res.json(); });
        });
        // return this.http.get('http://localhost:1337/api/states').map((res:Response) => res.json());
    };
    ItemService.prototype.changeItemState = function (item) {
        switch (item[1]) {
            case 'off':
                this.state = 'on';
                break;
            case 'OFF':
                this.state = 'ON';
                break;
            case 'on':
                this.state = 'off';
                break;
            case 'ON':
                this.state = 'OFF';
                break;
        }
        var headers = new http_1.Headers({ 'Content-Type': 'application/json' });
        var options = new http_1.RequestOptions({ headers: headers });
        return this.http.post('http://localhost:1337/api/states/' + item[0], JSON.stringify({ 'state': this.state }), options)
            .map(this.extractData)
            .catch(this.handleError);
    };
    ItemService.prototype.extractData = function (res) {
        var body = res.json();
        return body.data || {};
    };
    ItemService.prototype.handleError = function (error) {
        // In a real world app, we might use a remote logging infrastructure
        var errMsg;
        if (error instanceof http_1.Response) {
            var body = error.json() || '';
            var err = body.error || JSON.stringify(body);
            errMsg = error.status + " - " + (error.statusText || '') + " " + err;
        }
        else {
            errMsg = error.message ? error.message : error.toString();
        }
        console.error(errMsg);
        return Rx_1.Observable.throw(errMsg);
    };
    return ItemService;
}());
ItemService = __decorate([
    core_1.Injectable(),
    __metadata("design:paramtypes", [http_1.Http])
], ItemService);
exports.ItemService = ItemService;
//# sourceMappingURL=item.service.js.map