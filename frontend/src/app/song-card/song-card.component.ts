import { Component, Input } from '@angular/core';

import { SongOverview } from '../song.service';

@Component({
  selector: 'app-song-card',
  templateUrl: './song-card.component.html',
  styleUrls: ['./song-card.component.scss'],
})
export class SongCardComponent {
  @Input() song: SongOverview;

  showDetails() {
    // TODO: song page
  }

}
