import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { dateToInt, headers, intToDate } from '../utils';

export interface Deadlines {
  voteDeadline: Date;
  suggestDeadline: Date;
}

interface DeadlinesJSON {
  voteDeadline: number;
  suggestDeadline: number;
}

function jsonToDeadlines(json: DeadlinesJSON): Deadlines {
  return {
    voteDeadline: intToDate(json.voteDeadline),
    suggestDeadline: intToDate(json.suggestDeadline),
  };
}

@Injectable({
  providedIn: 'root',
})
export class GroupService {

  constructor(private http: HttpClient) { }

  editDeadlines(deadlines: Deadlines): Observable<boolean> {
    const url = 'api/groups/1/deadlines';
    const body = {
      suggestDeadline: dateToInt(deadlines.suggestDeadline),
      voteDeadline: dateToInt(deadlines.voteDeadline),
    };
    return this.http.put<boolean>(url, body, { headers });
  }

  getDeadlines(): Observable<Deadlines> {
    const url = 'api/groups/1';
    return this.http.get<DeadlinesJSON>(url, { headers })
      .pipe(map(jsonToDeadlines));
  }

  unsuggestAll(): Observable<boolean> {
    const url = 'api/groups/1/suggestions';
    return this.http.delete<boolean>(url, { headers });
  }

  getRatings(): Observable<[string, string, number][]> {
    const url = 'api/groups/1/ratings';
    return this.http.get<[string, string, number][]>(url, { headers });
  }
}
