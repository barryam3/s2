import { Component, Input } from '@angular/core';
import { Router } from '@angular/router';
import { Location } from '@angular/common';

import { User } from '../user.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss'],
})
export class NavbarComponent {
  @Input() user: User;

  constructor(private router: Router, private location: Location) { }

  showFilters() {
    return this.router.url.startsWith('/songs');
  }

  showHome() {
    return !this.showFilters();
  }

  back() {
    this.location.back();
  }

}
