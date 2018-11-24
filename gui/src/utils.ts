import { HttpParams } from '@angular/common/http';

export interface StringToSupportedValue {
  [s: string]: SupportedValue;
}

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

type SupportedValue = string | boolean | number;
function supportedValueToString(sv: SupportedValue) {
  if (sv === true) { return '1'; }
  if (sv === false) { return '0'; }
  return `${sv}`;
}

export function objectToParams(obj: StringToSupportedValue) {
  let params = new HttpParams();
  Object.keys(obj).forEach(key => {
    params = params.set(key, supportedValueToString(obj[key]));
  });
  return params;
}
