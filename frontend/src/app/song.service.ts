import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import * as _ from 'lodash';

import { headers, objectToParams } from '../utils';
import { Link } from './link.service';
import { Comment, CommentJSON, jsonToComment } from './comment.service';

export interface SongOverview {
  id: number;
  title: string;
  artist: string;
  lyrics: string;
  arranged: boolean;
  suggestor: string | null;
  myRating: number | null;
  // below are dates but I have no need to convert them
  lastEdited: number;
  lastViewed: number;
}

export interface SongBase extends SongOverview {
  links: Link[];
}

export interface SongJSON extends SongBase {
  comments: CommentJSON[];
}

export interface Song extends SongBase {
  comments: Comment[];
}

export interface GetSongOptions {
  suggested?: boolean;
  title?: string;
  artist?: string;
  arranged?: boolean;
  suggestor?: string;
}

export interface UpdateSongOptions {
  title?: string;
  artist?: string;
  lyrics?: string;
  arranged?: boolean;
  suggested?: boolean;
}

@Injectable()
export class SongService {
  constructor(private http: HttpClient) { }

  getSong(songID: number): Observable<Song> {
    const url = `api/songs/${songID}`;
    return this.http.get<SongJSON>(url, { headers })
      .pipe(map(songJSON => {
        songJSON.comments.sort((cA, cB) => cA.timestamp - cB.timestamp);
        const song: Song = {
          ...songJSON,
          comments: _.sortBy(songJSON.comments, 'timestamp').map(jsonToComment),
        };
        return song;
      }));
  }

  getSongs(filters: GetSongOptions): Observable<SongOverview[]> {
    const url = 'api/songs';
    const params = objectToParams(filters);
    return this.http.get<SongOverview[]>(url, { headers, params });
  }

  addSong(title: string, artist: String): Observable<SongOverview> {
    const url = 'api/songs';
    const body = {
      title,
      artist,
    };
    return this.http.post<SongOverview>(url, body, { headers });
  }

  updateSong(songID: number, body: UpdateSongOptions): Observable<boolean> {
    const url = `api/songs/${songID}`;
    return this.http.patch<boolean>(url, body, { headers });
  }

  rateSong(songID: number, rating: number): Observable<boolean> {
    const url = `api/songs/${songID}/ratings/mine`;
    const body = { rating };
    return this.http.put<boolean>(url, body, { headers });
  }

  deleteSong(songID: number): Observable<boolean> {
    const url = `api/songs/${songID}`;
    return this.http.delete<boolean>(url, { headers });
  }

}
