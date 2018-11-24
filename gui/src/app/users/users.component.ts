import { Component, OnInit } from '@angular/core';

import { UserService, User } from '../user.service';

@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.scss'],
})
export class UsersComponent implements OnInit {
  users: User[];

  constructor(private user: UserService) { }

  ngOnInit() {
    this.user.getUsers().subscribe(users => {
      this.users = users;
    });
  }

  resetPassword(userID) {
    this.user.resetPassword(userID).subscribe();
  }

}
