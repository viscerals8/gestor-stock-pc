import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HistorialPcsPage } from './historial-pcs.page';

describe('HistorialPcsPage', () => {
  let component: HistorialPcsPage;
  let fixture: ComponentFixture<HistorialPcsPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(HistorialPcsPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
