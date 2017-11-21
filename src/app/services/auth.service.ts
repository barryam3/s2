import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs/observable';


@Injectable()
export class AuthService {
  private BASE_URL = 'api';
  private headers: HttpHeaders = new HttpHeaders({
    'Content-Type': 'application/json',
  });

  constructor(private http: HttpClient) { }

  test(): Observable<string> {
    return this.http.get<string>(`${this.BASE_URL}/`);
  }

  // login(user): Observable<any> {
  //   let url: string = `${this.BASE_URL}/login`;
  //   return this.http.post(url, user, {headers: this.headers});
  // }
  // register(user): Observable<any> {
  //   let url: string = `${this.BASE_URL}/register`;
  //   return this.http.post(url, user, {headers: this.headers});
  // }

}
