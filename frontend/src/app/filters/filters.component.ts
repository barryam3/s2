import { Component } from '@angular/core';
import { Router } from '@angular/router';

import { GetSongOptions, SortOptions } from '../song.service';
import { objectToParams } from '../../utils';

@Component({
  selector: 'app-filters',
  templateUrl: './filters.component.html',
  styleUrls: ['./filters.component.scss'],
})
export class FiltersComponent {
  filter: GetSongOptions = {
    title: '',
    artist: '',
    suggestor: '',
    suggested: true,
    arranged: null,
    sort: SortOptions.Edited,
  };

  SortOptions = Object.entries(SortOptions);

  constructor(
    private router: Router,
  ) { }

  submit() {
    const queryParams = objectToParams(this.filter);
    this.router.navigate(['/songs'], { queryParams });
  }

}
