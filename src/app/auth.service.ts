import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs/observable';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';

import { MessageService } from './message.service';


@Injectable()
export class AuthService {
  private BASE_URL = 'api/auth';
  private headers: HttpHeaders = new HttpHeaders({
    'Content-Type': 'application/json',
  });

  constructor(
    private http: HttpClient,
    private messageService: MessageService
   ) { }

  login(username: string, password: string): Observable<boolean> {
    const url = `${this.BASE_URL}/login`;
    const payload = {
      username,
      password,
    };
    this.messageService.add("Trying to log in.");
    return this.http.post<boolean>(url, payload, { headers: this.headers });
  }
}
