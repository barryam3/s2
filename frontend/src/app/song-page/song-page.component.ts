import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Subscription, Subject } from 'rxjs';

import { SongService, Song } from '../song.service';
import { UserService, User } from '../user.service';
import { homepage } from '../../utils';

@Component({
  selector: 'app-song-page',
  templateUrl: './song-page.component.html',
  styleUrls: ['./song-page.component.scss'],
})
export class SongPageComponent implements OnInit, OnDestroy {
  song: Song; // TODO: full song
  currentUser: User;
  userStream: Subscription;

  editing = false;
  title = '';
  artist = '';
  lyrics = '';
  arranged = false;

  commitSubject: Subject<void> = new Subject<void>();
  cancelSubject: Subject<void> = new Subject<void>();

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private songService: SongService,
    private userService: UserService,
  ) { }

  ngOnInit() {
    const id = parseInt(this.route.snapshot.paramMap.get('id'), 10);
    this.songService.getSong(id).subscribe(song => {
      this.song = song;
      this.title = song.title;
      this.artist = song.artist;
      this.lyrics = song.lyrics;
      this.arranged = song.arranged;
    });
    this.userStream = this.userService.currentUser.subscribe(newCurrentUser => {
      this.currentUser = newCurrentUser;
    });
  }

  ngOnDestroy() {
    this.userStream.unsubscribe();
  }

  startEdit() {
    this.title = this.song.title;
    this.artist = this.song.artist;
    this.lyrics = this.song.lyrics;
    this.editing = true;
    this.arranged = this.song.arranged;
  }

  commitEdit() {
    this.editing = false;
    this.songService.updateSong(this.song.id, {
      title: this.title,
      artist: this.artist,
      lyrics: this.lyrics,
      arranged: this.arranged,
    }).subscribe(() => {
      this.song.title = this.title;
      this.song.artist = this.artist;
      this.song.lyrics = this.lyrics;
      this.song.arranged = this.arranged;
    });
    this.commitSubject.next();
  }

  cancelEdit() {
    this.editing = false;
    this.cancelSubject.next();
  }

  doDelete() {
    if (confirm('Are you sure you want to delete this song?')) {
      this.songService.deleteSong(this.song.id)
        .subscribe(() => this.router.navigate(homepage.route, { queryParams: homepage.queryParams }));
    }
  }

  setSuggested(suggested: boolean) {
    this.songService.updateSong(this.song.id, { suggested })
      .subscribe(() => {
        this.song.suggestor = suggested ? this.currentUser.username : null;
      });
  }

  onRatingChange(event: { rating: number }) {
    this.songService.rateSong(this.song.id, event.rating)
      .subscribe(() => {
        this.song.myRating = event.rating;
      });
  }

}
