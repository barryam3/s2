import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { headers, intToDate } from '../utils';
import { map } from 'rxjs/operators';

interface CommentBase {
  id: number;
  text: string;
  author: string;
}

export interface CommentJSON extends CommentBase {
  timestamp: number;
}

export interface Comment extends CommentBase {
  timestamp: Date;
}

export function jsonToComment(json: CommentJSON): Comment {
  return Object.assign({}, json, { timestamp: intToDate(json.timestamp) });
}

@Injectable({
  providedIn: 'root',
})
export class CommentService {

  constructor(private http: HttpClient) { }

  addComment(songID: number, text: string): Observable<Comment> {
    return this.http.post<CommentJSON>(`api/songs/${songID}/comments`, { text }, { headers })
      .pipe(map(jsonToComment));
  }

  editComment(commentID: number, text: string): Observable<boolean> {
    return this.http.patch<boolean>(`api/comments/${commentID}`, { text }, { headers });
  }

  deleteComment(commentID: number): Observable<boolean> {
    return this.http.delete<boolean>(`api/comments/${commentID}`, { headers });
  }
}
