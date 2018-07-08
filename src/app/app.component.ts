import { Component, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';

import { filter, windowToggle } from 'rxjs/operators';

import { User } from './user';
import { UserService } from './user.service';
import { MatSnackBar } from '../../node_modules/@angular/material';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit {
  title = 'app';
  user: User;

  constructor(
    private router: Router,
    private userService: UserService,
    private snackBar: MatSnackBar,
  ) { }

  ngOnInit() {
    this.router.events
      .pipe(filter(e => e instanceof NavigationEnd))
      .subscribe(nav => this.getCurrentUser());
  }

  showNavbar() {
    return this.router.url === '/songs';
  }

  getCurrentUser() {
    this.userService.getCurrentUser()
      .subscribe(
        user => {
          this.user = user;
          if (window.location.pathname === '/') {
            this.router.navigateByUrl('/songs');
          }
        },
        error => {
          if (window.location.pathname !== '/login') {
            this.router.navigateByUrl('/login');
            this.snackBar.open('Your session timed out. Please log in again.', 'dismiss');
          }
        },
      );
  }
}
