import { ComponentFixture, TestBed } from '@angular/core/testing';
import { DetalleCelularesPage } from './detalle-celulares.page';

describe('DetalleCelularesPage', () => {
  let component: DetalleCelularesPage;
  let fixture: ComponentFixture<DetalleCelularesPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(DetalleCelularesPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
