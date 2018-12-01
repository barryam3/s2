import { Component } from '@angular/core';
import { Router } from '@angular/router';

import { GetSongOptions } from '../song.service';
import { objectToParams } from '../../utils';

@Component({
  selector: 'app-filters',
  templateUrl: './filters.component.html',
  styleUrls: ['./filters.component.scss'],
})
export class FiltersComponent {
  filter: GetSongOptions = {
    suggested: null,
    arranged: null,
  };

  constructor(
    private router: Router,
  ) { }

  submit() {
    const queryParams = objectToParams(this.filter);
    this.router.navigate(['/songs'], { queryParams });
  }

}
