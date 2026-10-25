
import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface PredictionResponse {
  prediction: number;
  class: string;
  model: string;
  probabilities?: Record<string, number>;
}

@Injectable({
  providedIn: 'root'
})
export class PredictionService {
  private http = inject(HttpClient);

  loadSample(): Observable<Record<string, unknown>> {
    return this.http.get<Record<string, unknown>>(
      '/sample_input.json'
    );
  }

  predict(
    features: Record<string, unknown>
  ): Observable<PredictionResponse> {
    return this.http.post<PredictionResponse>(
      '/api/predict',
      features
    );
  }
}
