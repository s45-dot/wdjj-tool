import { apiPost } from './client'

export interface BatchExportItemPayload {
  imageId: string
}

export interface BatchUploadRequest {
  /** Array of images to include in batch export. */
  images: BatchExportItemPayload[]
  /** Scale factors to generate for each image. */
  selectedScales: number[]
  /** Cap insets to apply to each image. */
  capInsets: { top: number; right: number; bottom: number; left: number }
  /** Content insets to apply to each image. */
  contentInsets: { top: number; right: number; bottom: number; left: number }
  /** Preview dimensions for each export. */
  preview: { targetWidth: number; targetHeight: number }
}

export interface BatchExportResult {
  fileId: string
  filename: string
  downloadUrl: string
}

/**
 * Send a batch export request to the backend.
 *
 * The backend processes all images with the given settings and
 * returns a single ZIP containing all export artifacts.
 */
export async function batchExport(request: BatchUploadRequest): Promise<BatchExportResult> {
  return apiPost<BatchExportResult>('/api/export/batch', request)
}
