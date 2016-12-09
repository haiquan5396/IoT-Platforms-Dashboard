import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule, Routes } from '@angular/router';
import { HttpModule, JsonpModule} from '@angular/http';
import { FormsModule } from '@angular/forms';

import { AppComponent }  from './app.component';
import { SideBarComponent } from './sidebar/sidebar.component';
import { NavComponent } from './nav/nav.component';
import { ItemsComponent } from './items/items.component';
import { HelpComponent } from './help/help.component';

const appRoutes: Routes = [
  { path: 'home', component: ItemsComponent },
  { path: 'help', component: HelpComponent},
  { path: '', component: ItemsComponent},
  // { path: '/scr'}
]


@NgModule({
  imports: [ 
    BrowserModule,
    HttpModule,
    JsonpModule,
    RouterModule.forRoot(appRoutes)
     ],
  declarations: [ 
    AppComponent,
    SideBarComponent,
    NavComponent,
    ItemsComponent,
    HelpComponent,
    ],
  providers: [],
  bootstrap: [ AppComponent ]
})
export class AppModule { }
