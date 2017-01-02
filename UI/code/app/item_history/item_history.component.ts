import 'rxjs/add/operator/switchMap';
import { Component, OnInit } from '@angular/core';
import { Item } from '../items/item';
import { ItemService } from '../items/item.service';
import { ItemHistoryService } from './item_history.service';
import { ActivatedRoute, Params } from '@angular/router';
declare var jQuery:any ;
declare var Highcharts:any ;
@Component({
    moduleId: module.id,
    selector: 'pm-item-history',
    templateUrl: 'item_history.template.html',
    providers: [ItemHistoryService, ItemService]
})
export class ItemHistoryComponent implements OnInit {
    private items: Item[]
    private errorMessage: string
    private selectedType:string
    private selectedName: string
    private start_time:string // onInit -> goi lan dau tien luon -> luu lai moc thoi gian nay

    constructor(
        private itemHistoryService: ItemHistoryService,
        private itemService: ItemService,
        private route: ActivatedRoute,
    ) {}
    getHistoryFromScratch(name: string, time_start: string):void{ //time_start 1phut, 2 phut, 100phut
        this.itemHistoryService.getHistoryFromScratch(name, time_start).subscribe(
            // res => this.items = res,
            res => {
                for (let i of res){
                    console.log(i['state'])
                }
            },
            error => this.errorMessage = <any> error
        )
    }
    getUpdatedHistory(name: string, time_start:string): void { //time_start moc thoi gian
        this.itemHistoryService.getUpdatedHistory(name, time_start).subscribe(
            res => this.items = res,
            error => this.errorMessage = <any> error
        )
    }

    getItemType(name: string): void {
        this.itemService.getItemByName(name).subscribe(
            res => this.selectedType = res['type']
        )
        // console.log(this.selectedType)
    }


    ngOnInit() {
        this.route.params.subscribe(params => {
        this.selectedName = params['name'];
        this.getItemType(this.selectedName)
        this.getHistoryFromScratch(this.selectedName, this.selectedType)
        })
    }

    ngAfterViewInit(){
      this.renderChart();
    }
    renderChart(){

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
                  var data = [],
                      time = (new Date()).getTime(),
                      i;

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
    }

}