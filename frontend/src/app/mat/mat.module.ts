import { NgModule } from '@angular/core';
import {
  MatSnackBarModule,
  MatInputModule,
  MatButtonModule,
  MatCardModule,
  MatToolbarModule,
  MatIconModule,
  MatMenuModule,
  MatDatepickerModule,
  MatNativeDateModule,
  MatRadioModule,
  MatBadgeModule,
  MatChipsModule,
  MatCheckboxModule,
} from '@angular/material';

const modules = [
  MatSnackBarModule,
  MatInputModule,
  MatButtonModule,
  MatCardModule,
  MatToolbarModule,
  MatIconModule,
  MatMenuModule,
  MatDatepickerModule,
  MatNativeDateModule,
  MatRadioModule,
  MatBadgeModule,
  MatChipsModule,
  MatCheckboxModule,
];

@NgModule({
  imports: modules,
  exports: modules,
})
export class MatModule { }
