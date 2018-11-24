import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';

import { Observable } from 'rxjs';

import { Song } from './song';
import { objectToParams } from '../utils';

const headers: HttpHeaders = new HttpHeaders({
  'Content-Type': 'application/json',
});

export enum Solo {
  Male = 'Male',
  Female = 'Female',
  Both = 'Both',
  Either = 'Either',
  None = 'None',
}

export type SongQueryOptions = {
  title?: string;
  artist?: string;
  current?: boolean;
  arranged?: boolean;
  solo?: Solo;
  sort?: 'title' | 'artist' | 'suggestor';
  asc?: boolean;
  size?: number;
  page?: number;
};

@Injectable()
export class SongService {
  private BASE_URL = 'api/songs';

  constructor(private http: HttpClient) { }

  getSongs(options: SongQueryOptions): Observable<Song[]> {
    const url = `${this.BASE_URL}/`;
    const params = objectToParams(options);
    return this.http.get<Song[]>(url, { params, headers });
  }

  addSong(title: string, artist: string, solo: Solo) {
    const url = `${this.BASE_URL}/`;
    const body = {
      title,
      artist,
      solo,
    };
    return this.http.post<number>(url, body, { headers });
  }

}
