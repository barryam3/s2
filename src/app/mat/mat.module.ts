import { NgModule } from '@angular/core';
import {
  MatSnackBarModule,
  MatInputModule,
  MatButtonModule,
  MatListModule,
  MatCardModule,
  MatToolbarModule,
  MatIconModule,
} from '@angular/material';

@NgModule({
  imports: [
    MatSnackBarModule,
    MatInputModule,
    MatButtonModule,
    MatListModule,
    MatCardModule,
    MatToolbarModule,
    MatIconModule,
  ],
  exports: [
    MatSnackBarModule,
    MatInputModule,
    MatButtonModule,
    MatListModule,
    MatCardModule,
    MatToolbarModule,
    MatIconModule,
  ],
})
export class MatModule { }
