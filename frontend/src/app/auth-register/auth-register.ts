import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { RouterLink, Router } from '@angular/router'; 

/**
 * @description Componente encargado de gestionar el registro de nuevos estudiantes.
 * Incluye validaciones específicas para la BUAP (matrícula y correo institucional).
 * @author Arturo Guevara
 */
@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './auth-register.html',
  styleUrls: ['./auth-register.css']
})
export class RegisterComponent {
  /** @property Formulario reactivo para la captura de datos del alumno */
  registerForm: FormGroup;
  
  /** @property Listado dinámico de carreras según la facultad seleccionada */
  carrerasDisponibles: string[] = [];

  /** @property Catálogo de facultades y sus respectivas carreras */
  facultades = [
    {
      nombre: 'Ciencias de la Computación',
      carreras: [
        'Ingeniería en Ciencias de la Computación', 
        'Licenciatura en Ciencias de la Computación', 
        'Ingeniería en Tecnologías de la Información'
      ]
    },
    {
      nombre: 'Ingeniería',
      carreras: [
        'Ingeniería Civil', 
        'Ingeniería Industrial', 
        'Ingeniería Mecánica', 
        'Ingeniería Mecatrónica',
      ]
    }
  ];

  constructor(private fb: FormBuilder, private router: Router) {
    // Configuración inicial del formulario con validaciones personalizadas
    this.registerForm = this.fb.group({
      nombre: ['', [Validators.required, Validators.pattern(/^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/)]],
      // Validación de matrícula: Acepta años 2018-2026 seguidos de 5 dígitos
      matricula: ['', [Validators.required, Validators.pattern(/^(201[8-9]|202[0-6])\d{5}$/)]],
      facultad: ['', Validators.required],
      carrera: ['', Validators.required],
      // Restricción de dominio exclusivo para alumnos BUAP
      email: ['', [Validators.required, Validators.pattern(/^[a-zA-Z0-9._%+-]+@alumno\.buap\.mx$/)]],
      password: ['', [Validators.required, Validators.minLength(8)]]
    });
  }

  /**
   * Filtra la entrada del usuario para permitir únicamente letras y espacios en tiempo real.
   * @param event Evento de entrada del teclado
   * @param controlName Nombre del control del formulario a limpiar
   */
  soloLetras(event: Event, controlName: string): void {
    const input = event.target as HTMLInputElement;
    const valorFiltrado = input.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]/g, '');
    this.registerForm.get(controlName)?.setValue(valorFiltrado, { emitEvent: false });
  }

  /**
   * Filtra la entrada del usuario para permitir únicamente números en tiempo real.
   * @param event Evento de entrada del teclado
   * @param controlName Nombre del control del formulario a limpiar
   */
  soloNumeros(event: Event, controlName: string): void {
    const input = event.target as HTMLInputElement;
    const valorFiltrado = input.value.replace(/[^0-9]/g, '');
    this.registerForm.get(controlName)?.setValue(valorFiltrado, { emitEvent: false });
  }

  /**
   * Actualiza el listado de carreras disponibles basado en la selección de facultad.
   * @param event Evento de cambio en el selector de facultades
   */
  onFacultadChange(event: any): void {
    const facultadSeleccionada = event.target.value;
    const facultad = this.facultades.find(f => f.nombre === facultadSeleccionada);
    
    this.carrerasDisponibles = facultad ? facultad.carreras : [];
    this.registerForm.get('carrera')?.setValue(''); // Limpiar selección previa
  }

  /**
   * Procesa el envío del formulario. Redirige al login si los datos son válidos,
   * de lo contrario, marca los errores en la interfaz.
   */
  onSubmit(): void {
    if (this.registerForm.valid) {
      console.log('Datos validados listos para enviar:', this.registerForm.value);
      alert('¡Registro exitoso! Redirigiendo al inicio de sesión...');
      this.router.navigate(['/login']); 
    } else {
      // Activa los mensajes de error visuales en todos los campos
      this.registerForm.markAllAsTouched();
    }
  }
}