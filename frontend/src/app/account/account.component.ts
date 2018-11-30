import { Component, OnInit, OnDestroy } from '@angular/core';
import { MatSnackBar } from '@angular/material';
import { Subscription } from 'rxjs';

import { UserService, User } from '../user.service';

@Component({
  selector: 'app-account',
  templateUrl: './account.component.html',
  styleUrls: ['./account.component.scss'],
})
export class AccountComponent implements OnInit, OnDestroy {
  currentUser: User;
  userStream: Subscription;
  oldPassword: '';
  newPassword: '';
  newPasswordConf: '';

  constructor(
    private user: UserService,
    private snackBar: MatSnackBar,
  ) { }

  ngOnInit() {
    this.user.currentUser.subscribe(user => this.currentUser = user);
  }

  ngOnDestroy() {
    this.userStream.unsubscribe();
  }

  changePassword() {
    if (this.newPassword !== this.newPasswordConf) {
      this.snackBar.open('Passwords do not match.', 'dismiss');
      return;
    }

    this.user.updateCurrentUserPassword(this.oldPassword, this.newPassword)
      .subscribe(() => this.snackBar.open('Your password has been updated.', 'dismiss'));
  }

}
