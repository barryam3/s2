import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material';

import { SongService, Solo } from '../song.service';

const soloOptions = Object.keys(Solo).map(key => ({ key, value: Solo[key] }));

@Component({
  selector: 'app-create-song',
  templateUrl: './add-song.component.html',
  styleUrls: ['./add-song.component.scss'],
})
export class AddSongComponent {
  title = '';
  artist = '';
  solo: Solo = Solo.None;

  soloOptions = soloOptions;

  constructor(
    private songService: SongService,
    private router: Router,
    private snackBar: MatSnackBar,
  ) { }

  submit() {
    this.songService.addSong(this.title, this.artist, this.solo)
      .subscribe(
        success => this.router.navigateByUrl('/songs'),
        failure => this.snackBar.open(failure.error, 'dismiss'),
      );
  }

}
