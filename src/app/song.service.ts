import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';

import { Observable } from 'rxjs';

import { Song } from './song';

@Injectable()
export class SongService {
  private BASE_URL = 'api/song';
  private headers: HttpHeaders = new HttpHeaders({
    'Content-Type': 'application/json',
  });

  constructor(private http: HttpClient) { }

  getSongs(current = true): Observable<Song[]> {
    const url = `${this.BASE_URL}/`;
    const params = new HttpParams();
    if (current !== undefined) {
      params.set('current', current ? '1' : '0');
    }
    return this.http.get<Song[]>(url, { params, headers: this.headers });
  }

}
