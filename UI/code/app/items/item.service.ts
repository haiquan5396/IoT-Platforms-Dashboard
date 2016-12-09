import { Injectable } from '@angular/core';
import { Http, Response, Headers, RequestOptions } from '@angular/http';
import {Observable}     from 'rxjs/Rx';

import { Item } from './item';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
@Injectable()

export class ItemService {
    constructor(private http: Http){}
    state : string;
    getItems(): Observable<Item[]> {
        return Observable
        .interval(1000).flatMap(() => {
            return this.http.get('http://localhost:1337/api/states').map((res:Response) => res.json());
        });
        // return this.http.get('http://localhost:1337/api/states').map((res:Response) => res.json());
    }

    changeItemState(item: Item) {
        switch (item[1]){
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
        let headers = new Headers({ 'Content-Type': 'application/json' });
        let options = new RequestOptions({ headers: headers });
        return this.http.post('http://localhost:1337/api/states/'+item[0], JSON.stringify({'state':this.state}), options)
                .map(this.extractData)
                .catch(this.handleError);
    }
    private extractData(res: Response) {
        let body = res.json();
        return body.data || { };
    }
    private handleError (error: Response | any) {
        // In a real world app, we might use a remote logging infrastructure
        let errMsg: string;
        if (error instanceof Response) {
        const body = error.json() || '';
        const err = body.error || JSON.stringify(body);
        errMsg = `${error.status} - ${error.statusText || ''} ${err}`;
        } else {
        errMsg = error.message ? error.message : error.toString();
        }
        console.error(errMsg);
        return Observable.throw(errMsg);
    }
}

