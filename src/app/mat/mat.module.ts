import { NgModule } from '@angular/core';
import {
  MatSnackBarModule,
  MatInputModule,
  MatButtonModule,
} from '@angular/material';

@NgModule({
  imports: [
    MatSnackBarModule,
    MatInputModule,
    MatButtonModule,
  ],
  exports: [
    MatSnackBarModule,
    MatInputModule,
    MatButtonModule,
  ],
})
export class MatModule { }
