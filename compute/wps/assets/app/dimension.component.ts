import { Component, Input, Output, EventEmitter } from '@angular/core';

export class Dimension {
  uuid: number;
  nameEdit: boolean = false;

  @Output() remove: EventEmitter<Dimension> = new EventEmitter();

  constructor(
    public name?: string,
    public unit?: string,
    public start?: number,
    public stop?: number,
    public step?: number
  ) { 
    this.uuid = new Date().getTime();

    this.nameEdit = this.name !== undefined;

    if (this.unit !== undefined) {
      this.name = `${this.name} (${this.unit})`;
    }

    if (this.step === undefined) {
      this.step = 1;
    }
  }
  
  valid(): any {
    let error = '';
    let values = [this.name, this.start, this.stop, this.step];  

    let result = values.every((element, index, array) => {
      return element !== undefined && element !== '';
    });

    if (!result) {
      error = 'Dimension is missing a value';
    } else {
      let name = this.name.toLowerCase();

      let time_pattern = /^t(ime)?.*$/;

      if (time_pattern.test(name)) {
        let pattern = /\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{1}/;

        let start = this.start + '';

        let stop = this.stop + '';

        if (!pattern.test(start) || !pattern.test(stop)) {
          return { result: false, error: 'Time must match format "YYYY-MM-DD HH:MM:SS.S"' };
        }
      }
    }

    return { result: result, error: error };
  }

  toString(): string {
    return JSON.stringify(this);
  }
}

@Component({
  selector: 'dimension',
  templateUrl: './dimension.component.html',
  styleUrls: ['./forms.css']
})
export class DimensionComponent {
  @Input() dimension: Dimension;

  onRemoveDimension(): void {
    this.dimension.remove.emit(this.dimension);
  }
}
