import { Component, Input } from '@angular/core';
import { Router } from '@angular/router';
import { Location } from '@angular/common';

import { User, UserService } from '../user.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss'],
})
export class NavbarComponent {
  @Input() user: User;

  constructor(
    private router: Router,
    private location: Location,
    private userService: UserService,
  ) { }

  showFilters() {
    return this.router.url.startsWith('/songs');
  }

  showHome() {
    return !this.showFilters();
  }

  logout() {
    this.userService.logout().subscribe(() => this.router.navigateByUrl('/login'));
  }

  back() {
    this.router.navigateByUrl('/songs?suggested=1');
  }

}
