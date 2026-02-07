import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { CaregiverComponent } from './caregiver.component';

const routes: Routes = [
  { path: '', component: CaregiverComponent }
];

@NgModule({
  declarations: [CaregiverComponent],
  imports: [
    CommonModule,
    RouterModule.forChild(routes)
  ]
})
export class CaregiverModule { }
