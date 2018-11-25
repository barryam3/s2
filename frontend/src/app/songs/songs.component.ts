import { Component, OnInit } from '@angular/core';
import { filter } from 'rxjs/operators';

import { SetlistService } from '../setlist.service';
import { SongService, SongOverview } from '../song.service';

@Component({
  selector: 'app-songs',
  templateUrl: './songs.component.html',
  styleUrls: ['./songs.component.scss'],
})
export class SongsComponent implements OnInit {
  songs: SongOverview[];

  constructor(
    private setlistService: SetlistService,
    private songService: SongService,
  ) { }

  ngOnInit() {
    // TODO: dynamically load pages
    this.setlistService.currentSetlist
      .pipe(filter(setlist => setlist !== null))
      .subscribe(({ id }) => {
        this.songService.getSuggestions(id)
          .subscribe(songs => {
            this.songs = songs;
          });
      });
  }

}
