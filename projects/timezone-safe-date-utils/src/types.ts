/** IANA timezone identifier (e.g., "America/New_York", "Europe/London", "UTC"). */
export type TimezoneString = string;

/** A date value paired with its timezone context. */
export interface SafeDate {
  /** The underlying Date object in UTC. */
  utc: Date;
  /** The IANA timezone identifier. */
  timezone: string;
  /** The UTC offset in minutes for this date in this timezone. */
  offset: number;
}

/** A range between two SafeDate values. */
export interface DateRange {
  start: SafeDate;
  end: SafeDate;
}

/** Options for formatting a SafeDate. */
export interface FormatOptions {
  /** Locale string (e.g., "en-US"). */
  locale?: string;
  /** Whether to include the timezone abbreviation. */
  includeTimezone?: boolean;
}
