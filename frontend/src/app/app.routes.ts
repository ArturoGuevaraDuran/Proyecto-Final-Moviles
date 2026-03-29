import { Routes } from '@angular/router';
import { AuthLoginComponent } from './auth-login/auth-login';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: AuthLoginComponent }
];