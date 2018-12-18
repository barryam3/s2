import { Component } from '@angular/core';
import { Router } from '@angular/router';

import { GetSongOptions, SortOptions } from '../song.service';
import { objectToParams } from '../../utils';

@Component({
  selector: 'app-find-songs',
  templateUrl: './find-songs.component.html',
  styleUrls: ['./find-songs.component.scss'],
})
export class FindSongsComponent {
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
