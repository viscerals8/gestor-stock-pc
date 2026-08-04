import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink, RouterLinkActive } from '@angular/router';
import {
  IonApp, IonRouterOutlet, IonSplitPane, IonMenu, IonHeader, IonToolbar,
  IonTitle, IonContent, IonList, IonItem, IonLabel, IonIcon, IonMenuToggle,
  IonNote,
} from '@ionic/angular/standalone';
import { addIcons } from 'ionicons';
import {
  homeOutline, hardwareChipOutline, addCircleOutline, phonePortraitOutline,
  listOutline, timeOutline, documentTextOutline, logOutOutline,
} from 'ionicons/icons';
import { AuthService } from './core/services/auth.service';

interface PaginaMenu {
  titulo: string;
  url: string;
  icono: string;
}

@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  styleUrls: ['app.component.scss'],
  imports: [
    CommonModule, RouterLink, RouterLinkActive,
    IonApp, IonRouterOutlet, IonSplitPane, IonMenu, IonHeader, IonToolbar,
    IonTitle, IonContent, IonList, IonItem, IonLabel, IonIcon, IonMenuToggle,
    IonNote,
  ],
})
export class AppComponent {
  paginas: PaginaMenu[] = [
    { titulo: 'Dashboard', url: '/dashboard-tecnico', icono: 'home-outline' },
    { titulo: 'Inventario de PCs', url: '/inventario', icono: 'hardware-chip-outline' },
    { titulo: 'Registrar PC', url: '/registro-pc', icono: 'add-circle-outline' },
    { titulo: 'Celulares', url: '/listado-celulares', icono: 'phone-portrait-outline' },
    { titulo: 'Gestión de Tareas', url: '/gestion-tareas', icono: 'list-outline' },
    { titulo: 'Historial de PCs', url: '/historial-pcs', icono: 'time-outline' },
    { titulo: 'Reportes', url: '/admin-reportes', icono: 'document-text-outline' },
  ];

  constructor(public authService: AuthService, private router: Router) {
    addIcons({
      homeOutline, hardwareChipOutline, addCircleOutline, phonePortraitOutline,
      listOutline, timeOutline, documentTextOutline, logOutOutline,
    });
  }

  logout() {
    this.authService.logout();
    this.router.navigateByUrl('/login');
  }
}
