import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';

import { SongService, Song } from '../song.service';

@Component({
  selector: 'app-song-page',
  templateUrl: './song-page.component.html',
  styleUrls: ['./song-page.component.scss'],
})
export class SongPageComponent implements OnInit {
  song: Song; // TODO: full song

  editing = false;
  title = '';
  artist = '';
  lyrics = '';

  constructor(
    private route: ActivatedRoute,
    private songService: SongService,
    private location: Location,
  ) { }

  ngOnInit() {
    const id = parseInt(this.route.snapshot.paramMap.get('id'), 10);
    this.songService.getSong(id).subscribe(song => {
      this.song = song;
      this.title = song.title;
      this.artist = song.artist;
      this.lyrics = song.lyrics;
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
    }).subscribe(() => {
      this.song.title = this.title;
      this.song.artist = this.artist;
      this.song.lyrics = this.lyrics;
    });
  }

  delete() {
    this.songService.deleteSong(this.song.id)
      .subscribe(() => this.location.back());
  }

  onRatingChange(event: { rating: number }) {
    this.songService.rateSong(this.song.id, event.rating)
      .subscribe(() => {
        this.song.myRating = event.rating;
      });
  }

}
