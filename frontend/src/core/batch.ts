/**
 * Batch processing types and utilities for Bubble Stretch Tool.
 */

import type { Insets } from './types'

/** Status of a batch item throughout the import/export lifecycle. */
export type BatchItemStatus =
  | 'pending'    // Imported, ready for processing
  | 'uploading'  // Being uploaded to backend
  | 'uploaded'   // Uploaded successfully
  | 'exporting'  // Being exported
  | 'exported'   // Export completed
  | 'failed'     // An error occurred

/** A single image in a batch import list. */
export interface BatchItem {
  /** Unique client-side identifier. */
  id: string
  /** Original File object from the file input. */
  file: File
  /** Original filename (basename). */
  filename: string
  /** Image width in pixels. */
  width: number
  /** Image height in pixels. */
  height: number
  /** File size in bytes. */
  sizeBytes: number
  /** Current processing status. */
  status: BatchItemStatus
  /** Error message when status is 'failed'. */
  error?: string
  /** Backend imageId after successful upload. */
  imageId?: string
}

/**
 * Apply a template's cap and content insets to a batch item.
 *
 * Returns a new BatchItem (reference-free) with the insets applied.
 * Currently this is a no-op passthrough since insets are handled at
 * the export stage; the function serves as an extension point for
 * future template-driven inset assignment.
 *
 * @param item - The source batch item.
 * @param _template - Template object with capInsets and contentInsets.
 * @returns A copy of the item (immutable application).
 */
export function applyTemplateToItem(
  item: BatchItem,
  _template: { capInsets: Insets; contentInsets: Insets },
): BatchItem {
  // Clone to avoid mutation; template application is a future extension.
  return { ...item }
}
