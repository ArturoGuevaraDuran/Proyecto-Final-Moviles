import { Component, inject } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http'; 
import { RouterLink, Router } from '@angular/router'; 

/**
 * @description Componente de autenticación encargado de validar credenciales
 * contra el backend de Django y obtener un Token de sesión.
 * @author Arturo Guevara
 */
@Component({
  selector: 'app-auth-login',
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './auth-login.html',
  styleUrls: ['./auth-login.css']
})
export class AuthLoginComponent {
  /** @property Formulario reactivo para capturar credenciales del usuario */
  loginForm: FormGroup;
  
  /** @property Servicio inyectado para realizar peticiones HTTP */
  http = inject(HttpClient); 
  router = inject(Router);

  constructor(private fb: FormBuilder) {
    // Definición de campos con validaciones mínimas de seguridad
    this.loginForm = this.fb.group({
      email: ['', [Validators.required]],
      password: ['', [Validators.required, Validators.minLength(4)]]
    });
  }

  /**
   * Procesa el intento de inicio de sesión.
   * Envía las credenciales al endpoint de Django y gestiona la respuesta del Token.
   * * @note Django REST Framework espera el campo 'username', por lo que 
   * el email del formulario se mapea a ese nombre de propiedad.
   */
  onSubmit(): void {
    if (this.loginForm.valid) {
      // Preparación del objeto de datos según el esquema de Django
      const loginData = {
        username: this.loginForm.value.email, 
        password: this.loginForm.value.password
      };

      // Petición POST al endpoint de autenticación
      this.http.post('http://localhost:8000/api/login/', loginData).subscribe({
        /** Gestión de éxito: El servidor devuelve un objeto con el token */
        next: (response: any) => {
          console.log('¡Login Exitoso!', response);
          localStorage.setItem('token', response.token);
          localStorage.setItem('rol', response.rol);
          localStorage.setItem('nombre', response.nombre);
          localStorage.setItem('user_id', response.user_id);

          // Redirección a la página principal del dashboard según el rol del usuario
          if (response.rol === 'ADMIN') {
            this.router.navigate(['/admin-panel']);
          } else if (response.rol === 'OPERADOR') {
            this.router.navigate(['/scanner']);
          } else {
            // Si es ALUMNO (o cualquier otro por defecto)
            this.router.navigate(['/student-dashboard']);
          }
        },
        /** Gestión de error: Credenciales no válidas o error de red */
        error: (err) => {
          console.error('Error al iniciar sesión', err);
          alert('Credenciales incorrectas o no existe el usuario. Por favor, inténtalo de nuevo.');
        }
      });
    }
  }
}