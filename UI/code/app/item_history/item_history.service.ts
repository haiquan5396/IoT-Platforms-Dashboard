import { Injectable } from '@angular/core';
import { Http, Response, Headers, RequestOptions } from '@angular/http';
import {Observable}     from 'rxjs/Rx';

import { Item } from '../items/item';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';

@Injectable()
export class ItemHistoryService {

    constructor(private http: Http){}
    getHistoryFromScratch(name: string, time_start: string): Observable<string[][]>{
        return this.http.get('http://localhost:1337/api/states/history/'+name+'/first_time/'+ time_start).map((res:Response) => res.json());
    }
    getUpdatedHistory(name: string, time_start: string): Observable<string[][]> {
        return Observable
        .interval(3000).flatMap(() => {
            return this.http.get('http://localhost:1337/api/states/history/'+name+'/first_time/'+ time_start).map((res:Response) => res.json());
        });
        // return this.http.get('http://localhost:1337/api/states').map((res:Response) => res.json());
    }
}