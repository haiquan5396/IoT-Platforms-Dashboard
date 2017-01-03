import 'rxjs/add/operator/switchMap';
import { Component, OnInit } from '@angular/core';
import { Item } from '../items/item';
import { ItemService } from '../items/item.service';
import { ItemHistoryService } from './item_history.service';
import { ActivatedRoute, Params } from '@angular/router';
import { Http } from '@angular/http';
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
    private raw_data: string[][]
    constructor(
        private itemHistoryService: ItemHistoryService,
        private itemService: ItemService,
        private route: ActivatedRoute,
    ) {
        this.raw_data = []
    }
    getHistoryFromScratch(name: string, time_start: string):void{ //time_start 1phut, 2 phut, 100phut
        let flag = true
        while (flag){
            this.itemHistoryService.getHistoryFromScratch(name, time_start).subscribe(
                res => {
                    for (let i of res){
                        this.raw_data.push(i)
                    }
                },
                error => this.errorMessage = <any> error
            )
            flag = false   
        }
        
    }
    getUpdatedHistory(name: string, time_start:string): void { //time_start moc thoi gian
        this.itemHistoryService.getUpdatedHistory(name, time_start).subscribe(
            res => this.raw_data = res,
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
        this.getHistoryFromScratch(this.selectedName, "2")
        })

    }

    ngAfterViewInit(){
      this.renderChart(this.selectedName,'2');
    }
    renderChart(name:string, time:string){
        var url = 'http://localhost:1337/api/states/history/'+name+'/first_time/'+ time;
        jQuery.getJSON(url,function(data:string[][]){
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
                            var time_start = data[data.length-1]['0']

                            setInterval(function(){
                                updateData(time_start)
                            }, 1000);

                            function updateData(time_start:string){
                                console.log("update");
                                var url2 = 'http://localhost:1337/api/states/history/'+name+'/second_time/'+ time_start
                                data = jQuery.getJSON(url2,function(data1:string[][]){
                                    for (let item of data1){
                                        var time = new Date(item['0']).getTime();
                                        var state = Number(item['1'])
                                        series.addPoint([time*1000,state],true,true)
                                    };
                                    update_time(data1[data1.length-1]+'');
                                    
                                });
                                function update_time(time:string){
                                    time_start = time;
                                }
                                console.log(time_start)
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
                        for( let i of data){
                            var time = new Date(i['0']).getTime();
                            var state = Number(i['1'])
                            newdata.push([time*1000,state])
                        }
                        return newdata;
                    }())
                }]
            })

        });
    }

}