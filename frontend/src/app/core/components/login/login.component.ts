import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
    selector: 'app-login',
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.css']
})
export class LoginComponent {
    isLoading = false;
    selectedRole: string = 'admin'; // Default role

    constructor(private router: Router) { }

    onLogin() {
        this.isLoading = true;

        // Simulate API call and redirect
        setTimeout(() => {
            switch (this.selectedRole) {
                case 'admin':
                    this.router.navigate(['/admin']);
                    break;
                case 'caregiver':
                    this.router.navigate(['/caregiver']);
                    break;
                case 'patient':
                    this.router.navigate(['/family']);
                    break;
                default:
                    this.router.navigate(['/admin']);
            }
        }, 1500);
    }
}
