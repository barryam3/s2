import { Component, OnInit, OnDestroy, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Subscription } from 'rxjs';

import { SongService, SongOverview, GetSongOptions } from '../song.service';
import { UserService, User } from '../user.service';

@Component({
  selector: 'app-songs',
  templateUrl: './songs.component.html',
  styleUrls: ['./songs.component.scss'],
})
export class SongsComponent implements OnInit, OnDestroy {
  @Input() filters: GetSongOptions;
  songs: SongOverview[];
  currentUser: User;
  userStream: Subscription;

  constructor(
    private songService: SongService,
    private userService: UserService,
    private route: ActivatedRoute,
  ) { }

  ngOnInit() {
    if (this.filters) {
      this.getSongs(this.filters);
    } else {
      this.route.queryParams.subscribe(queryParams => {
        const filters: GetSongOptions = {
          ...queryParams,
        };
        if (queryParams.suggested) {
          filters.suggested = queryParams.suggested === '1';
        }
        if (queryParams.arranged) {
          filters.arranged = queryParams.arranged === '1';
        }
        this.getSongs(filters);
      });
    }
    this.userStream = this.userService.currentUser.subscribe(newCurrentUser => {
      this.currentUser = newCurrentUser;
    });
  }

  ngOnDestroy() {
    this.userStream.unsubscribe();
  }

  getSongs = (filters: GetSongOptions) => {
    this.songService.getSongs(filters).subscribe(songs => {
      this.songs = songs || [];
    });
  }

}
