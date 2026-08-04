import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { ToastController } from '@ionic/angular';
import {
  IonContent, IonHeader, IonTitle, IonToolbar, IonItem,
  IonLabel, IonInput, IonButton, IonSelect, IonSelectOption,
  IonButtons, IonMenuButton
} from '@ionic/angular/standalone';
import { CelularService } from '../../core/services/celular.service';

@Component({
  selector: 'app-formulario-celular',
  templateUrl: './formulario-celular.page.html',
  styleUrls: ['./formulario-celular.page.scss'],
  standalone: true,
  imports: [
    CommonModule, ReactiveFormsModule,
    IonContent, IonHeader, IonTitle, IonToolbar, IonItem,
    IonLabel, IonInput, IonButton, IonSelect, IonSelectOption,
    IonButtons, IonMenuButton
  ]
})
export class FormularioCelularPage implements OnInit {
  form: FormGroup;
  celularId: number | null = null;
  guardando = false;
  errorMessage = '';

  constructor(
    private fb: FormBuilder,
    private celularService: CelularService,
    private route: ActivatedRoute,
    private router: Router,
    private toastCtrl: ToastController
  ) {
    this.form = this.fb.group({
      codigo: ['', Validators.required],
      numero: [''],
      marca: ['', Validators.required],
      modelo: ['', Validators.required],
      estado: ['Activo', Validators.required],
      usuario_asignado: [''],
      imei: [''],
      codigo_proyecto: [''],
      fecha_asignacion: [''],
    });
  }

  get esEdicion() {
    return this.celularId !== null;
  }

  ngOnInit() {
    const idParam = this.route.snapshot.paramMap.get('id');

    if (idParam) {
      this.celularId = Number(idParam);
      this.celularService.obtener(this.celularId).subscribe((celular) => {
        this.form.patchValue({
          ...celular,
          fecha_asignacion: celular.fecha_asignacion ? celular.fecha_asignacion.substring(0, 10) : '',
        });
        this.form.get('codigo')?.disable(); // el código no se puede modificar una vez creado
      });
    } else {
      this.sugerirCodigo();
    }
  }

  private sugerirCodigo() {
    this.celularService.listar().subscribe((celulares) => {
      const numeros = celulares
        .map(c => parseInt(c.codigo.replace(/\D/g, ''), 10))
        .filter(n => !isNaN(n));
      const siguiente = (numeros.length ? Math.max(...numeros) : 0) + 1;
      this.form.patchValue({ codigo: `CEL-${String(siguiente).padStart(3, '0')}` });
    });
  }

  guardar() {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.guardando = true;
    this.errorMessage = '';
    const valores = {
      ...this.form.getRawValue(),
      fecha_asignacion: this.form.value.fecha_asignacion || null,
    };

    const accion = this.esEdicion
      ? this.celularService.actualizar(this.celularId!, valores)
      : this.celularService.crear(valores);

    accion.subscribe({
      next: async () => {
        this.guardando = false;
        const toast = await this.toastCtrl.create({
          message: this.esEdicion ? 'Celular actualizado' : 'Celular creado',
          duration: 1500,
          color: 'success',
        });
        toast.present();
        this.router.navigateByUrl('/listado-celulares');
      },
      error: (err) => {
        this.guardando = false;
        this.errorMessage = err.status === 400
          ? 'Ya existe un celular con ese código.'
          : 'No se pudo guardar el celular. Intentá de nuevo.';
      }
    });
  }
}
