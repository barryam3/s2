import { Component, OnInit } from '@angular/core';

import { SongService, SongOverview } from '../song.service';

@Component({
  selector: 'app-songs',
  templateUrl: './songs.component.html',
  styleUrls: ['./songs.component.scss'],
})
export class SongsComponent implements OnInit {
  songs: SongOverview[];

  constructor(private songService: SongService) { }

  ngOnInit() {
    // TODO: dynamically load pages
    this.songService.getSongs({ current: true, size: 1000 })
      .subscribe(songs => {
        this.songs = songs;
      });
  }

}
