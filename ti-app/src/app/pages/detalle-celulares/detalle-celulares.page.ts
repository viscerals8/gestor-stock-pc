import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { AlertController, ToastController } from '@ionic/angular';

// Importar solo los componentes usados
import {
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardSubtitle,
  IonCardContent,
  IonButton,
  IonButtons,
  IonMenuButton
} from '@ionic/angular/standalone';
import { CelularService } from '../../core/services/celular.service';
import { Celular } from '../../core/models/celular.model';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-detalle-celulares',
  standalone: true,
  templateUrl: './detalle-celulares.page.html',
  styleUrls: ['./detalle-celulares.page.scss'],
  imports: [
    CommonModule,
    RouterLink,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonContent,
    IonCard,
    IonCardHeader,
    IonCardTitle,
    IonCardSubtitle,
    IonCardContent,
    IonButton,
    IonButtons,
    IonMenuButton
  ]
})
export class DetalleCelularesPage implements OnInit {

  celular: Celular | null = null;
  cargando = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private celularService: CelularService,
    private authService: AuthService,
    private alertCtrl: AlertController,
    private toastCtrl: ToastController,
  ) {}

  get puedeEliminar() {
    return this.authService.tieneRol('admin');
  }

  ngOnInit() {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    if (!id) return;

    this.cargando = true;
    this.celularService.obtener(id).subscribe({
      next: (celular) => {
        this.celular = celular;
        this.cargando = false;
      },
      error: () => {
        this.cargando = false;
      }
    });
  }

  async eliminar() {
    if (!this.celular) return;

    const alert = await this.alertCtrl.create({
      header: 'Eliminar celular',
      message: `¿Seguro que querés eliminar ${this.celular.codigo}? Esta acción no se puede deshacer.`,
      buttons: [
        { text: 'Cancelar', role: 'cancel' },
        {
          text: 'Eliminar',
          role: 'destructive',
          handler: () => this.confirmarEliminacion()
        }
      ]
    });
    await alert.present();
  }

  private confirmarEliminacion() {
    if (!this.celular) return;

    this.celularService.eliminar(this.celular.id).subscribe({
      next: async () => {
        const toast = await this.toastCtrl.create({
          message: 'Celular eliminado',
          duration: 1500,
          color: 'success'
        });
        toast.present();
        this.router.navigateByUrl('/listado-celulares');
      },
      error: async () => {
        const toast = await this.toastCtrl.create({
          message: 'No se pudo eliminar el celular',
          duration: 1500,
          color: 'danger'
        });
        toast.present();
      }
    });
  }
}
