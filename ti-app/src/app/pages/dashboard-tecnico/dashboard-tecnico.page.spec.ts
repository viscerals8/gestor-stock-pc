import { ComponentFixture, TestBed } from '@angular/core/testing';
import { DashboardTecnicoPage } from './dashboard-tecnico.page';

describe('DashboardTecnicoPage', () => {
  let component: DashboardTecnicoPage;
  let fixture: ComponentFixture<DashboardTecnicoPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(DashboardTecnicoPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
