import { Component, Input } from '@angular/core';
import { Router, NavigationEnd, ActivatedRoute, Params, UrlHandlingStrategy } from '@angular/router';

import { User, UserService } from '../user.service';
import { homepage } from '../../utils';
import { filter, first } from 'rxjs/operators';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss'],
})
export class NavbarComponent {
  @Input() user: User;
  homepage = homepage;
  lastParams: Params;

  constructor(
    private router: Router,
    private userService: UserService,
    route: ActivatedRoute,
  ) {
    router.events
      .pipe(filter(e => e instanceof NavigationEnd && this.isSongPageURL(e.urlAfterRedirects)))
      .subscribe(() => {
        route.queryParams.pipe(first()).subscribe(params => {
          this.lastParams = params;
        });
      });
  }

  get onSongPage(): boolean {
    return this.isSongPageURL(this.router.url);
  }

  isSongPageURL(url: string): boolean {
    return url.startsWith('/songs');
  }

  logout() {
    this.userService.logout().subscribe(() => this.router.navigateByUrl('/login'));
  }
}
