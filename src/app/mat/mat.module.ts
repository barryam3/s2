import { NgModule } from '@angular/core';
import {
  MatSnackBarModule,
  MatInputModule,
  MatButtonModule,
  MatListModule,
  MatCardModule,
} from '@angular/material';

@NgModule({
  imports: [
    MatSnackBarModule,
    MatInputModule,
    MatButtonModule,
    MatListModule,
    MatCardModule,
  ],
  exports: [
    MatSnackBarModule,
    MatInputModule,
    MatButtonModule,
    MatListModule,
    MatCardModule,
  ],
})
export class MatModule { }
