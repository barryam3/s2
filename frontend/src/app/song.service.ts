import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';

import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

const headers: HttpHeaders = new HttpHeaders({
  'Content-Type': 'application/json',
});

export interface SongOverviewBase {
  arranged: boolean;
  artist: string;
  id: number;
  lyrics: string;
  title: string;
}

interface SongOverviewJSON extends SongOverviewBase {
  edited: number;
}

export interface SuggestedSongOverview extends SongOverviewBase {
  suggestion?: {
    id: number,
    suggestor: string,
    rating: number,
  };
}

export type SongOverview = SuggestedSongOverview | SongOverviewBase;

interface SuggestionJSON {
  song: SongOverviewJSON;
  id: number;
  suggestor: string;
  setlist: string;
}

function suggestionToSong(suggestion: SuggestionJSON): SuggestedSongOverview {
  return {
    ...suggestion.song,
    suggestion: {
      id: suggestion.id,
      suggestor: suggestion.suggestor,
      rating: Math.floor(Math.random() * 4) + 1, // TODO
    },
  };
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

  getSuggestions(setlistID: number): Observable<SuggestedSongOverview[]> {
    const url = `api/setlists/${setlistID}/suggestions`;
    return this.http.get<SuggestionJSON[]>(url, { headers })
      .pipe(map(jsonArr => jsonArr.map(suggestionToSong)));
  }

  suggestSong(setlistID: number, songID: number): Observable<SuggestedSongOverview> {
    const url = `api/setlists/${setlistID}/suggestions`;
    const body = {
      songID,
    };
    return this.http.post<SuggestionJSON>(url, body, { headers })
      .pipe(map(suggestionToSong));
  }

}
