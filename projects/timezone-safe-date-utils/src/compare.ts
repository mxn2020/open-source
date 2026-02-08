import type { SafeDate } from "./types.js";

/**
 * Check whether SafeDate `a` is before SafeDate `b`.
 */
export function isBefore(a: SafeDate, b: SafeDate): boolean {
  return a.utc.getTime() < b.utc.getTime();
}

/**
 * Check whether SafeDate `a` is after SafeDate `b`.
 */
export function isAfter(a: SafeDate, b: SafeDate): boolean {
  return a.utc.getTime() > b.utc.getTime();
}

/**
 * Check whether two SafeDate values represent the same instant.
 */
export function isEqual(a: SafeDate, b: SafeDate): boolean {
  return a.utc.getTime() === b.utc.getTime();
}

/**
 * Return the difference in milliseconds (a - b).
 */
export function diffInMilliseconds(a: SafeDate, b: SafeDate): number {
  return a.utc.getTime() - b.utc.getTime();
}

/**
 * Return the difference in minutes (a - b).
 */
export function diffInMinutes(a: SafeDate, b: SafeDate): number {
  return diffInMilliseconds(a, b) / 60000;
}

/**
 * Return the difference in hours (a - b).
 */
export function diffInHours(a: SafeDate, b: SafeDate): number {
  return diffInMilliseconds(a, b) / 3600000;
}

/**
 * Return the difference in days (a - b).
 */
export function diffInDays(a: SafeDate, b: SafeDate): number {
  return diffInMilliseconds(a, b) / 86400000;
}
