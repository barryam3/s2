import { Component, Input } from '@angular/core';
import { SongOverview } from '../song.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-song-card',
  templateUrl: './song-card.component.html',
  styleUrls: ['./song-card.component.scss'],
})
export class SongCardComponent {
  @Input() song: SongOverview;

  constructor(private router: Router) { }

  navigate() {
    this.router.navigateByUrl(`/song/${this.song.id}`);
  }

}
