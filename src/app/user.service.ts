import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';

import { Observable } from 'rxjs';

import { User } from './user';

@Injectable()
export class UserService {
  private BASE_URL = 'api/user';
  private headers: HttpHeaders = new HttpHeaders({
    'Content-Type': 'application/json',
  });

  constructor(private http: HttpClient) { }

  getUsers(): Observable<User[]> {
    const url = `${this.BASE_URL}/`;
    return this.http.get<User[]>(url, { headers: this.headers });
  }

  getCurrentUser(): Observable<User> {
    const url = `${this.BASE_URL}/current`;
    return this.http.get<User>(url, { headers: this.headers });
  }

  resetPassword(userID): Observable<boolean> {
    const url = `${this.BASE_URL}/${userID}/password`;
    return this.http.delete<boolean>(url, { headers: this.headers });
  }

  updatePassword(userID, oldPassword, newPassword): Observable<boolean> {
    const url = `${this.BASE_URL}/${userID}/password`;
    const payload = { oldPassword, newPassword };
    return this.http.put<boolean>(url, payload, { headers: this.headers });
  }

}
