import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Observable } from 'rxjs';

@Injectable()
export class AuthService {
  private BASE_URL = 'api/auth';
  private headers: HttpHeaders = new HttpHeaders({
    'Content-Type': 'application/json',
  });

  constructor(private http: HttpClient) { }

  login(username: string, password: string): Observable<boolean> {
    const url = `${this.BASE_URL}/login`;
    const payload = {
      username,
      password,
    };
    return this.http.post<boolean>(url, payload, { headers: this.headers });
  }
}
