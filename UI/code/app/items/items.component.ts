import { Component, OnInit } from '@angular/core';
import { ItemService } from './item.service';
import { Item } from './item';
@Component({
    moduleId: module.id,
    selector: 'pm-items',
    templateUrl: 'items.template.html',
    styleUrls: ['items.component.css'],
    providers: [ItemService]
})
export class ItemsComponent implements OnInit {
    errorMessage: string;
    items: Item[];
    selectedItem: Item;
    constructor(private itemsService: ItemService) { }

    switchTypes: string[] = ['light','switch','SwitchItem']
    ngOnInit() { 
        this.getItems();
    }

    isSwitchTypes(type: string) {
        for (let stype of this.switchTypes){
            if (stype == type) return true;
        }
        return false;
    }

    isOn(state: string){
        if (state == 'on' || state == 'ON') return true;
        return false;
    }

    changeState(item: Item): void {
        this.itemsService.changeItemState(item).subscribe(
            res => console.log(res),
            error => this.errorMessage = <any> error
        )
    }
    getItems(): void{
        this.itemsService.getItems().subscribe(
            items => this.items = items,
            error => this.errorMessage = <any> error
        )
    }
}