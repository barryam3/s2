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
  MatDatepickerModule,
  MatNativeDateModule,
} from '@angular/material';

const modules = [
  MatSnackBarModule,
  MatInputModule,
  MatButtonModule,
  MatListModule,
  MatCardModule,
  MatToolbarModule,
  MatIconModule,
  MatMenuModule,
  MatDatepickerModule,
  MatNativeDateModule,
];

@NgModule({
  imports: modules,
  exports: modules,
})
export class MatModule { }
