import { Inject, Injectable } from '@angular/core';
import { Http, Headers } from '@angular/http';
import { DOCUMENT } from '@angular/platform-browser';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';

import 'rxjs/add/operator/toPromise';

import { User } from './user';

@Injectable()
export class AuthService {
  logged = this.isLogged();

  logged$ = new BehaviorSubject(this.logged);

  constructor(@Inject(DOCUMENT) private doc: any, private http: Http) { }

  isLogged(): boolean {
    let expires = localStorage.getItem('wps_expires');

    if (expires != null) {
      let expiresDate = new Date(expires);

      if (expiresDate.getTime() > Date.now()) {
          return true
      }
    }

    return false;
  }

  getCookie(name: string): string {
    let cookieValue: string = null;

    if (this.doc.cookie && this.doc.cookie !== '') {
      let cookies: string[] = this.doc.cookie.split(';');

      for (let cookie of cookies) {
        if (cookie.trim().substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.trim().substring(name.length + 1));

          break;
        }
      }
    }

    return cookieValue;
  }

  userToUrlEncoded(user: User): string {
    let params: string = '';

    for (let k in user) {
      params += `${k.toLowerCase()}=${user[k]}&`;
    }

    return params;
  }

  create(user: User): Promise<string> {
    return this.http.post('auth/create/', this.userToUrlEncoded(user), {
      headers: new Headers({
        'X-CSRFToken': this.getCookie('csrftoken'),
        'Content-Type': 'application/x-www-form-urlencoded'
      })
    })
      .toPromise()
      .then(response => response.json())
      .catch(this.handleError);
  }

  login(user: User): Promise<string> {
    return this.http.post('auth/login/', this.userToUrlEncoded(user), {
      headers: new Headers({
        'X-CSRFToken': this.getCookie('csrftoken'),
        'Content-Type': 'application/x-www-form-urlencoded'
      })
    })
      .toPromise()
      .then(response => this.handleLoginResponse(response.json()))
      .catch(this.handleError);
  }

  logout(): Promise<string> {
    return this.http.get('auth/logout/', {
      headers: new Headers({
        'X-CSRFToken': this.getCookie('csrftoken'),
        'Content-Type': 'application/x-www-form-urlencoded'
      })
    })
      .toPromise()
      .then(response => this.handleLogoutResponse(response.json()))
      .catch(this.handleError);
  }

  private handleLoginResponse(response: any): any {
    if (response.status && response.status === 'success') {
      localStorage.setItem('wps_expires', response.expires);

      this.logged$.next(true);
    } else {
      this.handleLogoutResponse(response);
    }
  }

  private handleLogoutResponse(response: any): any {
    localStorage.removeItem('wps_expires');

    this.logged$.next(false);
  }

  private handleError(error: any): Promise<any> {
    return Promise.reject(error.message || error);
  }
}