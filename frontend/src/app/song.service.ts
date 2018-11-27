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

export interface SongFilters {
  setlistID: number;
  suggested?: boolean;
}

function filtersToParams(filters: SongFilters): HttpParams {
  const params = {};
  params['setlist'] = `${filters.setlistID}`;
  if (filters.suggested != null) { params['suggested'] = `${filters.suggested ? 1 : 0}`; }
  return new HttpParams({ fromObject: params });
}

@Injectable()
export class SongService {
  constructor(private http: HttpClient) { }

  getSongs(filters: SongFilters): Observable<SongOverview[]> {
    const url = '/api/songs';
    const params = filtersToParams(filters);
    return this.http.get<SongOverviewJSON[]>('/api/songs', { headers, params })
      .pipe(map(jsonArr => jsonArr.map(jsonToSong)));
  }

  addSong(title: string, artist: String, autosuggest = 0): Observable<SongOverview> {
    const url = 'api/songs';
    const body = {
      title,
      artist,
    };
    if (autosuggest) { body['autosuggest'] = autosuggest; }
    return this.http.post<SongOverviewJSON>(url, body, { headers })
      .pipe(map(jsonToSong));
  }

  suggestSong(setlistID: number, songID: number): Observable<SongOverview> {
    const url = `api/setlists/${setlistID}/suggestions`;
    const body = {
      songID,
    };
    return this.http.post<SongOverviewJSON>(url, body, { headers })
      .pipe(map(jsonToSong));
  }

  rateSuggestion(suggestionID: number, newRating: number): Observable<SongOverview> {
    const url = `api/suggestions/${suggestionID}/ratings/mine`;
    const body = newRating;
    return this.http.put<SongOverviewJSON>(url, body, { headers })
      .pipe(map(jsonToSong));
  }

}
