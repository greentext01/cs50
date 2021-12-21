import { HttpClient } from '@angular/common/http';
import { Component, ChangeDetectionStrategy, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import Chart from 'chart.js/auto';
import zoomPlugin from 'chartjs-plugin-zoom';
import { MoistureData } from './moistureData';

Chart.register(zoomPlugin);

@Component({
    selector: 'app-graph',
    templateUrl: './graph.component.html',
    styleUrls: ['./graph.component.css'],
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class GraphComponent implements AfterViewInit {
    @ViewChild('graph') graphCanvas: ElementRef;

    constructor(private http: HttpClient) { }

    ngAfterViewInit(): void {
        this.http.get<MoistureData>('http://24.54.14.56:5000/api/moisture', { responseType: 'json' }).subscribe(resp => {
            new Chart(this.graphCanvas.nativeElement, {
                type: 'line',
                data: {
                    labels: resp.time,
                    datasets: [{
                        label: 'Moisture',
                        backgroundColor: 'rgb(255, 99, 132)',
                        borderColor: 'rgb(255, 99, 132)',
                        data: resp.moisture
                    }, {
                        label: 'Threshold',
                        backgroundColor: 'rgb(105, 230, 255)',
                        borderColor: 'rgb(105, 230, 255)',
                        data: resp.threshold
                    }]
                },
                options: {
                    scales: {
                        x: {
                            max: 40,
                        }
                    },
                    plugins: {
                        zoom: {
                            pan: {
                                enabled: true,
                                mode: 'x'
                            },
                            zoom: {
                                wheel: {
                                    enabled: true,
                                },
                                pinch: {
                                    enabled: true
                                },
                                mode: 'x',
                            }
                        }
                    },
                    maintainAspectRatio: false,
                },
            });
        });
    }
}
