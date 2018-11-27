import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { StarRatingModule, StarRatingConfigService } from 'angular-star-rating';

import { AppRoutingModule } from './app-routing.module';
import { MatModule } from './mat/mat.module';

import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { SongsComponent } from './songs/songs.component';
import { UsersComponent } from './users/users.component';
import { AccountComponent } from './account/account.component';
import { SongCardComponent } from './song-card/song-card.component';
import { AddSongComponent } from './add-song/add-song.component';
import { NavbarComponent } from './navbar/navbar.component';
import { ManageSetlistComponent } from './manage-setlist/manage-setlist.component';
import { FiltersComponent } from './filters/filters.component';

import { UserService } from './user.service';
import { SongService } from './song.service';
import { SetlistService } from './setlist.service';
import { CustomStarRatingConfigService } from './custom-star-rating-config.service';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    SongsComponent,
    UsersComponent,
    AccountComponent,
    SongCardComponent,
    NavbarComponent,
    AddSongComponent,
    ManageSetlistComponent,
    FiltersComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule,
    BrowserAnimationsModule,
    StarRatingModule.forRoot(),
    AppRoutingModule,
    MatModule,
  ],
  providers: [
    SongService,
    UserService,
    SetlistService,
    { provide: StarRatingConfigService, useClass: CustomStarRatingConfigService },
  ],
  bootstrap: [AppComponent],
})
export class AppModule { }
