import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material';

import { GroupService } from '../group.service';

const now = new Date();

@Component({
  selector: 'app-edit-deadlines',
  templateUrl: './edit-deadlines.component.html',
  styleUrls: ['./edit-deadlines.component.scss'],
})
export class EditDeadlinesComponent implements OnInit {
  // ISO date strings
  newSuggestDeadline = '';
  newVoteDeadline = '';

  constructor(
    private snackBar: MatSnackBar,
    private groupService: GroupService,
  ) { }

  ngOnInit() {
    this.groupService.getDeadlines().subscribe(deadlines => {
      if (deadlines.suggestDeadline) {
        this.newSuggestDeadline = deadlines.suggestDeadline.toISOString();
      }
      if (deadlines.voteDeadline) {
        this.newVoteDeadline = deadlines.voteDeadline.toISOString();
      }
    });
  }

  edit() {
    this.groupService.editDeadlines({
      suggestDeadline: new Date(this.newSuggestDeadline),
      voteDeadline: new Date(this.newVoteDeadline),
    })
      .subscribe(() => this.snackBar.open('Deadlines updated.', 'dismiss'));
  }

}
