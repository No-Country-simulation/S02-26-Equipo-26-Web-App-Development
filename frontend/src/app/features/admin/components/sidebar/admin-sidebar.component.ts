import { Component, EventEmitter, HostBinding, Input, Output } from '@angular/core';

@Component({
    selector: 'app-admin-sidebar',
    templateUrl: './admin-sidebar.component.html',
    styleUrls: ['./admin-sidebar.component.css']
})
export class AdminSidebarComponent {
     @Output() navigate = new EventEmitter<void>();
      @Input() collapsed = false;

  navItems = [
    { label: 'Dashboard', icon: 'dashboard', route: '/admin', active: false },
    { label: 'Cuidadores', icon: 'group', route: '/admin/caregivers', active: false },
    { label: 'Pacientes', icon: 'accessible', route: '/admin/patients', active: false },
    { label: 'Pagos', icon: 'payments', route: '/admin/payments', active: false },
    { label: 'Documentos', icon: 'folder', route: '/admin/documents', active: false },
    { label: 'Reportes', icon: 'bar_chart', route: '/admin/reports', active: false },
    { label: 'Configuración', icon: 'settings', route: '/admin/settings', active: false }
  ];

  onNavigate(): void {
    this.navigate.emit();
  }

   @HostBinding('class.collapsed')
  get isCollapsed() {
    return this.collapsed;
  }
}
