// Does an in-place filter
export function filterInPlace<T>(arr: T[], f: (elm: T) => boolean): void {
  let out = 0;
  for (let i = 0; i < arr.length; i += 1) {
    if (f(arr[i])) {
      arr[out] = arr[i];
      out += 1;
    }
  }
  arr.length = out;
}
