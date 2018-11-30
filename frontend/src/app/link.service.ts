import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { headers } from '../utils';

export interface Link {
  id: number;
  url: string;
  description: string;
}

@Injectable({
  providedIn: 'root',
})
export class LinkService {

  constructor(private http: HttpClient) { }

  addLink(songID: number, url: string, description: string): Observable<Link> {
    const body = { url, description };
    return this.http.post<Link>(`api/songs/${songID}/links`, body, { headers });
  }

  deleteLink(linkID: number): Observable<boolean> {
    return this.http.delete<boolean>(`api/links/${linkID}`, { headers });
  }
}
