import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { combineLatest } from 'rxjs';
import { filter } from 'rxjs/operators';

import { SongService, SongOverview, SongFilters } from '../song.service';
import { SetlistService, Setlist } from '../setlist.service';
import { MatSnackBar } from '@angular/material';

@Component({
  selector: 'app-songs',
  templateUrl: './songs.component.html',
  styleUrls: ['./songs.component.scss'],
})
export class SongsComponent implements OnInit {
  @Input() filters: SongFilters;
  currentSetlist: Setlist;
  songs: SongOverview[];

  constructor(
    private songService: SongService,
    private setlistService: SetlistService,
    private route: ActivatedRoute,
    private snackBar: MatSnackBar,
  ) { }

  ngOnInit() {
    if (this.filters) {
      this.getSongs(this.filters);
    } else {
      combineLatest(
        this.setlistService.currentSetlist
          .pipe(filter(newCurrentSetlist => newCurrentSetlist !== null)),
        this.route.queryParams,
      )
        .subscribe(([newCurrentSetlist, queryParams]) => {
          const filters: SongFilters = {
            setlistID: newCurrentSetlist.id,
          };
          if (queryParams.suggested) {
            filters.suggested = queryParams.suggested === '1';
          }
          this.getSongs(filters);
        });
    }
  }

  getSongs = (filters: SongFilters) => {
    this.songService.getSongs(filters).subscribe(songs => {
      this.songs = songs;
    });
  }

  updateRating(song: SongOverview, newRating: number) {
    this.songService.rateSuggestion(song.suggestion.id, newRating)
      .subscribe(
        success => song.suggestion.myRating = newRating,
        failure => this.snackBar.open(failure.error, 'dismiss'),
      );
  }

}
