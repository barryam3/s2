import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material';
import { filter } from 'rxjs/operators';

import { SongService } from '../song.service';
import { SetlistService, Setlist } from '../setlist.service';

@Component({
  selector: 'app-create-song',
  templateUrl: './add-song.component.html',
  styleUrls: ['./add-song.component.scss'],
})
export class AddSongComponent implements OnInit {
  title = '';
  artist = '';
  currentSetlist: Setlist;

  constructor(
    private songService: SongService,
    private setlistService: SetlistService,
    private router: Router,
    private snackBar: MatSnackBar,
  ) { }

  ngOnInit() {
    this.setlistService.currentSetlist
      .pipe(filter(newCurrentSetlist => newCurrentSetlist !== undefined))
      .subscribe(newCurrentSetlist => {
        this.currentSetlist = newCurrentSetlist;
      });
  }

  submit() {
    const autosuggest = this.currentSetlist ? this.currentSetlist.id : 0;
    this.songService.addSong(this.title, this.artist, autosuggest)
      .subscribe(
        success => this.router.navigateByUrl('/songs'),
        failure => this.snackBar.open(failure.error, 'dismiss'),
      );
  }

}
