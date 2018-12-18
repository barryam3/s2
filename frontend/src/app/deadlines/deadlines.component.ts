import { Component, OnInit, OnDestroy } from '@angular/core';
import { MatSnackBar } from '@angular/material';

import { Subscription } from 'rxjs';

import { GroupService } from '../group.service';
import { UserService, User } from '../user.service';

@Component({
  selector: 'app-deadlines',
  templateUrl: './deadlines.component.html',
  styleUrls: ['./deadlines.component.scss'],
})
export class DeadlinesComponent implements OnInit, OnDestroy {
  // ISO date strings
  suggestDeadline = '';
  rateDeadline = '';

  currentUser: User;
  userStream: Subscription;

  constructor(
    private snackBar: MatSnackBar,
    private groupService: GroupService,
    private userService: UserService,
  ) { }

  ngOnInit() {
    this.userStream = this.userService.currentUser.subscribe(newCurrentUser => {
      this.currentUser = newCurrentUser;
      if (newCurrentUser) {
        this.suggestDeadline = newCurrentUser.group.suggestDeadline.toISOString();
        this.rateDeadline = newCurrentUser.group.rateDeadline.toISOString();
      }
    });
  }

  ngOnDestroy() {
    this.userStream.unsubscribe();
  }

  edit() {
    this.groupService.editDeadlines({
      suggestDeadline: new Date(this.suggestDeadline),
      rateDeadline: new Date(this.rateDeadline),
    })
      .subscribe(() => {
        this.snackBar.open('Deadlines updated.', 'dismiss');
        this.userService.getCurrentUser().subscribe(); // load new deadlines
      });
  }

}
