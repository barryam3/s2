import { NgModule } from '@angular/core';
import {
  MatSnackBarModule,
  MatInputModule,
  MatButtonModule,
  MatListModule,
  MatCardModule,
  MatToolbarModule,
} from '@angular/material';

@NgModule({
  imports: [
    MatSnackBarModule,
    MatInputModule,
    MatButtonModule,
    MatListModule,
    MatCardModule,
    MatToolbarModule,
  ],
  exports: [
    MatSnackBarModule,
    MatInputModule,
    MatButtonModule,
    MatListModule,
    MatCardModule,
    MatToolbarModule,
  ],
})
export class MatModule { }
