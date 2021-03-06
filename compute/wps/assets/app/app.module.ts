import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { RouterModule } from '@angular/router';

import { AppComponent } from './app.component';
import { HomeComponent } from './home.component';
import { CreateUserComponent } from './create-user.component';
import { UpdateUserComponent } from './update-user.component';
import { LoginComponent } from './login.component';
import { LogoutComponent } from './logout.component';
import { ConfigureComponent } from './configure.component';
import { DimensionComponent } from './dimension.component';
import { JobsComponent } from './jobs.component';

import { AuthService } from './auth.service';
import { AuthGuard } from './auth-guard.service';
import { NotificationService } from './notification.service';

@NgModule({
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    RouterModule.forRoot([
      {
        path: 'wps/home',
        children: [
          {
            path: '',
            component: HomeComponent
          },
          {
            path: 'create',
            component: CreateUserComponent
          },
          {
            path: 'login',
            component: LoginComponent
          }
        ]
      },
      {
        path: 'wps/home',
        canActivate: [AuthGuard],
        children: [
          {
            path: 'jobs',
            component: JobsComponent
          },
          {
            path: 'profile',
            component: UpdateUserComponent
          },
          {
            path: 'logout',
            component: LogoutComponent
          },
          {
            path: 'configure',
            component: ConfigureComponent
          }
        ]
      }
    ])
  ],
  declarations: [
    AppComponent,
    HomeComponent,
    CreateUserComponent,
    UpdateUserComponent,
    LoginComponent,
    LogoutComponent,
    ConfigureComponent,
    DimensionComponent,
    JobsComponent
  ],
  providers: [
    AuthService,
    AuthGuard,
    NotificationService
  ],
  bootstrap: [ AppComponent ]
})

export class AppModule { }
