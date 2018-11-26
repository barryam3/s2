import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';

import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

const headers: HttpHeaders = new HttpHeaders({
  'Content-Type': 'application/json',
});

interface SongOverviewBase {
  arranged: boolean;
  artist: string;
  id: number;
  lyrics: string;
  title: string;
  suggestion?: Suggestion;
}

interface Suggestion {
  id: number;
  setlistID: number;
  suggestor: string;
  myRating?: number;
}

export interface SongOverview extends SongOverviewBase {
  edited: Date;
}

interface SongOverviewJSON extends SongOverviewBase {
  edited: number;
}

function jsonToSong(json: SongOverviewJSON): SongOverview {
  return Object.assign({}, json, { edited: new Date(json.edited * 1000) });
}

@Injectable()
export class SongService {
  constructor(private http: HttpClient) { }

  getSongs(): Observable<SongOverviewBase[]> {
    const url = 'api/songs';
    return this.http.get<SongOverviewJSON[]>(url, { headers });
  }

  addSong(title: string, artist: String, autosuggest = 0): Observable<SongOverviewBase> {
    const url = 'api/songs';
    const body = {
      title,
      artist,
    };
    if (autosuggest) { body['autosuggest'] = autosuggest; }
    return this.http.post<SongOverviewJSON>(url, body, { headers });
  }

  getSuggestions(setlistID: number): Observable<SongOverview[]> {
    const url = `api/songs?setlist=${setlistID}&suggested=1`;
    return this.http.get<SongOverviewJSON[]>(url, { headers })
      .pipe(map(jsonArr => jsonArr.map(jsonToSong)));
  }

  suggestSong(setlistID: number, songID: number): Observable<SongOverview> {
    const url = `api/setlists/${setlistID}/suggestions`;
    const body = {
      songID,
    };
    return this.http.post<SongOverviewJSON>(url, body, { headers })
      .pipe(map(jsonToSong));
  }

}
