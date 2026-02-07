import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';

// Components
import { AdminLayoutComponent } from './layout/admin-layout.component';
import { AdminSidebarComponent } from './components/sidebar/admin-sidebar.component';
import { AdminTopbarComponent } from './components/topbar/admin-topbar.component';
import { AdminComponent } from './admin.component'; // Dashboard
// Pages
import { CaregiversComponent } from './pages/caregivers.component';
import { PatientsComponent } from './pages/patients.component';
import { PaymentsComponent } from './pages/payments.component';
import { DocumentsComponent } from './pages/documents.component';
import { ReportsComponent } from './pages/reports.component';
import { SettingsComponent } from './pages/settings.component';
import { ConfigComponent } from './pages/config.component';
import { CoreModule } from "src/app/core/core.module";

const routes: Routes = [
  {
    path: '',
    component: AdminLayoutComponent,
    children: [
      { path: '', component: AdminComponent },
      { path: 'dashboard', component: AdminComponent },
      { path: 'caregivers', component: CaregiversComponent },
      { path: 'patients', component: PatientsComponent },
      { path: 'payments', component: PaymentsComponent },
      { path: 'documents', component: DocumentsComponent },
      { path: 'reports', component: ReportsComponent },
      { path: 'settings', component: SettingsComponent },
      { path: 'config', component: ConfigComponent },
    ]
  }
];

@NgModule({
  declarations: [
    AdminLayoutComponent,
    AdminSidebarComponent,
    AdminTopbarComponent,
    AdminComponent,
    CaregiversComponent,
    PatientsComponent,
    PaymentsComponent,
    DocumentsComponent,
    ReportsComponent,
    SettingsComponent,
    ConfigComponent
  ],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    CoreModule
]
})
export class AdminModule { }
