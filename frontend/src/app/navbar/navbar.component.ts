import { Component, Input, OnInit } from '@angular/core';
import { Router, NavigationEnd, ActivatedRoute, Params } from '@angular/router';

import { User, UserService } from '../user.service';
import { homepage } from '../../utils';
import { filter, first } from 'rxjs/operators';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss'],
})
export class NavbarComponent implements OnInit {
  @Input() user: User;
  homepage = homepage;
  lastParams: Params = homepage.queryParams;

  constructor(
    private router: Router,
    private userService: UserService,
    private route: ActivatedRoute,
  ) {
    router.events
      .pipe(filter(e => e instanceof NavigationEnd && this.isSongsPageURL(e.urlAfterRedirects)))
      .subscribe(() => {
        route.queryParams.pipe(first()).subscribe(params => {
          this.lastParams = params;
        });
      });
  }

  ngOnInit() {
    if (this.onSongsPage) {
      this.route.queryParams.pipe(first()).subscribe(params => {
        this.lastParams = params;
      });
    }
  }

  get onSongsPage(): boolean {
    return this.isSongsPageURL(this.router.url);
  }

  isSongsPageURL(url: string): boolean {
    return url.startsWith('/songs');
  }

  logout() {
    this.userService.logout().subscribe(() => this.router.navigateByUrl('/login'));
  }
}
