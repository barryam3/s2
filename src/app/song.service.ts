import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';

import { Observable } from 'rxjs';

import { Song } from './song';

const headers: HttpHeaders = new HttpHeaders({
  'Content-Type': 'application/json',
});

@Injectable()
export class SongService {
  private BASE_URL = 'api/song';

  constructor(private http: HttpClient) { }

  getSongs(current): Observable<Song[]> {
    const url = `${this.BASE_URL}/`;
    let params = new HttpParams();
    if (current !== undefined) {
      params = params.set('current', current ? '1' : '0');
    }
    return this.http.get<Song[]>(url, { params, headers });
  }

  addSong(title: string, artist: string) {
    const url = `${this.BASE_URL}/`;
    const body = {
      title,
      artist,
    };
    return this.http.post<Song>(url, body, { headers });
  }

}
