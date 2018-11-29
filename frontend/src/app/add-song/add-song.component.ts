import { Component } from '@angular/core';
import { Router } from '@angular/router';

import { SongService } from '../song.service';

@Component({
  selector: 'app-create-song',
  templateUrl: './add-song.component.html',
  styleUrls: ['./add-song.component.scss'],
})
export class AddSongComponent {
  title = '';
  artist = '';

  constructor(private songService: SongService, private router: Router) { }

  submit() {
    this.songService.addSong(this.title, this.artist)
      .subscribe(() => this.router.navigateByUrl('/songs'));
  }

}
