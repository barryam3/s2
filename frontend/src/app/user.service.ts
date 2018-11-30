import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable, BehaviorSubject } from 'rxjs';
import { tap, distinctUntilChanged } from 'rxjs/operators';

import { headers } from '../utils';

export interface User {
  id: number;
  username: string;
  active: boolean;
  admin: boolean;
}

@Injectable()
export class UserService {
  private userSubject = new BehaviorSubject<User>(null);
  public currentUser = this.userSubject.asObservable().pipe(distinctUntilChanged());

  constructor(private http: HttpClient) { }

  login(username: string, password: string): Observable<User> {
    const url = 'api/auth/login';
    const payload = {
      username,
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
    return this.http.post<boolean>(url, { headers })
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
    const url = 'api/users';
    return this.http.get<User[]>(url, { headers });
  }

  resetPassword(userID: number): Observable<boolean> {
    const url = `api/users/${userID}/password`;
    return this.http.delete<boolean>(url, { headers });
  }

  updateCurrentUserPassword(
    oldPassword: string,
    newPassword: string,
  ): Observable<boolean> {
    const url = 'api/users/me/password';
    const body = { oldPassword, newPassword };
    return this.http.put<boolean>(url, body, { headers });
  }

  addUser(username: string): Observable<User> {
    const url = 'api/users';
    const body = { username };
    return this.http.post<User>(url, body, { headers });
  }

  deleteUser(userID: number): Observable<boolean> {
    const url = `api/users/${userID}`;
    return this.http.delete<boolean>(url, { headers });
  }

  editUserPermissions(
    userID: number,
    userPermissions: { active?: boolean, admin?: boolean },
  ): Observable<boolean> {
    const url = `api/users/${userID}`;
    return this.http.patch<boolean>(url, userPermissions, { headers });
  }
}
