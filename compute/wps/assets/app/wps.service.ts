import { Injectable } from '@angular/core';
import { Http, URLSearchParams } from '@angular/http';

import { NotificationService } from './notification.service';

export interface WPSResponse {
  status: string;
  error: string;
  data: any;
}

export class Job {
  status: Status[];

  constructor(
    public id: number,
    public elapsed: string,
    public accepted: string[]
  ) { }

  reformatStatus(status: Status): Status {
    let p = new DOMParser();

    if (status.exception) {
      let xmlDoc = p.parseFromString(status.exception, 'text/xml');

      let elements = xmlDoc.getElementsByTagName('ows:ExceptionText');

      if (elements.length > 0) {
        status.exception = elements[0].innerHTML;
      }
    } else if (status.output) {
      let xmlDoc = p.parseFromString(status.output, 'text/xml');

      let elements = xmlDoc.getElementsByTagName('ows:ComplexData');

      if (elements.length > 0) {
        let variable = JSON.parse(elements[0].innerHTML);

        status.output = variable.uri;
      }
    }

    return status;
  }

  update(updates: Status[]): string {
    if (this.status === undefined) {
      this.status = new Array<Status>();
    }

    updates.forEach((s: Status) => {
      let match = this.status.find((i: Status) => i.status === s.status);

      if (match !== undefined) {
        s.messages.forEach((m: Message) => match.messages.push(m));
      } else {
        s = this.reformatStatus(s);

        this.status.push(s);
      }
    });

    return this.status[this.status.length-1].status || undefined;
  }
}

export interface Status {
  created_date: string;
  status: string;
  output: string;
  exception: string;
  messages: Message[];
}

export interface Message {
  created_date: string;
  percent: number;
  message: string;
}

@Injectable()
export class WPSService {
  constructor(
    private notificationService: NotificationService,
    private http: Http
  ) { }

  status(jobID: number): Promise<Status[]> {
    return this.http.get(`/wps/jobs/${jobID}`)
      .toPromise()
      .then(response => response.json().data as Status[])
      .catch(this.handleError);
  }

  update(jobID: number): Promise<Status[]> {
    return this.http.get(`/wps/jobs/${jobID}?update=true`)
      .toPromise()
      .then(response => response.json().data as Status[])
      .catch(this.handleError);
  }

  removeAll(): Promise<number> {
    return this.http.get('/wps/jobs/remove')
      .toPromise()
      .then(response => response.json())
      .catch(error => this.handleError(error));
  }

  remove(jobID: number): Promise<number> {
    return this.http.get(`/wps/jobs/${jobID}/remove`)
      .toPromise()
      .then(response => response.json())
      .catch(error => this.handleError(error));
  }

  jobs(index: number, limit: number): Promise<any> {
    let params = new URLSearchParams();

    params.append('index', ''+index);
    //params.append('limit', ''+limit);

    return this.http.get('/wps/jobs', {
      params: params 
    })
      .toPromise()
      .then(response => {
        let res = response.json();

        return {
          count: res.data.count,
          jobs: res.data.jobs.map((x: any) => new Job(x.id, x.elapsed, x.accepted))
        };
      })
      .catch(error => this.handleError(error));
  }
  
  private handleError(error: any): Promise<any> {
    this.notificationService.error(error.message || error);

    return Promise.reject(error.message || error);
  }
}
