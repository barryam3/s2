import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';

import { Observable } from 'rxjs/observable';

export interface Song {
  id: number;
  title: string;
  artist: string;
  genre: string;
  solo: string;
  suggestor: number;
  last_edit: Date;
  current: boolean;
  arranged: boolean;
}

@Injectable()
export class SongService {
  private BASE_URL = 'api/song';
  private headers: HttpHeaders = new HttpHeaders({
    'Content-Type': 'application/json',
  });

  constructor(private http: HttpClient) { }

  getSongs(current= true): Observable<Song[]> {
    const url = `${this.BASE_URL}/`;
    const params = new HttpParams().set('current', current ? '1' : '0');
    return this.http.get<Song[]>(url, { params, headers: this.headers });
  }

}
