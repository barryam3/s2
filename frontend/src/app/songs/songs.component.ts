import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { SongService, SongOverview, GetSongOptions } from '../song.service';

@Component({
  selector: 'app-songs',
  templateUrl: './songs.component.html',
  styleUrls: ['./songs.component.scss'],
})
export class SongsComponent implements OnInit {
  @Input() filters: GetSongOptions;
  songs: SongOverview[];

  constructor(
    private songService: SongService,
    private route: ActivatedRoute,
  ) { }

  ngOnInit() {
    if (this.filters) {
      this.getSongs(this.filters);
    } else {
      this.route.queryParams.subscribe(queryParams => {
        const filters: GetSongOptions = {};
        if (queryParams.suggested) {
          filters.suggested = queryParams.suggested === '1';
        }
        this.getSongs(filters);
      });
    }
  }

  getSongs = (filters: GetSongOptions) => {
    this.songService.getSongs(filters).subscribe(songs => {
      this.songs = songs;
    });
  }

}
