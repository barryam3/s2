import { HttpHeaders } from '@angular/common/http';

export const homepageURL = '/songs?suggested=1&sort=edited';

// Does an in-place filter
export function filterInPlace<T>(arr: T[], f: (elm: T) => boolean) {
  let out = 0;
  for (let i = 0; i < arr.length; i += 1) {
    if (f(arr[i])) {
      arr[out] = arr[i];
      out += 1;
    }
  }
  arr.length = out;
}

export function intToDate(date: number): Date {
  if (date === null) { return null; }
  if (date === undefined) { return undefined; }
  return new Date(date * 1000);
}

export function dateToInt(date: Date): number {
  if (date === null) { return null; }
  if (date === undefined) { return undefined; }
  return Math.floor(date.getTime() / 1000);
}

export const headers: HttpHeaders = new HttpHeaders({
  'Content-Type': 'application/json',
});

export function objectToParams(obj: { [s: string]: any }): { [s: string]: string } {
  const params = {};
  Object.keys(obj).forEach(key => {
    let val = obj[key];
    if (val === null || val === undefined) { return; }
    if (val === true) {
      val = '1';
    } else if (val === false) {
      val = '0';
    } else {
      val = `${val}`;
    }
    if (val.length > 0) {
      params[key] = val;
    }
  });
  return params;
}
