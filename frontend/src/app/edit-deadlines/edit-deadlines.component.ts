import { Component, OnInit, OnDestroy } from '@angular/core';
import { MatSnackBar } from '@angular/material';

import { Subscription } from 'rxjs';

import { GroupService } from '../group.service';
import { UserService } from '../user.service';

@Component({
  selector: 'app-edit-deadlines',
  templateUrl: './edit-deadlines.component.html',
  styleUrls: ['./edit-deadlines.component.scss'],
})
export class EditDeadlinesComponent implements OnInit, OnDestroy {
  // ISO date strings
  newSuggestDeadline = '';
  newRateDeadline = '';

  userStream: Subscription;

  constructor(
    private snackBar: MatSnackBar,
    private groupService: GroupService,
    private userService: UserService,
  ) { }

  ngOnInit() {
    this.userStream = this.userService.currentUser.subscribe(newCurrentUser => {
      if (newCurrentUser) {
        this.newSuggestDeadline = newCurrentUser.group.suggestDeadline.toISOString();
        this.newRateDeadline = newCurrentUser.group.rateDeadline.toISOString();
      }
    });
  }

  ngOnDestroy() {
    this.userStream.unsubscribe();
  }

  edit() {
    this.groupService.editDeadlines({
      suggestDeadline: new Date(this.newSuggestDeadline),
      rateDeadline: new Date(this.newRateDeadline),
    })
      .subscribe(() => {
        this.snackBar.open('Deadlines updated.', 'dismiss');
        this.userService.getCurrentUser().subscribe(); // load new deadlines
      });
  }

}
