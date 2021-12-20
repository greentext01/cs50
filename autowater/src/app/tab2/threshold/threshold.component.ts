import { HttpRequest, HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, OnInit, ChangeDetectionStrategy } from '@angular/core';
import { ToastController } from '@ionic/angular';
import { errorMonitor } from 'events';
import { Threshold } from './threshold';

@Component({
    selector: 'app-threshold',
    templateUrl: './threshold.component.html',
    styleUrls: ['./threshold.component.css'],
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class ThresholdComponent implements OnInit {
    model = new Threshold();

    constructor(private http: HttpClient, public toastController: ToastController) {
    }

    async toast(msg: string) {
        const toast = await this.toastController.create({
            message: msg,
            duration: 2000
        });
        toast.present();
    }

    ngOnInit(): void {
    }

    onSubmit(): void {
        if (!this.model.password) {
            this.toast('Password is empty!');
            return;
        } else if (!this.model.threshold) {
            this.toast('Threshold is empty!');
            return;
        }

        console.log(this.http);
        const headers: HttpHeaders = new HttpHeaders().set('Content-Type', 'application/x-www-form-urlencoded');
        this.http.post<any>('http://24.54.14.56:5000/api/threshold',
            `threshold=${this.model.threshold}&password=${this.model.password}`, {
            headers,
            observe: 'response'
        }).subscribe(
            (response) => {
                this.toast('Threshold updated!');
            },
            (error) => {
                if (error.status === 403) {
                    this.toast('Wrong password!');
                } else {
                    this.toast('Misc error: ' + error.status);
                }
            }
        );
    }
}
