import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { FormsModule } from '@angular/forms'; // Necesario para el buscador (ngModel)

/**
 * @description Panel principal de Administración. Gestiona métricas en vivo, 
 * logística de operadores y soporte a alumnos.
 * @author Arturo Guevara
 * @version 1.0.0
 */
@Component({
  selector: 'app-admin-panel',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-panel.html',
  styleUrls: ['./admin-panel.css']
})
export class AdminPanel implements OnInit {
  nombreAdmin: string = '';
  // Controla qué vista se está mostrando en la pantalla principal
  vistaActual: 'metricas' | 'operadores' | 'soporte' = 'metricas';

  http = inject(HttpClient);

  // --- VARIABLES DE MÓDULOS ---
  
  // Métricas
  estadisticas = {
    totalReservas: 0,
    entregadas: 0,
    pendientes: 0
  };

  // Operadores
  codigoInvitacionGenerado: string | null = null;

  // Soporte
  busquedaMatricula: string = '';
  alumnoEncontrado: any = null;

  ngOnInit(): void {
    this.nombreAdmin = localStorage.getItem('nombre') || 'Administrador';
    this.cargarMetricasEnVivo();
  }

  /**
   * @description Genera las cabeceras de autorización exigidas por Django REST.
   */
  private getHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    return new HttpHeaders({
      'Authorization': `Token ${token}`
    });
  }

  /**
   * @description Cambia la pestaña activa en el panel lateral.
   * @param vista El nombre de la vista a mostrar.
   */
  cambiarVista(vista: 'metricas' | 'operadores' | 'soporte'): void {
    this.vistaActual = vista;
    if (vista === 'metricas') this.cargarMetricasEnVivo();
  }

  // ==========================================
  // LÓGICA DE MÓDULOS (Conexiones a Django)
  // ==========================================

 cargarMetricasEnVivo(): void {
    this.http.get('http://localhost:8000/api/admin/metricas/', { headers: this.getHeaders() })
      .subscribe({
        next: (res: any) => {
          this.estadisticas = res;
        },
        error: (err) => console.error('Error al cargar métricas', err)
      });
  }

  generarCodigoOperador(): void {
    this.http.post('http://localhost:8000/api/admin/generar-token/', {}, { headers: this.getHeaders() })
      .subscribe({
        next: (res: any) => {
          this.codigoInvitacionGenerado = res.codigo;
        },
        error: (err) => {
          console.error('Error al generar código', err);
          alert('No tienes permisos de Administrador o el servidor falló.');
        }
      });
  }
  buscarAlumno(): void {
    if (!this.busquedaMatricula) return;
    
    // TODO: Conectar con endpoint GET en Django buscando por matrícula
    console.log('Buscando matrícula:', this.busquedaMatricula);
    // Simulación temporal:
    if (this.busquedaMatricula === '202294250') {
      this.alumnoEncontrado = {
        nombre: 'Arturo Guevara',
        estadoQR: 'RESERVADO',
        comidasRestantesMensuales: 18
      };
    } else {
      alert('Alumno no encontrado');
      this.alumnoEncontrado = null;
    }
  }

  cancelarReserva(alumnoId: number): void {
    const confirmar = confirm('¿Estás seguro de cancelar esta reserva y liberar la ración?');
    if (confirmar) {
      console.log('Reserva cancelada para el alumno', alumnoId);
      this.alumnoEncontrado.estadoQR = 'CANCELADO';
      // TODO: Petición HTTP DELETE/POST a Django
    }
  }
}