import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';

import { AppComponent } from './app.component';
import { MessagesComponent } from './messages/messages.component';
import { LoginComponent } from './login/login.component';
import { SongsComponent } from './songs/songs.component';

import { AuthService } from './auth.service';
import { MessageService } from './message.service';
import { SongService } from './song.service';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    MessagesComponent,
    SongsComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    AppRoutingModule,
    HttpClientModule,
  ],
  providers: [
    AuthService,
    MessageService,
    SongService,
  ],
  bootstrap: [AppComponent],
})
export class AppModule { }
