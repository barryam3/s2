import { Component, Input, Output, EventEmitter } from '@angular/core';
import { SongOverview } from '../song.service';

@Component({
  selector: 'app-song-card',
  templateUrl: './song-card.component.html',
  styleUrls: ['./song-card.component.scss'],
})
export class SongCardComponent {
  @Input() song: SongOverview;
  @Output() ratingChange = new EventEmitter<number>();

  onRatingChange({ rating }) {
    this.ratingChange.emit(rating);
  }

}
