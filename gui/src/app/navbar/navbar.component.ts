import { Component, OnInit, Input } from '@angular/core';
import { Router } from '@angular/router';

import { User } from '../user';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss'],
})
export class NavbarComponent implements OnInit {
  @Input() user: User;

  constructor(private router: Router) { }

  ngOnInit() {
  }

  showFilters() {
    return this.router.url === '/songs';
  }

  showHome() {
    return this.router.url !== '/songs';
  }

}
