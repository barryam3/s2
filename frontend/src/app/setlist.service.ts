import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { BehaviorSubject } from 'rxjs';
import { map, tap, distinctUntilChanged } from 'rxjs/operators';

import { unixTimestamp } from '../utils';

const headers: HttpHeaders = new HttpHeaders({
  'Content-Type': 'application/json',
});

interface SetlistBase {
  id: number;
  title: string;
}

interface SetlistJSON extends SetlistBase {
  suggestDeadline: number;
  voteDeadline: number;
}

export interface Setlist extends SetlistBase {
  suggestDeadline: Date;
  voteDeadline: Date;
}

function jsonToSetlist(json: SetlistJSON): Setlist {
  if (!json) { return null; }
  return Object.assign(
    {},
    json,
    {
      suggestDeadline: new Date(json.suggestDeadline * 1000),
      voteDeadline: new Date(json.voteDeadline * 1000),
    },
  );
}

function defaultDeadlines() {
  const now = new Date();
  const suggestDeadline = new Date();
  const voteDeadline = new Date();
  suggestDeadline.setMonth(now.getMonth() + 1);
  voteDeadline.setMonth(now.getMonth() + 2);
  [suggestDeadline, voteDeadline].forEach(deadline => {
    deadline.setHours(0);
    deadline.setMinutes(0);
    deadline.setSeconds(0);
    deadline.setMilliseconds(0);
  });
  return {
    suggestDeadline: unixTimestamp(suggestDeadline),
    voteDeadline: unixTimestamp(voteDeadline),
  };
}

@Injectable()
export class SetlistService {
  private setlistSubject = new BehaviorSubject<Setlist>(null);
  public currentSetlist = this.setlistSubject.asObservable().pipe(distinctUntilChanged());

  constructor(private http: HttpClient) { }

  createSetlist(title: string) {
    const url = 'api/setlists';
    const body = {
      title,
      ...defaultDeadlines(),
    };
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

  editSetlistDeadlines(setlistID: number, deadlines: { voteDeadline: Date, suggestDeadline: Date }) {
    const url = `api/setlists/${setlistID}`;
    const body = {
      suggestDeadline: unixTimestamp(deadlines.suggestDeadline),
      voteDeadline: unixTimestamp(deadlines.voteDeadline),
    };
    return this.http.patch<SetlistJSON>(url, body, { headers })
      .pipe(
        map(jsonToSetlist),
        tap(setlist => this.setlistSubject.next(setlist)),
      );
  }

}
