import { Component } from '@angular/core';
import { GroupService } from '../group.service';
import { MatSnackBar } from '@angular/material';

@Component({
  selector: 'app-reset-site',
  templateUrl: './reset-site.component.html',
  styleUrls: ['./reset-site.component.scss'],
})
export class ResetSiteComponent {

  constructor(
    private groupService: GroupService,
    private snackBar: MatSnackBar,
  ) { }

  reset() {
    this.groupService.unsuggestAll().subscribe(() => {
      this.snackBar.open('The site has been reset.', 'dismiss');
    });
  }

}
