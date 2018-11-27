import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';
import { MatSnackBar } from '@angular/material';
import { filter } from 'rxjs/operators';

import { SongService, SongOverview } from '../song.service';
import { SetlistService, Setlist } from '../setlist.service';

@Component({
  selector: 'app-song-page',
  templateUrl: './song-page.component.html',
  styleUrls: ['./song-page.component.scss'],
})
export class SongPageComponent implements OnInit {
  song: SongOverview; // TODO: full song
  currentSetlist: Setlist;

  editing = false;
  title = '';
  artist = '';
  lyrics = '';

  constructor(
    private route: ActivatedRoute,
    private songService: SongService,
    private setlistService: SetlistService,
    private snackBar: MatSnackBar,
    private location: Location,
  ) { }

  ngOnInit() {
    const id = parseInt(this.route.snapshot.paramMap.get('id'), 10);
    this.setlistService.currentSetlist
      .pipe(filter(newCurrentSetlist => newCurrentSetlist !== undefined))
      .subscribe(newCurrentSetlist => {
        const setlistID = newCurrentSetlist ? newCurrentSetlist.id : 0;
        this.songService.getSong(id, setlistID).subscribe(song => {
          this.song = song;
          this.title = song.title;
          this.artist = song.artist;
          this.lyrics = song.lyrics;
        });
      });
  }

  edit() {
    this.title = this.song.title;
    this.artist = this.song.artist;
    this.lyrics = this.song.lyrics;
    this.editing = true;
  }

  save() {
    this.editing = false;
    this.songService.updateSong(this.song.id, {
      title: this.title,
      artist: this.artist,
      lyrics: this.lyrics,
      arranged: false, // TODO
    }).subscribe(
      success => {
        this.song.title = this.title;
        this.song.artist = this.artist;
        this.song.lyrics = this.lyrics;
      },
      failure => this.snackBar.open(failure.error, 'dismiss'),
    );
  }

  delete() {
    this.songService.deleteSong(this.song.id).subscribe(
      success => this.location.back(),
      failure => this.snackBar.open(failure.error, 'dismiss'),
    );
  }

}
