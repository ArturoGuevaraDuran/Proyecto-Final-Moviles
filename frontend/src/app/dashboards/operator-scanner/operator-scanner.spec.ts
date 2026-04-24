import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OperatorScanner } from './operator-scanner';

describe('OperatorScanner', () => {
  let component: OperatorScanner;
  let fixture: ComponentFixture<OperatorScanner>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OperatorScanner],
    }).compileComponents();

    fixture = TestBed.createComponent(OperatorScanner);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
