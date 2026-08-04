import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ListadoCelularesPage } from './listado-celulares.page';

describe('ListadoCelularesPage', () => {
  let component: ListadoCelularesPage;
  let fixture: ComponentFixture<ListadoCelularesPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(ListadoCelularesPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
