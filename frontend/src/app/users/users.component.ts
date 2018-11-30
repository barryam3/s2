import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';

import { UserService, User } from '../user.service';
import { filterInPlace } from '../../utils';

@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.scss'],
})
export class UsersComponent implements OnInit, OnDestroy {
  users: User[];
  currentUser: User;
  userStream: Subscription;

  constructor(private userService: UserService) { }

  ngOnInit() {
    this.userStream = this.userService.currentUser.subscribe(currentUser => {
      this.currentUser = currentUser;
      if (this.currentUser) {
        this.userService.getUsers().subscribe(users => {
          this.users = users.filter(user => user.id !== currentUser.id);
        });
      }
    });
  }

  ngOnDestroy() {
    this.userStream.unsubscribe();
  }

  resetPassword(userID: number) {
    if (confirm('Are you sure you want to reset this user\'s password?')) {
      this.userService.resetPassword(userID).subscribe();
    }
  }

  setAdmin(userID: number, admin: boolean) {
    this.userService.editUserPermissions(userID, { admin })
      .subscribe(() => this.users.find(user => user.id === userID).admin = admin);
  }

  setActive(userID: number, active: boolean) {
    this.userService.editUserPermissions(userID, { active })
      .subscribe(() => this.users.find(user => user.id === userID).active = active);
  }

  delete(userID: number) {
    if (confirm('Are you sure you want to delete this user?')) {
      this.userService.deleteUser(userID).subscribe(() => {
        filterInPlace(this.users, user => user.id !== userID);
      });
    }
  }

}
