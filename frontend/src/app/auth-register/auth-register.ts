import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { RouterLink, Router } from '@angular/router'; 
import { HttpClient } from '@angular/common/http'; 

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './auth-register.html',
  styleUrls: ['./auth-register.css']
})
export class RegisterComponent implements OnInit {

  tipoRegistro: 'alumno' | 'operador' = 'alumno';

  // Formularios reactivos
  registerForm: FormGroup;
  operadorForm: FormGroup;
  
  // Catálogos
  facultades: any[] = [];
  carrerasTotales: any[] = [];
  carrerasDisponibles: any[] = [];
  fechaMaxima: string;
  mensajeErrorOperador: string = '';

  http = inject(HttpClient);
  router = inject(Router);

  constructor(private fb: FormBuilder) {
    const hoy = new Date();
    this.fechaMaxima = hoy.toISOString().split('T')[0];
    
    // FORMULARIO DEL ALUMNO
    this.registerForm = this.fb.group({
      nombre: ['', [Validators.required, Validators.pattern(/^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/)]],
      apellidos: ['', [Validators.required, Validators.pattern(/^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/)]],
      matricula: ['', [Validators.required, Validators.pattern(/^(201[8-9]|202[0-6])\d{5}$/)]],
      curp: ['', [Validators.required, Validators.pattern(/^[A-Z]{4}\d{6}[HM][A-Z]{5}[A-Z0-9]\d$/)]],      
      fecha_nacimiento: ['', Validators.required],
      facultad_id: ['', Validators.required],
      carrera_id: ['', Validators.required],
      email: ['', [Validators.required, Validators.pattern(/^[a-zA-Z0-9._%+-]+@alumno\.buap\.mx$/)]],
      password: ['', [Validators.required, Validators.minLength(8)]]
    });

    // FORMULARIO DEL OPERADOR
    this.operadorForm = this.fb.group({
      codigo_invitacion: ['', Validators.required],
      nombre: ['', [Validators.required, Validators.pattern(/^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/)]],
      apellidos: ['', [Validators.required, Validators.pattern(/^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/)]],
      email: ['', [Validators.required, Validators.email]], // Email normal, no forzosamente BUAP
      password: ['', [Validators.required, Validators.minLength(8)]]
    });
  }

  ngOnInit(): void {
    this.http.get('http://localhost:8000/api/catalogos/').subscribe({
      next: (res: any) => {
        this.facultades = res.facultades;
        this.carrerasTotales = res.carreras;
      },
      error: (err) => console.error('Error cargando catálogos', err)
    });
  }

  soloLetras(event: Event, controlName: string, esOperador: boolean = false): void {
    const input = event.target as HTMLInputElement;
    const valorFiltrado = input.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]/g, '');
    const form = esOperador ? this.operadorForm : this.registerForm;
    form.get(controlName)?.setValue(valorFiltrado, { emitEvent: false });
  }

  soloNumeros(event: Event, controlName: string): void {
    const input = event.target as HTMLInputElement;
    const valorFiltrado = input.value.replace(/[^0-9]/g, '');
    this.registerForm.get(controlName)?.setValue(valorFiltrado, { emitEvent: false });
  }

  soloLetrasYNumeros(event: Event, controlName: string, esOperador: boolean = false): void {
    const input = event.target as HTMLInputElement;
    const valorFiltrado = input.value.replace(/[^a-zA-Z0-9-]/g, '').toUpperCase();
    const form = esOperador ? this.operadorForm : this.registerForm;
    form.get(controlName)?.setValue(valorFiltrado, { emitEvent: false });
    if (controlName === 'codigo_invitacion') {
      this.mensajeErrorOperador = '';
    }
  }

  onFacultadChange(event: any): void {
    const facultadId = parseInt(event.target.value, 10);
    this.carrerasDisponibles = this.carrerasTotales.filter(c => c.facultad === facultadId);
    this.registerForm.get('carrera_id')?.setValue(''); 
  }

  // ENVÍO DE DATOS
  onSubmitAlumno(): void {
    if (this.registerForm.valid) {
      const payload = this.registerForm.value;
      this.http.post('http://localhost:8000/api/registro/alumno/', payload).subscribe({
        next: (res: any) => {
          alert('¡Registro de alumno exitoso! Ya puedes iniciar sesión.');
          this.router.navigate(['/login']); 
        },
        error: (err) => {
          console.error('Error en el registro', err);
          alert(err.error?.error || 'Ocurrió un error al registrar.');
        }
      });
    } else {
      this.registerForm.markAllAsTouched();
    }
  }

  onSubmitOperador(): void {
    this.mensajeErrorOperador = ''; 

    // Verificamos si el formulario está lleno y cumple el formato
    if (this.operadorForm.valid) {
      const payload = this.operadorForm.value;
      
      this.http.post('http://localhost:8000/api/registro/operador/', payload).subscribe({
        next: (res: any) => {
          alert('¡Registro de personal exitoso! Ya puedes iniciar sesión.');
          this.router.navigate(['/login']); 
        },
        error: (err) => {
          console.error('Error del backend:', err);
          // Obtenemos el texto del error que manda Django
          const mensaje = err.error?.error || 'El código ingresado es inválido o ya fue utilizado.';
          
          this.mensajeErrorOperador = mensaje;
          alert(' No se pudo registrar: ' + mensaje);
        }
      });
    } else {
      this.operadorForm.markAllAsTouched();
      alert(' Por favor, llena todos los campos obligatorios correctamente.');
    }
  }
}