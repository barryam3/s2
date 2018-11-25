import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { BehaviorSubject } from 'rxjs';
import { map, tap, distinctUntilChanged } from 'rxjs/operators';

const headers: HttpHeaders = new HttpHeaders({
  'Content-Type': 'application/json',
});

interface SetlistBase {
  id: number;
  title: string;
}

interface SetlistJSON extends SetlistBase {
  suggestDeadline: string;
  voteDeadline: string;
}

export interface Setlist extends SetlistBase {
  suggestDeadline: Date;
  voteDeadline: Date;
}

function jsonToSetlist(json: SetlistJSON): Setlist {
  if (!json) { return null; }
  return Object.assign(
    { suggestDeadline: new Date(json.suggestDeadline),
      voteDeadline: new Date(json.voteDeadline),
    },
    json,
  );
}

@Injectable()
export class SetlistService {
  private BASE_URL = 'api/setlists';

  private setlistSubject = new BehaviorSubject<Setlist>(null);
  public currentSetlist = this.setlistSubject.asObservable().pipe(distinctUntilChanged());

  constructor(private http: HttpClient) { }

  createSetlist(title: string) {
    const url = 'api/setlists';
    const body = { title };
    return this.http.post<SetlistJSON>(url, body, { headers })
      .pipe(
        map(jsonToSetlist),
        tap(setlist => this.setlistSubject.next(setlist)),
      );
  }

  getSetlists() {
    const url = 'api/setlists';
    return this.http.get<SetlistJSON[]>(url, { headers })
      .pipe(
        map(setlists => setlists.map(jsonToSetlist)),
        tap(setlists => this.setlistSubject.next(setlists[0] || null)),
      );
  }

}
