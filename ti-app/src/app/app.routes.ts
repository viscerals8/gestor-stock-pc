import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'login',
    pathMatch: 'full',
  },
  {
    path: 'login',
    loadComponent: () =>
      import('./pages/login/login.page').then(m => m.LoginPage),
  },
  {
    path: 'registro-pc',
    canActivate: [authGuard],
    loadComponent: () =>
      import('./pages/registro-pc/registro-pc.page').then(m => m.RegistroPcPage),
  },
  {
    path: 'dashboard-tecnico',
    canActivate: [authGuard],
    loadComponent: () =>
      import('./pages/dashboard-tecnico/dashboard-tecnico.page').then(m => m.DashboardTecnicoPage),
  },
  {
    path: 'gestion-tareas',
    canActivate: [authGuard],
    loadComponent: () =>
      import('./pages/gestion-tareas/gestion-tareas.page').then(m => m.GestionTareasPage),
  },
  {
    path: 'inventario',
    canActivate: [authGuard],
    loadComponent: () =>
      import('./pages/inventario/inventario.page').then(m => m.InventarioPage),
  },
  {
    path: 'historial-pcs',
    canActivate: [authGuard],
    loadComponent: () =>
      import('./pages/historial-pcs/historial-pcs.page').then(m => m.HistorialPcsPage),
  },
  {
    path: 'pages',
    canActivate: [authGuard],
    loadComponent: () =>
      import('./pages/pages.page').then(m => m.PagesPage),
  },
  {
    path: 'admin-reportes',
    canActivate: [authGuard],
    loadComponent: () =>
      import('./pages/admin-reportes/admin-reportes.page').then(m => m.AdminReportesPage),
  },

  // ⭐ LISTADO CELULARES
  {
    path: 'listado-celulares',
    canActivate: [authGuard],
    loadComponent: () =>
      import('./pages/listado-celulares/listado-celulares.page')
        .then(m => m.ListadoCelularesPage),
  },

  // ⭐ DETALLE CELULAR
  {
    path: 'detalle-celulares/:id',
    canActivate: [authGuard],
    loadComponent: () =>
      import('./pages/detalle-celulares/detalle-celulares.page')
        .then(m => m.DetalleCelularesPage),
  },

  // ⭐ ALTA / EDICIÓN DE CELULAR
  {
    path: 'registro-celular',
    canActivate: [authGuard],
    loadComponent: () =>
      import('./pages/formulario-celular/formulario-celular.page')
        .then(m => m.FormularioCelularPage),
  },
  {
    path: 'registro-celular/:id',
    canActivate: [authGuard],
    loadComponent: () =>
      import('./pages/formulario-celular/formulario-celular.page')
        .then(m => m.FormularioCelularPage),
  },

  // ⭐ SIEMPRE AL FINAL
  {
    path: '**',
    redirectTo: 'login',
  },
];
