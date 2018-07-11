import { NgModule } from '@angular/core';
import {
  MatSnackBarModule,
  MatInputModule,
  MatButtonModule,
  MatListModule,
  MatCardModule,
  MatToolbarModule,
  MatIconModule,
  MatMenuModule,
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
    MatMenuModule,
  ],
  exports: [
    MatSnackBarModule,
    MatInputModule,
    MatButtonModule,
    MatListModule,
    MatCardModule,
    MatToolbarModule,
    MatIconModule,
    MatMenuModule,
  ],
})
export class MatModule { }
