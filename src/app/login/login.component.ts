import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material';

import { AuthService } from '../auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent implements OnInit {
  username: '';
  password: '';
  season: any = 'Spring 2018';

  constructor(
    private auth: AuthService,
    private router: Router,
    private snackBar: MatSnackBar,
   ) {}

  calculateSeason() {
    const today = new Date();
    let year = today.getFullYear();
    const month = today.getMonth();
    let fall = false;
    // if it's between apr & sep, assume Fall semester
    if (month >= 3 && month <= 8) {
      fall = true;
    }
    // if it's oct/nov/dec, show spring of next year
    if (!fall && month >= 9) {
      year += 1;
    }
    this.season = `${fall ? 'Fall' : 'Spring'} ${year}`;
  }

  login() {
    this.auth.login(this.username, this.password)
      .subscribe(
        success => {
          this.router.navigateByUrl('/songs');
        },
        failure => {
          if (failure.status === 504) {
            this.snackBar.open('Unable to connect to server.', 'dismiss');
          } else {
            this.snackBar.open('Unsuccessful signin attempt.', 'dismiss');
          }
        },
      );
  }

  ngOnInit() {
    this.auth.logout().subscribe(success => console.log(success));
    this.calculateSeason();
  }

}
