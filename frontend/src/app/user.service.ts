import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable, BehaviorSubject } from 'rxjs';
import { map, tap, distinctUntilChanged } from 'rxjs/operators';

import { headers } from '../utils';
import { Deadlines, DeadlinesJSON, jsonToDeadlines } from './group.service';

export interface UserOverview {
  id: number;
  username: string;
  active: boolean;
  admin: boolean;
}

interface UserData {
  id: number;
  username: string;
  active: boolean;
  admin: boolean;
  group: DeadlinesJSON;
}

export class User {
  id: number;
  username: string;
  active: boolean;
  admin: boolean;
  group: Deadlines;

  constructor(userData: UserData) {
    this.id = userData.id;
    this.username = userData.username;
    this.active = userData.active;
    this.admin = userData.admin;
    this.group = jsonToDeadlines(userData.group);
  }

  get canSuggest() {
    return this.group.suggestDeadline > new Date();
  }

  get canRate() {
    return this.active && (this.group.rateDeadline > new Date());
  }
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
    return this.http.post<UserData>(url, payload, { headers })
      .pipe(
        map(userData => userData ? new User(userData) : null),
        tap(
          user => this.userSubject.next(user),
          () => this.userSubject.next(null),
        ),
      );
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
    return this.http.get<UserData>(url, { headers })
      .pipe(
        map(userData => userData ? new User(userData) : null),
        tap(
          user => this.userSubject.next(user),
          () => this.userSubject.next(null),
        ),
      );
  }

  getUsers(): Observable<UserOverview[]> {
    const url = 'api/users';
    return this.http.get<UserOverview[]>(url, { headers });
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
