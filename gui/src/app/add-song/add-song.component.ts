import { Component } from '@angular/core';
import { SongService } from '../song.service';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material';

@Component({
  selector: 'app-create-song',
  templateUrl: './add-song.component.html',
  styleUrls: ['./add-song.component.scss'],
})
export class AddSongComponent {
  title = '';
  artist = '';

  constructor(
    private songService: SongService,
    private router: Router,
    private snackBar: MatSnackBar,
  ) { }

  submit() {
    this.songService.addSong(this.title, this.artist)
      .subscribe(
        success => this.router.navigateByUrl('/songs'),
        failure => this.snackBar.open(failure.error, 'dismiss'),
      );
  }

}
