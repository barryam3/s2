import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { dateToInt, headers, intToDate } from '../utils';

export interface Deadlines {
  rateDeadline: Date;
  suggestDeadline: Date;
}

export interface DeadlinesJSON {
  rateDeadline: number;
  suggestDeadline: number;
}

// 30 Dec 9999 20:59:59 (max for display accounting for timezones)
const MAX_TIMESTAMP = 253402221599;

export function jsonToDeadlines(json: DeadlinesJSON): Deadlines {
  return {
    rateDeadline: intToDate(json.rateDeadline || MAX_TIMESTAMP),
    suggestDeadline: intToDate(json.suggestDeadline || MAX_TIMESTAMP),
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
      rateDeadline: dateToInt(deadlines.rateDeadline),
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
