import { Component, OnInit } from '@angular/core';
import { UserService, ActiveUserOverview } from '../user.service';

@Component({
  selector: 'app-engagement',
  templateUrl: './engagement.component.html',
  styleUrls: ['./engagement.component.scss'],
})
export class EngagementComponent implements OnInit {
  dataSource: ActiveUserOverview[];
  displayedColumns: string[] = ['username', 'numSuggestions', 'numRatings'];

  constructor(private userService: UserService) { }

  ngOnInit() {
    this.userService.getActiveUsers().subscribe(activeUsers => {
      this.dataSource = activeUsers;
    });
  }

}
