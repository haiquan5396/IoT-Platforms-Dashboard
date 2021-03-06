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
var platform_browser_1 = require("@angular/platform-browser");
var router_1 = require("@angular/router");
var http_1 = require("@angular/http");
var app_component_1 = require("./app.component");
var sidebar_component_1 = require("./sidebar/sidebar.component");
var nav_component_1 = require("./nav/nav.component");
var items_component_1 = require("./items/items.component");
var help_component_1 = require("./help/help.component");
var item_history_component_1 = require("./item_history/item_history.component");
var appRoutes = [
    { path: 'home', component: items_component_1.ItemsComponent },
    { path: 'help', component: help_component_1.HelpComponent },
    { path: 'history/:name', component: item_history_component_1.ItemHistoryComponent },
    { path: '', component: items_component_1.ItemsComponent },
];
var AppModule = (function () {
    function AppModule() {
    }
    return AppModule;
}());
AppModule = __decorate([
    core_1.NgModule({
        imports: [
            platform_browser_1.BrowserModule,
            http_1.HttpModule,
            http_1.JsonpModule,
            router_1.RouterModule.forRoot(appRoutes)
        ],
        declarations: [
            app_component_1.AppComponent,
            sidebar_component_1.SideBarComponent,
            nav_component_1.NavComponent,
            items_component_1.ItemsComponent,
            item_history_component_1.ItemHistoryComponent,
            help_component_1.HelpComponent,
        ],
        providers: [],
        bootstrap: [app_component_1.AppComponent]
    }),
    __metadata("design:paramtypes", [])
], AppModule);
exports.AppModule = AppModule;
//# sourceMappingURL=app.module.js.map