import { Injectable } from '@angular/core';
import { HttpEvent, HttpInterceptor, HttpHandler, HttpRequest, HttpErrorResponse } from '@angular/common/http';
import { MatSnackBar } from '@angular/material';

import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

// ignore errors from URLs ending with these suffixes
const whitelist = [
  '/users/me',
];

@Injectable({
  providedIn: 'root',
})
export class HttpErrorInterceptor implements HttpInterceptor {

  constructor (private snackBar: MatSnackBar) {}

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(request).pipe(catchError((error: HttpErrorResponse) => {
      if (!error.url || !whitelist.some(suffix => error.url.endsWith(suffix))) {
        let errMsg = '';
        if (error.error instanceof ErrorEvent) { // Client Side Error
          errMsg = `Error: ${error.error.message}`;
        } else {  // Server Side Error
          if (error.status === 500 && !error.error) {
            errMsg = 'Error [500]: Something went wrong. Please try again. If the problem persists, inform the webmaster.';
          } else {
            errMsg = `Error [${error.status}]: ${error.error || error.statusText || error.message}`;
          }
        }
        this.snackBar.open(errMsg, 'dismiss', { duration: 5000 });
      }
      return throwError(error);
    }));
  }

}
