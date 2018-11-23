import { Component, OnInit, Input } from '@angular/core';

import { Song } from '../song';

@Component({
  selector: 'app-song-card',
  templateUrl: './song-card.component.html',
  styleUrls: ['./song-card.component.scss'],
})
export class SongCardComponent implements OnInit {
  @Input() song: Song;

  constructor() { }

  ngOnInit() {
  }

  showDetails() {
    // TODO: song page
    window.location.href = `http://xprod.mit.edu/SetSelection/viewsong.php?song=${this.song.id}`;
  }

}