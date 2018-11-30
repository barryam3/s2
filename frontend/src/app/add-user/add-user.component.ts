import { Component } from '@angular/core';
import { UserService } from '../user.service';
import { MatSnackBar } from '@angular/material';

@Component({
  selector: 'app-add-user',
  templateUrl: './add-user.component.html',
  styleUrls: ['./add-user.component.scss'],
})
export class AddUserComponent {
  username = '';

  constructor(
    private userService: UserService,
    private snackBar: MatSnackBar,
  ) { }
  submit() {
    this.userService.addUser(this.username)
      .subscribe(() => {
        this.snackBar.open('User added.', 'dismiss');
        this.username = '';
      });
  }

}
