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

    ngOnInit() { 
        this.getItems();
    }

    getItems(): void{
        this.itemsService.getItems().subscribe(
            items => this.items = items,
            error => this.errorMessage = <any> error
        )
    }
}