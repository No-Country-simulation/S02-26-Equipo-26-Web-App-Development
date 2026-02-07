import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { FamilyComponent } from './family.component';

const routes: Routes = [
  { path: '', component: FamilyComponent }
];

@NgModule({
  declarations: [FamilyComponent],
  imports: [
    CommonModule,
    RouterModule.forChild(routes)
  ]
})
export class FamilyModule { }
