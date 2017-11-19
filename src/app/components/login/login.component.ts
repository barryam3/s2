import { Component, OnInit } from '@angular/core';

import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  message = 'The API is not working!';

  constructor(private auth: AuthService) { }

  ngOnInit() {
    this.auth.test()
      .subscribe(msg => this.message = msg);
  }

}
