import { ComponentFixture, TestBed } from '@angular/core/testing';
import { GestionTareasPage } from './gestion-tareas.page';

describe('GestionTareasPage', () => {
  let component: GestionTareasPage;
  let fixture: ComponentFixture<GestionTareasPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(GestionTareasPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
