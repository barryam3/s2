import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
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
import { EditDeadlinesComponent } from './edit-deadlines/edit-deadlines.component';
import { FiltersComponent } from './filters/filters.component';
import { SongPageComponent } from './song-page/song-page.component';
import { CustomStarRatingConfigService } from './custom-star-rating-config.service';

import { UserService } from './user.service';
import { SongService } from './song.service';
import { GroupService } from './group.service';

import { HttpErrorInterceptor } from './http-error-interceptor';
import { AddUserComponent } from './add-user/add-user.component';

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
    EditDeadlinesComponent,
    FiltersComponent,
    SongPageComponent,
    AddUserComponent,
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
    GroupService,
    { provide: StarRatingConfigService, useClass: CustomStarRatingConfigService },
    { provide: HTTP_INTERCEPTORS, useClass: HttpErrorInterceptor, multi: true },
  ],
  bootstrap: [AppComponent],
})
export class AppModule { }
