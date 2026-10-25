
import { Component, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { KeyValuePipe } from '@angular/common';
import {
  PredictionService,
  PredictionResponse
} from './prediction.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [FormsModule, KeyValuePipe],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit {
  private predictionService = inject(PredictionService);

  jsonText = '';
  result: PredictionResponse | null = null;
  error = '';
  loading = false;

  ngOnInit(): void {
    this.predictionService.loadSample().subscribe({
      next: (sample) => {
        this.jsonText = JSON.stringify(sample, null, 2);
      },
      error: () => {
        this.error = 'Could not load sample_input.json.';
      }
    });
  }

  runPrediction(): void {
    this.error = '';
    this.result = null;

    let features: Record<string, unknown>;

    try {
      features = JSON.parse(this.jsonText);

      if (
        features === null ||
        typeof features !== 'object' ||
        Array.isArray(features)
      ) {
        throw new Error('Input must be a JSON object.');
      }
    } catch {
      this.error = 'Invalid JSON. Check the input and try again.';
      return;
    }

    this.loading = true;

    this.predictionService.predict(features).subscribe({
      next: (response) => {
        this.result = response;
        this.loading = false;
      },
      error: (err) => {
        this.error =
          err.error?.error ||
          'Prediction failed. Check that Flask is running.';
        this.loading = false;
      }
    });
  }
}
