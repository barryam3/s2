import { Component, OnInit, Input } from '@angular/core';

import { User } from '../user';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss'],
})
export class NavbarComponent implements OnInit {
  @Input() user: User;

  constructor() { }

  ngOnInit() {
  }

}
