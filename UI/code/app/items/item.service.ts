import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';
import {Observable}     from 'rxjs/Observable';

import { Item } from './item';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
@Injectable()

export class ItemService {
    constructor(private http: Http){}
    
    getItems(): Observable<Item[]> {
        // return Observable.interval(1000).flatMap(() => {
        //     return this.http.get('http://localhost:1337/api/states').map((res:Response) => res.json());
        // });
        return this.http.get('http://localhost:1337/api/states').map((res:Response) => res.json());
    }
}

