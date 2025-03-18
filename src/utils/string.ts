/**
 * String To Category Value
 *
 * @param str
 * @param defaultStr
 * @returns
 */
export function convertToCategoryKey(
  str?: unknown,
  defaultStr: string = 'TYPE_A',
): string {
  if (typeof str !== 'string') {
    return defaultStr;
  } else {
    return str.replace(/\s+/g, '_').toUpperCase();
  }
}
