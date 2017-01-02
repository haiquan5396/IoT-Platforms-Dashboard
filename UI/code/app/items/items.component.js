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
var router_1 = require("@angular/router");
var item_service_1 = require("./item.service");
var ItemsComponent = (function () {
    function ItemsComponent(itemsService, router) {
        this.itemsService = itemsService;
        this.router = router;
        this.switchTypes = ['light', 'switch', 'SwitchItem'];
    }
    ItemsComponent.prototype.ngOnInit = function () {
        this.getItems();
    };
    ItemsComponent.prototype.isSwitchTypes = function (type) {
        for (var _i = 0, _a = this.switchTypes; _i < _a.length; _i++) {
            var stype = _a[_i];
            if (stype == type)
                return true;
        }
        return false;
    };
    ItemsComponent.prototype.isOn = function (state) {
        if (state == 'on' || state == 'ON')
            return true;
        return false;
    };
    ItemsComponent.prototype.changeState = function (item) {
        var _this = this;
        this.itemsService.changeItemState(item).subscribe(function (res) { return console.log(res); }, function (error) { return _this.errorMessage = error; });
    };
    ItemsComponent.prototype.getItems = function () {
        var _this = this;
        this.itemsService.getItems().subscribe(function (items) { return _this.items = items; }, function (error) { return _this.errorMessage = error; });
    };
    ItemsComponent.prototype.goToHistory = function (item) {
        this.router.navigate(['/history', item[0]]);
    };
    return ItemsComponent;
}());
ItemsComponent = __decorate([
    core_1.Component({
        moduleId: module.id,
        selector: 'pm-items',
        templateUrl: 'items.template.html',
        styleUrls: ['items.component.css'],
        providers: [item_service_1.ItemService]
    }),
    __metadata("design:paramtypes", [item_service_1.ItemService,
        router_1.Router])
], ItemsComponent);
exports.ItemsComponent = ItemsComponent;
//# sourceMappingURL=items.component.js.map