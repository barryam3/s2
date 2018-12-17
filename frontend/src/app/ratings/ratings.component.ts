import { Component, OnInit } from '@angular/core';
import { GroupService } from '../group.service';

@Component({
  selector: 'app-ratings',
  templateUrl: './ratings.component.html',
  styleUrls: ['./ratings.component.scss'],
})
export class RatingsComponent implements OnInit {
  dataSource: [string, string, number][];
  displayedColumns: string[] = ['title', 'artist', 'avgRating'];

  constructor(private groupService: GroupService) { }

  ngOnInit() {
    this.groupService.getRatings().subscribe(rows => {
      this.dataSource = rows;
    });
  }

}
