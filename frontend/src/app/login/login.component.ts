import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { UserService } from '../user.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent implements OnInit {
  username: '';
  password: '';
  season = '';

  constructor(private user: UserService, private router: Router) {}

  ngOnInit() {
    this.calculateSeason();
  }

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
    this.user.login(this.username, this.password)
      .subscribe(() => this.router.navigateByUrl('/songs?suggested=1'));
  }

}
