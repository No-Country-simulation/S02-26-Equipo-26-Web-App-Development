import { Component } from '@angular/core';

@Component({
    selector: 'app-admin-dashboard',
    templateUrl: './admin.component.html',
    styleUrls: ['./admin.component.css']
})
export class AdminComponent {
    stats = [
        { label: 'Acompañantes', value: '245', icon: 'groups', color: 'blue' },
        { label: 'Pacientes/Familia', value: '1,372', icon: 'elderly_woman', color: 'orange' },
        { label: 'Balance', value: '$105,265.75', icon: 'account_balance_wallet', color: 'green' }
    ];

    validationRequests = [
        { name: 'Nelson Gutiérrez', doc: 'Partición Geppert', type: 'Chofer hábitat', value: '$200.00', status: 'pending' },
        { name: 'Ana Martínez', doc: 'Mellouse Corntines', type: 'Gastos sistems', value: '$100.00', status: 'approved' },
        { name: 'José Pérez', doc: 'Martines Gamez', type: 'Gastos lopot', value: '$300.00', status: 'pending' }
    ];

    recentPayments = [
        { name: 'Marcos Andrada', amount: '$300.00', status: 'paid' },
        { name: 'José Tesuto', amount: '$45.00', status: 'paid' },
        { name: 'Aurora Rodriguez', amount: '$320.00', status: 'paid' },
        { name: 'Maria Aubeclasón', amount: '$-727.00', status: 'paid' }
    ];
}
