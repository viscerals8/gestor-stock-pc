import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ToastController } from '@ionic/angular';
import { Camera, CameraResultType, CameraSource } from '@capacitor/camera';
import { PcService } from '../../core/services/pc.service';
import { UploadService } from '../../core/services/upload.service';
import {
  IonContent,
  IonHeader,
  IonTitle,
  IonToolbar,
  IonItem,
  IonLabel,
  IonInput,
  IonButton,
  IonSelect,
  IonSelectOption,
  IonMenuButton,
  IonButtons,
  IonIcon,
} from '@ionic/angular/standalone';
import { addIcons } from 'ionicons';
import { cameraOutline, imageOutline } from 'ionicons/icons';

@Component({
  selector: 'app-registro-pc',
  templateUrl: './registro-pc.page.html',
  styleUrls: ['./registro-pc.page.scss'],
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,

    // Componentes de Ionic utilizados en la vista
    IonContent,
    IonHeader,
    IonTitle,
    IonToolbar,
    IonItem,
    IonLabel,
    IonInput,
    IonButton,
    IonSelect,
    IonSelectOption,
    IonMenuButton,
    IonButtons,
    IonIcon,
  ]
})
export class RegistroPcPage {
  private fb = inject(FormBuilder);
  private toastCtrl = inject(ToastController);
  private pcService = inject(PcService);
  private uploadService = inject(UploadService);

  registroForm: FormGroup;
  fotoPreview: string | null = null;
  qrGenerado = false;
  guardando = false;
  subiendoFoto = false;
  errorMessage = '';

  constructor() {
    addIcons({ cameraOutline, imageOutline });
    this.registroForm = this.fb.group({
      nroSerie: ['', Validators.required],
      marca: ['', Validators.required],
      modelo: ['', Validators.required],
      motivo: ['', Validators.required],
      estado: ['', Validators.required],
      foto: [null]
    });
  }

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.subirArchivo(file, file.name);
    }
  }

  async tomarFoto() {
    try {
      const foto = await Camera.getPhoto({
        resultType: CameraResultType.DataUrl,
        source: CameraSource.Prompt,
        quality: 80,
      });
      if (!foto.dataUrl) return;

      const blob = await (await fetch(foto.dataUrl)).blob();
      this.subirArchivo(blob, `foto.${foto.format || 'jpg'}`);
    } catch {
      // el usuario canceló la captura, no hacemos nada
    }
  }

  private subirArchivo(archivo: Blob, nombre: string) {
    this.subiendoFoto = true;
    this.uploadService.subirFoto(archivo, nombre).subscribe({
      next: (url) => {
        this.fotoPreview = url;
        this.registroForm.patchValue({ foto: url });
        this.subiendoFoto = false;
      },
      error: async () => {
        this.subiendoFoto = false;
        const toast = await this.toastCtrl.create({
          message: 'No se pudo subir la foto. Intentá de nuevo.',
          duration: 1800,
          color: 'danger',
        });
        toast.present();
      }
    });
  }

  async generarTicket() {
    if (this.registroForm.invalid) return;

    const { nroSerie, marca, modelo, motivo, estado, foto } = this.registroForm.value;

    this.guardando = true;
    this.errorMessage = '';

    this.pcService.crear({
      nro_serie: nroSerie,
      marca,
      modelo,
      motivo,
      estado,
      usuario_asignado: null,
      foto_url: foto,
    }).subscribe({
      next: async () => {
        this.guardando = false;
        const toast = await this.toastCtrl.create({
          message: 'PC registrado correctamente',
          duration: 1500,
          color: 'success'
        });
        toast.present();

        this.qrGenerado = true; // simulación de qr generado, no hay impresora conectada
      },
      error: async (err) => {
        this.guardando = false;
        this.errorMessage = err.status === 400
          ? 'Ya existe un PC con ese número de serie.'
          : 'No se pudo registrar el PC. Intentá de nuevo.';
      }
    });
  }

  limpiar() {
    this.registroForm.reset();
    this.fotoPreview = null;
    this.qrGenerado = false;
    this.errorMessage = '';
  }
}
