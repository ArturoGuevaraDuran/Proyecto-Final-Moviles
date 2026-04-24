import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { RouterLink, Router } from '@angular/router'; 
import { HttpClient } from '@angular/common/http'; 

/**
 * @description Componente principal para el registro de nuevos estudiantes en el sistema.
 * Implementa un formulario reactivo con validaciones, descarga catálogos dinámicos desde Django
 * y envía el payload estructurado para su almacenamiento en PostgreSQL.
 * @author Arturo Guevara
 */
@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './auth-register.html',
  styleUrls: ['./auth-register.css']
})
export class RegisterComponent implements OnInit {
  /** * @property {FormGroup} registerForm 
   * @description Instancia del formulario reactivo que agrupa y valida los controles de entrada de datos del alumno.
   */
  registerForm: FormGroup;
  
  /** * @property {Array<any>} facultades 
   * @description Almacena el catálogo de facultades obtenido desde el backend.
   */
  facultades: any[] = [];

  /** * @property {Array<any>} carrerasTotales 
   * @description Almacena el catálogo completo de carreras obtenido desde el backend.
   */
  carrerasTotales: any[] = [];

  /** * @property {Array<any>} carrerasDisponibles 
   * @description Arreglo dinámico filtrado que muestra únicamente las carreras correspondientes a la facultad seleccionada.
   */
  carrerasDisponibles: any[] = [];

  fechaMaxima: string;

  /** @property {HttpClient} http - Servicio inyectado para realizar peticiones HTTP al backend de Django. */
  http = inject(HttpClient);

  /** @property {Router} router - Servicio inyectado para manejar la navegación entre vistas. */
  router = inject(Router);

  /**
   * @constructor
   * @param {FormBuilder} fb - Servicio para la construcción simplificada de formularios reactivos.
   * @description Inicializa el formulario estableciendo los campos esperados por el backend y sus validaciones.
   */
  constructor(private fb: FormBuilder) {
    const hoy = new Date();
    this.fechaMaxima = hoy.toISOString().split('T')[0];
    this.registerForm = this.fb.group({
      // Solo letras (incluyendo acentos y ñ) y espacios.
      nombre: ['', [Validators.required, Validators.pattern(/^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/)]],
      apellidos: ['', [Validators.required, Validators.pattern(/^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/)]],
      // Años de ingreso entre 2018 y 2026, seguidos exactamente por 5 dígitos numéricos.
      matricula: ['', [Validators.required, Validators.pattern(/^(201[8-9]|202[0-6])\d{5}$/)]],
      // Validación de CURP estándar (18 caracteres)
      curp: ['', [Validators.required, Validators.pattern(/^[A-Z]{4}\d{6}[HM][A-Z]{5}[A-Z0-9]\d$/)]],      
      fecha_nacimiento: ['', Validators.required],
      facultad_id: ['', Validators.required],
      carrera_id: ['', Validators.required],
      // Restringe el registro exclusivamente a correos institucionales.
      email: ['', [Validators.required, Validators.pattern(/^[a-zA-Z0-9._%+-]+@alumno\.buap\.mx$/)]],
      password: ['', [Validators.required, Validators.minLength(8)]]
    });
  }

  /**
   * @method ngOnInit
   * @description Se ejecuta automáticamente al inicializar el componente.
   * Realiza una petición GET al endpoint de Django para llenar los selectores de facultad y carrera.
   * @returns {void}
   */
  ngOnInit(): void {
    this.http.get('http://localhost:8000/api/catalogos/').subscribe({
      next: (res: any) => {
        this.facultades = res.facultades;
        this.carrerasTotales = res.carreras;
      },
      error: (err) => console.error('Error cargando catálogos', err)
    });
  }

  /**
   * @method soloLetras
   * @description Filtra la entrada del usuario en tiempo real, eliminando cualquier carácter que no sea una letra o espacio.
   * @param {Event} event - El evento DOM disparado por el input de texto.
   * @param {string} controlName - El nombre exacto del FormControl dentro del FormGroup.
   * @returns {void}
   */
  soloLetras(event: Event, controlName: string): void {
    const input = event.target as HTMLInputElement;
    const valorFiltrado = input.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]/g, '');
    this.registerForm.get(controlName)?.setValue(valorFiltrado, { emitEvent: false });
  }

  /**
   * @method soloNumeros
   * @description Filtra la entrada del usuario en tiempo real, permitiendo exclusivamente caracteres numéricos (0-9).
   * @param {Event} event - El evento DOM disparado por el input de texto.
   * @param {string} controlName - El nombre exacto del FormControl dentro del FormGroup.
   * @returns {void}
   */
  soloNumeros(event: Event, controlName: string): void {
    const input = event.target as HTMLInputElement;
    const valorFiltrado = input.value.replace(/[^0-9]/g, '');
    this.registerForm.get(controlName)?.setValue(valorFiltrado, { emitEvent: false });
  }

  /**
   * @method soloLetrasYNumeros
   * @description Filtra la entrada en tiempo real, permitiendo exclusivamente letras y números.
   * Además, convierte el texto a mayúsculas automáticamente para mantener el formato estándar.
   * @param {Event} event - El evento DOM disparado por el input.
   * @param {string} controlName - El nombre del FormControl a modificar.
   * @returns {void}
   */
  soloLetrasYNumeros(event: Event, controlName: string): void {
    const input = event.target as HTMLInputElement;
    // Reemplaza todo lo que no sea letra (a-z) o número (0-9) por vacío, y lo pasa a mayúsculas
    const valorFiltrado = input.value.replace(/[^a-zA-Z0-9]/g, '').toUpperCase();
    this.registerForm.get(controlName)?.setValue(valorFiltrado, { emitEvent: false });
  }

  /**
   * @method onFacultadChange
   * @description Maneja el cambio en el selector de Facultades.
   * Filtra y actualiza el arreglo carrerasDisponibles basado en el ID de la facultad seleccionada.
   * @param {any} event - Evento DOM que contiene el valor (ID) seleccionado en el <select>.
   * @returns {void}
   */
  onFacultadChange(event: any): void {
    // Se convierte a entero para asegurar la coincidencia con el tipo de dato de la llave foránea en Django
    const facultadId = parseInt(event.target.value, 10);
    
    this.carrerasDisponibles = this.carrerasTotales.filter(c => c.facultad === facultadId);
    
    // Resetea el control de 'carrera_id' para obligar al usuario a elegir una opción válida.
    this.registerForm.get('carrera_id')?.setValue(''); 
  }

  /**
   * @method onSubmit
   * @description Intercepta el envío del formulario, valida los datos y realiza un POST al backend.
   * En caso de éxito, redirige al login; si hay error (ej. correo duplicado), notifica al usuario.
   * @returns {void}
   */
  onSubmit(): void {
    if (this.registerForm.valid) {
      const payload = this.registerForm.value;
      
      this.http.post('http://localhost:8000/api/registro/alumno/', payload).subscribe({
        next: (res: any) => {
          alert('¡Registro exitoso! Ya puedes iniciar sesión en el sistema.');
          this.router.navigate(['/login']); 
        },
        error: (err) => {
          console.error('Error en el registro', err);
          // Notifica errores específicos provenientes del backend
          alert(err.error?.error || 'Ocurrió un error al registrar.');
        }
      });
    } else {
      // Activa las validaciones visuales en la interfaz
      this.registerForm.markAllAsTouched();
    }
  }
}