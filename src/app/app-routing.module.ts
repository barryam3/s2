import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { LoginComponent } from './login/login.component';
import { SongsComponent } from './songs/songs.component';
import { UsersComponent } from './users/users.component';
import { AccountComponent } from './account/account.component';
import { AppComponent } from './app.component';

const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'songs', component: SongsComponent },
  { path: 'users', component: UsersComponent },
  { path: 'account', component: AccountComponent },
  { path: '', component: AppComponent },
];

@NgModule({
  exports: [RouterModule],
  imports: [RouterModule.forRoot(routes)],
})
export class AppRoutingModule {}
