import { Routes } from '@angular/router';
import { AuthLoginComponent } from './auth-login/auth-login';
import { RegisterComponent } from './auth-register/auth-register'; 
import { StudentDashboardComponent } from './dashboards/student-dashboard/student-dashboard';
import { OperatorScannerComponent } from './dashboards/operator-scanner/operator-scanner';
import { AdminPanel } from './dashboards/admin-panel/admin-panel';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: AuthLoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'student-dashboard', component: StudentDashboardComponent },
  { path: 'scanner', component: OperatorScannerComponent },
  { path: 'admin-panel', component: AdminPanel },
];