import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ServiceWorkerModule } from '@angular/service-worker';

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
import { DeadlinesComponent } from './deadlines/deadlines.component';
import { FindSongsComponent } from './find-songs/find-songs.component';
import { SongPageComponent } from './song-page/song-page.component';
import { AddUserComponent } from './add-user/add-user.component';
import { ResetSiteComponent } from './reset-site/reset-site.component';
import { LinksComponent } from './links/links.component';
import { CommentsComponent } from './comments/comments.component';
import { CommentComponent } from './comment/comment.component';
import { RatingsComponent } from './ratings/ratings.component';
import { TriStateCheckboxComponent } from './tri-state-checkbox/tri-state-checkbox.component';
import { EngagementComponent } from './engagement/engagement.component';

import { UserService } from './user.service';
import { SongService } from './song.service';
import { GroupService } from './group.service';
import { CommentService } from './comment.service';
import { LinkService } from './link.service';

import { CustomStarRatingConfigService } from './custom-star-rating-config.service';
import { HttpErrorInterceptor } from './http-error-interceptor';

import { environment } from '../environments/environment';

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
    DeadlinesComponent,
    FindSongsComponent,
    SongPageComponent,
    AddUserComponent,
    ResetSiteComponent,
    LinksComponent,
    CommentsComponent,
    CommentComponent,
    RatingsComponent,
    TriStateCheckboxComponent,
    EngagementComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule,
    BrowserAnimationsModule,
    StarRatingModule.forRoot(),
    AppRoutingModule,
    MatModule,
    ServiceWorkerModule.register('ngsw-worker.js', { enabled: environment.production }),
  ],
  providers: [
    SongService,
    UserService,
    GroupService,
    CommentService,
    LinkService,
    { provide: StarRatingConfigService, useClass: CustomStarRatingConfigService },
    { provide: HTTP_INTERCEPTORS, useClass: HttpErrorInterceptor, multi: true },
  ],
  bootstrap: [AppComponent],
})
export class AppModule { }
