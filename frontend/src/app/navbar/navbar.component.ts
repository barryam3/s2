import { Component, Input } from '@angular/core';
import { Router } from '@angular/router';

import { User, UserService } from '../user.service';
import { homepageURL } from '../../utils';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss'],
})
export class NavbarComponent {
  @Input() user: User;

  constructor(
    private router: Router,
    private userService: UserService,
  ) { }

  get onSongPage() {
    return this.router.url.startsWith('/songs');
  }

  logout() {
    this.userService.logout().subscribe(() => this.router.navigateByUrl('/login'));
  }

  back() {
    this.router.navigateByUrl(homepageURL);
  }

}
