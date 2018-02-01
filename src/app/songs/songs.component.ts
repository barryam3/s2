import { Component, OnInit } from '@angular/core';

import { SongService } from '../song.service';

@Component({
  selector: 'app-songs',
  templateUrl: './songs.component.html',
  styleUrls: ['./songs.component.css'],
})
export class SongsComponent implements OnInit {

  constructor(private song: SongService) { }

  ngOnInit() {
    this.song.getSongs().subscribe(songs => console.log(songs));
  }

}
