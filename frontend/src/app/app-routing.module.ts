import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { LoginComponent } from './login/login.component';
import { SongsComponent } from './songs/songs.component';
import { UsersComponent } from './users/users.component';
import { AccountComponent } from './account/account.component';
import { AppComponent } from './app.component';
import { AddSongComponent } from './add-song/add-song.component';
import { FindSongsComponent } from './find-songs/find-songs.component';
import { SongPageComponent } from './song-page/song-page.component';
import { AddUserComponent } from './add-user/add-user.component';
import { RatingsComponent } from './ratings/ratings.component';
import { DeadlinesComponent } from './deadlines/deadlines.component';
import { ResetSiteComponent } from './reset-site/reset-site.component';
import { EngagementComponent } from './engagement/engagement.component';

const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'songs', component: SongsComponent },
  { path: 'song/:id', component: SongPageComponent },
  { path: 'find-songs', component: FindSongsComponent },
  { path: 'add-song', component: AddSongComponent },
  { path: 'account', component: AccountComponent },
  { path: 'deadlines', component: DeadlinesComponent },
  { path: 'users', component: UsersComponent },
  { path: 'add-user', component: AddUserComponent },
  { path: 'ratings', component: RatingsComponent },
  { path: 'reset', component: ResetSiteComponent },
  { path: 'engagement', component: EngagementComponent },
  { path: '', component: AppComponent },
];

@NgModule({
  exports: [RouterModule],
  imports: [RouterModule.forRoot(routes)],
})
export class AppRoutingModule {}
