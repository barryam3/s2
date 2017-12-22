import { Component, OnInit } from '@angular/core';

import { AuthService } from '../auth.service';
import { MessageService, Context } from '../message.service';

import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent implements OnInit {
  username: '';
  password: '';
  season: any = 'Spring 2018';

  constructor(
    private auth: AuthService,
    private msg: MessageService,
    private router: Router
   ) {}

  calculateSeason() {
    let today = new Date();
    let year = today.getFullYear()
    let month = today.getMonth()
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
        success => this.router.navigateByUrl('/songs'),
        failure => this.msg.add('Login unsuccessful.', Context.Danger),
      );
  }

  ngOnInit() {
    this.calculateSeason();
  }

}
