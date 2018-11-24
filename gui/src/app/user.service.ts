import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Observable, BehaviorSubject } from 'rxjs';
import { tap, distinctUntilChanged } from 'rxjs/operators';

export interface User {
  id: string;
  athena: string;
  current: boolean;
  pitch: boolean;
}

const headers: HttpHeaders = new HttpHeaders({
  'Content-Type': 'application/json',
});

@Injectable()
export class UserService {
  private userSubject = new BehaviorSubject<User>(null);
  public currentUser = this.userSubject.asObservable().pipe(distinctUntilChanged());

  constructor(private http: HttpClient) { }

  login(athena: string, password: string): Observable<User> {
    const url = '/api/auth/login';
    const payload = {
      athena,
      password,
    };
    return this.http.post<User>(url, payload, { headers })
      .pipe(tap(
        user => this.userSubject.next(user),
        () => this.userSubject.next(null),
      ));
  }

  logout(): Observable<boolean> {
    const url = 'api/auth/logout';
    return this.http.get<boolean>(url, { headers })
    .pipe(tap(
      () => this.userSubject.next(null),
      () => this.userSubject.next(null),
    ));
  }

  getCurrentUser(): Observable<User> {
    const url = 'api/users/me';
    return this.http.get<User>(url, { headers })
      .pipe(tap(
        user => this.userSubject.next(user),
        () => this.userSubject.next(null),
      ));
  }

  getUsers(): Observable<User[]> {
    const url = '/api/users/';
    return this.http.get<User[]>(url, { headers });
  }

  resetPassword(userID: number): Observable<boolean> {
    const url = `/api/users/${userID}/password`;
    return this.http.delete<boolean>(url, { headers });
  }

  updateCurrentUserPassword(oldPassword: string, newPassword: string): Observable<boolean> {
    const url = `/api/users/me/password`;
    const payload = { oldPassword, newPassword };
    return this.http.put<boolean>(url, payload, { headers });
  }

}
