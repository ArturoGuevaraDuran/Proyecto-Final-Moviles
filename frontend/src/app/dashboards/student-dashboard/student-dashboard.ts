import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-student-dashboard',
  standalone: true,
  imports: [CommonModule], 
  templateUrl: './student-dashboard.html',
  styleUrls: ['./student-dashboard.css']
})
export class StudentDashboardComponent implements OnInit {
  nombreAlumno: string = '';
  menusDisponibles: any[] = [];
  reservaActiva: any = null;

  http = inject(HttpClient);

  ngOnInit(): void {
    this.nombreAlumno = localStorage.getItem('nombre') || 'Alumno';
    this.cargarMenu();
  }

  private getHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    return new HttpHeaders({
      'Authorization': `Token ${token}`
    });
  }

  cargarMenu(): void {
    this.http.get('http://localhost:8000/api/alumnos/menu/', { headers: this.getHeaders() })
      .subscribe({
        next: (res: any) => {
          console.log('Menú descargado:', res);
          this.menusDisponibles = res;
        },
        error: (err) => {
          console.error('Error de conexión:', err);
        }
      });
  }

  reservarComida(menuId: number): void {
    const payload = { menu_id: menuId };
    
    this.http.post('http://localhost:8000/api/alumnos/reservar/', payload, { headers: this.getHeaders() })
      .subscribe({
        next: (res: any) => {
          console.log('Reserva exitosa:', res);
          this.reservaActiva = res;
        },
        error: (err) => {
          console.error('Error al reservar', err);
          alert(err.error?.error || 'No se pudo procesar la reserva.');
        }
      });
  }
}