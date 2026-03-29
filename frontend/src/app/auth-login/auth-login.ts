import { Component, inject } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http'; 

@Component({
  selector: 'app-auth-login',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './auth-login.html',
  styleUrls: ['./auth-login.css']
})
export class AuthLoginComponent {
  loginForm: FormGroup;
  http = inject(HttpClient); 

  constructor(private fb: FormBuilder) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required]],
      password: ['', [Validators.required, Validators.minLength(4)]]
    });
  }

  onSubmit() {
    if (this.loginForm.valid) {
      const loginData = {
        username: this.loginForm.value.email, 
        password: this.loginForm.value.password
      };

      this.http.post('http://localhost:8000/api/login/', loginData).subscribe({
        next: (response: any) => {
          console.log('¡Login Exitoso!', response);
          alert('¡Funciona! Tu token es: ' + response.token);
        },
        error: (err) => {
          console.error('Error al iniciar sesión', err);
          alert('Credenciales incorrectas');
        }
      });

    }
  }
}