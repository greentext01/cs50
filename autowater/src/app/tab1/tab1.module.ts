import { IonicModule } from '@ionic/angular';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Tab1Page } from './tab1.page';

import { Tab1PageRoutingModule } from './tab1-routing.module';
import { GraphComponent } from './graph/graph.component';

@NgModule({
    imports: [
        IonicModule,
        CommonModule,
        FormsModule,
        Tab1PageRoutingModule,
        FormsModule
    ],
    declarations: [Tab1Page, GraphComponent],
    exports: [
      GraphComponent
    ]
})
export class Tab1PageModule { }
