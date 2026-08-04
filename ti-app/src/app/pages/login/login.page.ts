import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { IonicModule, LoadingController } from '@ionic/angular';
import { Router } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, IonicModule, ReactiveFormsModule],
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss']
})
export class LoginPage {
  loginForm: FormGroup;
  errorMessage = '';
  passwordVisible = false;

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private loadingCtrl: LoadingController,
    private authService: AuthService
  ) {
    this.loginForm = this.fb.group({
      correo: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(4)]]
    });
  }

  async onSubmit() {
    if (this.loginForm.invalid) {
      this.errorMessage = 'Completa los campos correctamente.';
      this.loginForm.markAllAsTouched();
      return;
    }

    const { correo, password } = this.loginForm.value;

    const loading = await this.loadingCtrl.create({
      message: 'Validando...',
      spinner: 'crescent'
    });
    await loading.present();

    this.authService.login(correo, password).subscribe({
      next: async () => {
        await loading.dismiss();
        this.errorMessage = '';
        this.router.navigateByUrl('/dashboard-tecnico');
      },
      error: async () => {
        await loading.dismiss();
        this.errorMessage = 'Correo o contraseña incorrectos.';
      }
    });
  }

  togglePassword() {
    this.passwordVisible = !this.passwordVisible;
  }
}
