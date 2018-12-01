import { Component } from '@angular/core';
import { Router } from '@angular/router';

import { GetSongOptions } from '../song.service';
import { objectToParams } from '../../utils';

function mergeBools(t: boolean, f: boolean): boolean | null {
  if (t && f) {
    return null;
  }

  if (t) {
    return true;
  }

  return false;
}

@Component({
  selector: 'app-filters',
  templateUrl: './filters.component.html',
  styleUrls: ['./filters.component.scss'],
})
export class FiltersComponent {
  filter: GetSongOptions = {};
  suggested = true;
  notSuggested = true;
  arranged = true;
  notArranged = true;

  constructor(
    private router: Router,
  ) { }

  submit() {
    this.filter.suggested = mergeBools(this.suggested, this.notSuggested);
    this.filter.arranged = mergeBools(this.arranged, this.notArranged);
    const queryParams = objectToParams(this.filter);
    this.router.navigate(['/songs'], { queryParams });
  }

  onCheck(keyToFlip: string, { checked }) {
    if (checked === false && !this[keyToFlip]) {
      this[keyToFlip] = true;
    }
  }

}
