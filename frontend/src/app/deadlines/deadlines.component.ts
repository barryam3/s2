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
        const suggestDeadline = new Date(newCurrentUser.group.suggestDeadline.getTime());
        const rateDeadline = new Date(newCurrentUser.group.rateDeadline.getTime());
        // show last active day, not first inactive day
        [suggestDeadline, rateDeadline].forEach(date => date.setDate(date.getDate() - 1));
        this.suggestDeadline = suggestDeadline.toISOString();
        this.rateDeadline = rateDeadline.toISOString();
      }
    });
  }

  ngOnDestroy() {
    this.userStream.unsubscribe();
  }

  edit() {
    const suggestDeadline = new Date(this.suggestDeadline);
    const rateDeadline = new Date(this.rateDeadline);
    [suggestDeadline, rateDeadline].forEach(date => {
      date.setDate(date.getDate() + 1); // end of selected day
      date.setMinutes(-1 * date.getTimezoneOffset()); // clear local timezone
      date.setUTCHours(10); // midnight in Hawaii
    });
    this.groupService.editDeadlines({ suggestDeadline, rateDeadline })
      .subscribe(() => {
        this.snackBar.open('Deadlines updated.', 'dismiss');
        this.userService.getCurrentUser().subscribe(); // load new deadlines
      });
  }

}
