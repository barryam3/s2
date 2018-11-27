import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { filter } from 'rxjs/operators';

import { SetlistService, Setlist } from '../setlist.service';
import { SongFilters } from '../song.service';

@Component({
  selector: 'app-filters',
  templateUrl: './filters.component.html',
  styleUrls: ['./filters.component.scss'],
})
export class FiltersComponent implements OnInit {
  currentSetlist: Setlist;
  suggested: boolean | null = null;

  constructor(
    private setlistService: SetlistService,
    private router: Router,
  ) { }

  ngOnInit() {
    this.setlistService.currentSetlist
      .pipe(filter(newCurrentSetlist => newCurrentSetlist !== undefined))
      .subscribe(newCurrentSetlist => {
        this.currentSetlist = newCurrentSetlist;
      });
  }

  submit() {
    const queryParams = {};
    if (this.suggested !== null) {
      queryParams['suggested'] = this.suggested ? 1 : 0;
    }
    this.router.navigate(['/songs'], { queryParams });
  }

}
