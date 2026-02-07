import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router'; // Needed for routerLink or generic routing in core
import { HeaderComponent } from './components/header/header.component';
import { LoginComponent } from './components/login/login.component';
import { FormsModule } from '@angular/forms'; // Typically needed for login forms

@NgModule({
    declarations: [
        HeaderComponent,
        LoginComponent
    ],
    imports: [
        CommonModule,
        RouterModule,
        FormsModule
    ],
    exports: [
        HeaderComponent,
        LoginComponent
    ]
})
export class CoreModule { }
