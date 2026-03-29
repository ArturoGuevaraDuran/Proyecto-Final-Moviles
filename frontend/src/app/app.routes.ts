import { Routes } from '@angular/router';
import { AuthLoginComponent } from './auth-login/auth-login';
import { RegisterComponent } from './auth-register/auth-register'; 

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: AuthLoginComponent },
  { path: 'register', component: RegisterComponent } 
];