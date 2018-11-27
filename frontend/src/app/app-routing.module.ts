import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { LoginComponent } from './login/login.component';
import { SongsComponent } from './songs/songs.component';
import { UsersComponent } from './users/users.component';
import { AccountComponent } from './account/account.component';
import { AppComponent } from './app.component';
import { AddSongComponent } from './add-song/add-song.component';
import { ManageSetlistComponent } from './manage-setlist/manage-setlist.component';
import { FiltersComponent } from './filters/filters.component';
import { SongPageComponent } from './song-page/song-page.component';

const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'songs', component: SongsComponent },
  { path: 'users', component: UsersComponent },
  { path: 'setlists', component: ManageSetlistComponent },
  { path: 'account', component: AccountComponent },
  { path: 'add-song', component: AddSongComponent },
  { path: 'filter', component: FiltersComponent },
  { path: 'song/:id', component: SongPageComponent },
  { path: '', component: AppComponent },
];

@NgModule({
  exports: [RouterModule],
  imports: [RouterModule.forRoot(routes)],
})
export class AppRoutingModule {}
