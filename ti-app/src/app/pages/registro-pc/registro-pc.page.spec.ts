import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RegistroPcPage } from './registro-pc.page';

describe('RegistroPcPage', () => {
  let component: RegistroPcPage;
  let fixture: ComponentFixture<RegistroPcPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(RegistroPcPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
